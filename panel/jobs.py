from django.http import HttpResponse
from django.core import serializers
import urllib.request
from django.db import transaction
from .models import Coordinates, Units, PowerExpected, PowerActual, Performance
from .utils import string_json_mapper
import numpy as np
from django.db.models import Q
from datetime import date
from dateutil.rrule import rrule, DAILY
import json
import simplejson
import ast
import datetime
import decimal
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

## ToDo- Put up Error handeling in place. ##
# from panel import jobs as a
# a.get_expected_data()
def get_expected_data():
	''' Makes cURL call with the metedata'''
	AZIMUTH = 180
	ARRAY_TYPE = 1
	MODULE_TYPE = 1
	LOOSES = 10
	API_KEY='DEMO_KEY'
	DATASET='IN'
	TIMEFRAME='hourly'

	base_url = "https://developer.nrel.gov/api/pvwatts/v5.json?"
	url_with_constants = base_url + '&azimuth=' + str(AZIMUTH) + '&array_type=' + str(ARRAY_TYPE) + '&module_type=' + str(MODULE_TYPE) + '&losses=' + str(LOOSES) + '&api_key=' + API_KEY + '&dataset=' + DATASET + '&timeframe=' + TIMEFRAME

	units_installed = Units.objects.all()
	for each_unit in units_installed:
		coordinates = Coordinates.objects.get(pk=each_unit.co_ordinates_id)
		capacity = each_unit.capacity
		lat = coordinates.lat
		lon = coordinates.lon
		url = url_with_constants + '&lat=' + str(lat) + '&lon=' + str(lon) + '&system_capacity=' + str(capacity) + '&tilt=' + str(lat)

		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		update_power_expected_table(response.read().decode('utf-8'), each_unit)
	return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")

def update_power_expected_table(response, each_unit):
	''' Inserts data into table for all the entries'''
	try:
		response = ast.literal_eval(response)
		dc_expected = response['outputs']['dc']
		entry = PowerExpected()
		entry.expected_dc = simplejson.dumps(dc_expected)
		entry.unit = each_unit
		entry.save()
	except KeyError:
		print("No output found in response!!")
	return 1

def simulate_energy_days_generation():
	"""
	This is just for simulating data for days.
	A function to pass time.now and call other function, for all systems installed -> 
	call normal distribution with current time, system indetifier and system capacity().
	A simulator function returns simulated data: Write the data in db against System id(FK), Date given.
	"""
	mar_date = date(2017, 3, 20)
	april_date = date(2017, 4, 20)

	for dt in rrule(DAILY, dtstart=mar_date, until=april_date):
		date_now = dt.strftime("%Y-%m-%d")
		date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d")
		units_installed = Units.objects.all()

		for each_unit in units_installed:
			simulated_dc_value = system_date_mapper(date_now, each_unit)
			# Save simulated_dc_value value in db.
			result = [save_power_actual(each_unit, date_now, each_power) for each_power in simulated_dc_value if simulated_dc_value]	
			logger.info("Data for Date {}  and system {} populated" .format(date_now, each_unit))

def save_power_actual(each_unit, date_now, each_power):
	entry = PowerActual(unit=each_unit, stamp_date=date_now, actual_dc=each_power)
	entry.save()


def system_date_mapper(today_date, each_unit):
	'''
		This will receive date, time and System ID and will return simulated value of energy in watt
	'''
	actual_dc = get_normal_distribution(each_unit.capacity)
	return actual_dc

def get_normal_distribution(capacity):
	'''
		Returns simulated value of heat based on normal distribution curve in List
	'''
	capacity_in_watt = capacity * 1000
	mu = (capacity_in_watt * decimal.Decimal(.70)) #Making an approximation for mean value to be 90% of system capacity
	sigma = mu/13 # As there are 13 numbers having data like bell curve, so making equal SD.
	series = np.random.normal(mu, sigma, 13)
	series = sorted(series)
	series_inc = series[::2]
	series_dec = series[-2::-2]
	energy_7_to_19 = series_inc + series_dec
	energy_0_to_6 = [0, 0, 0, 0, 0, 0, 0]
	energy_20_to_23 = [0, 0, 0, 0]
	daily_energy = energy_0_to_6 + energy_7_to_19 + energy_20_to_23
	return daily_energy

def update_performance_table():
	'''
	Steps:
	1. For Given date, Get all 24 data points from power_expected table
	2. For Given date, Get all 24 data points from power_actual table
	3. Check for eligiblity criteria(80 % performance) 
		if lesser performance, make an entry in performance table.
	'''

	mar_date = date(2017, 3, 20)
	april_date = date(2017, 4, 20)
	units_installed = Units.objects.all()

	for dt in rrule(DAILY, dtstart=mar_date, until=april_date):
		date_now = dt.strftime("%Y-%m-%d")
		date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d")

		result = [performance_task(each_unit, date_now) for each_unit in units_installed if units_installed]
		print(result)

def performance_task(each_unit, date_now):
	exp_power = expected_power(each_unit, date_now)
	act_power = list(actual_power(each_unit, date_now))
	time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	for each in time:
		print(type(act_power[each]))
		print(type(exp_power[each]))
		if (act_power[each] < decimal.Decimal(.80)*decimal.Decimal(exp_power[each])):
			# Insert row in Performance table
			p = Performance(unit=each_unit, hours=each, performance_date=date_now)
			p.save()

def actual_power(each_unit, date_now):
	power_actual = PowerActual.objects.values_list('actual_dc', flat=True).filter(Q(unit=each_unit) & Q(stamp_date=date_now))
	return power_actual

def expected_power(each_unit, date_now):
	days_dict = { # Dict for month number and days in it.
		1: 31,
		2: 28,
		3: 31,
		4: 30,
		5: 31,
		6: 30,
		7: 31,
		8: 31,
		9: 30,
		10: 31,
		11: 30,
		12: 31
	}
	today_date = date_now
	day = today_date.day
	month = today_date.month
	days_in_months = 0
	for i in range(1, month):
		days_in_months += days_dict[i]
	
	total_days_to_ignore_for_eval = days_in_months + (day-1)
	total_hours_to_ignore_for_eval = total_days_to_ignore_for_eval*24
	expected_power = PowerExpected.objects.filter(unit=each_unit).values('expected_dc')
	expected_power = expected_power[0]['expected_dc']
	expected_power = string_json_mapper(expected_power)
	expected_power_exact = expected_power[total_hours_to_ignore_for_eval:total_hours_to_ignore_for_eval+24]
	return expected_power_exact

# A Scheduler for sending mail to each panel for the given date at 8 PM IST.
    
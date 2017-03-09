from django.http import HttpResponse
from django.core import serializers
import urllib.request
from django.db import transaction
from .models import Coordinates, Units, PowerExpected, PowerActual, Performance
import numpy as np
from django.db.models import Q
import json
import ast
import datetime
import decimal
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

## ToDo- Put up logger for putting logs ##
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
		for each in dc_expected:
			entry = PowerExpected(unit=each_unit, expected_dc=each)
			entry.save()
		transaction.commit()
	except KeyError:
		print("No output found in response!!")
	return 1

def simulate_energy_generation():
	"""
	A function to pass time.now and call other function, for all systems installed -> 
	call normal distribution with current time, system indetifier and system capacity().
	A simulator function returns simulated data: Write the data in db against System id(FK), Date given.
	"""
	today_date = datetime.datetime.now().date()
	now_time = datetime.datetime.now().time()
	units_installed = Units.objects.all()
	for each_unit in units_installed:
		simulated_dc_value = system_time_date_mapper(today_date, now_time, each_unit)
		# Save simulated_dc_value value in db.
		entry = PowerActual(unit=each_unit, stamp_date=today_date, actual_dc=simulated_dc_value)
		entry.save()
		logger.info("{}" .format(simulated_dc_value))

def system_time_date_mapper(today_date, now_time, each_unit):
	'''
		This will receive date, time and System ID and will return simulated value of energy in watt
	'''
	actual_dc = get_normal_distribution(each_unit.capacity)
	hour = now_time.hour
	return actual_dc[hour]

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
	1. For Given date(today), Get all 24 data points from performance_expected_table
	2. For Today, Get all 24 data points from performance_expected tables
	3. Check for eligiblity criteria(80 % performance) 
		if lesser performance, make an entry in performance table.
	'''
	today_date = datetime.date.today()
	now_time = datetime.datetime.now().time()
	units_installed = Units.objects.all()
	for each_unit in units_installed:
		expected_power = expected_energy_data(each_unit, today_date, now_time)
		actual_power = actual_energy_data(each_unit, today_date, now_time)
		print(expected_power)
		print(actual_power)
		if (actual_power < decimal.Decimal(.80)*expected_power):
			# Insert row in Performance table
			p = Performance(unit=each_unit, hours=now_time, performance_date=today_date)
			p.save()		

def actual_energy_data(each_unit, today_date, now_time):
	power_actual = PowerActual.objects.filter(Q(unit=each_unit) & Q(stamp_date=today_date))
	hour = now_time.hour
	actual_power_now = power_actual[hour]
	return actual_power_now.actual_dc
	

def expected_energy_data(each_unit, date, now_time):
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
	hour = now_time.hour
	today_date = date
	day = today_date.day
	month = today_date.month
	days_in_months = 0
	for i in range(1, month):
		days_in_months += days_dict[i]
	
	total_days_to_ignore_for_eval = days_in_months + (day-1)
	total_hours_to_ignore_for_eval = total_days_to_ignore_for_eval*24
	expected_power = PowerExpected.objects.filter(unit=each_unit)[total_hours_to_ignore_for_eval:total_hours_to_ignore_for_eval+24]
	expected_power_now = expected_power[hour]
	return expected_power_now.expected_dc


    
    
    
    
    
    
    
    
    
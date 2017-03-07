from django.http import HttpResponse
from django.core import serializers
import urllib.request
from django.db import transaction
from .models import Coordinates, Units, PowerExpected, PowerActual, Performance
import numpy as np
import json
import ast
import datetime
import decimal

## ToDo- Put up logger for putting logs ##
## ToDo- Put up Error handeling in place. ##
def get_expected_data(request):
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

"""
A function to pass time.now and call other function, for all systems installed -> 
call normal distribution with current time, system indetifier and system capacity().
A simulator function returns simulated data: Write the data in db against System id(FK), Date given. 

from panel import jobs as a
a.simulate_energy_generation()

"""


def simulate_energy_generation():
	today_date = datetime.datetime.now().date()
	#today_date = datetime.datetime.strptime(str(today_date), '%Y-%m-%d').strftime('%d-%m-%Y')
	#Use above code for making an API mentioned in PRD, commenting temporirly.
	now_time = datetime.datetime.now().time()
	units_installed = Units.objects.all()
	for each_unit in units_installed:
		simulated_dc_value = system_time_date_mapper(today_date, now_time, each_unit)
		# Save simulated_dc_value value in db.
		entry = PowerActual(unit=each_unit, stamp_date=today_date, actual_dc=simulated_dc_value)
		entry.save()
		print("{}" .format(simulated_dc_value))

def system_time_date_mapper(today_date, now_time, each_unit):
	'''
		This will receive date, time and System ID and will return simulated value of energy in watt
	'''
	# 0-0, 1-0, 2-0, 3-0, 4-0, 5-0, 6-0, 
	# 7-1000, 8-2000, 9-3000, 10-4000, 11-5000, 12-6000, 13-8000,
	# 14-7000, 15-6000, 16-5000, 17-4000, 18-3000, 19-1000,
	# 20-0, 21-0, 22-0, 23-0, 24-0
	#10 * 1000
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



    
    
    
    
    
    
    
    
    
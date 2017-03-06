from django.http import HttpResponse
from django.core import serializers
import urllib.request
import json
from .models import Coordinates, Units, PowerExpected, PowerActual, Performance


def index(request):
    return HttpResponse("At panel Index")

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
	for each_units in units_installed:
		coordinates = Coordinates.objects.get(pk=each_units.co_ordinates_id)
		capacity = each_units.capacity
		lat = coordinates.lat
		lon = coordinates.lon
		url = url_with_constants + '&lat=' + str(lat) + '&lon=' + str(lon) + '&system_capacity=' + str(capacity) + '&tilt=' + str(lat)

		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		update_power_expected_table(response.read().decode('utf-8'))
	return HttpResponse(json.dumps('a'), content_type="application/json")

def update_power_expected_table(response):
	print(response)
	return 1



    
    
    
    
    
    
    
    
    
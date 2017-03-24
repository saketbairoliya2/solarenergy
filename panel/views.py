from django.http import HttpResponse
from .models import Units, PowerExpected, PowerActual, Performance
from .utils import validate
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import send_mail
import urllib.request
from datetime import date
from django.http import HttpResponse
import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

BASE_URL = "https://solarenergy.herokuapp.com/panel/"
MAIL_FROM = "solarenergysaket@gmail.com"
MAIL_TO = ['saketbairoliya2@gmail.com']
SUBJECT = "Daily Report"

def index(request):
    return HttpResponse("At panel Index")

def details(request, panel_id):
	message = "Please enter date in DD-MM-YYYY format"
	try:
		date = request.GET['date']
	except Exception as e:
		return JsonResponse({
		"status": "error",
		"data": None,
		"message": "No date is specified"
		})
		
	try:
		validate(date)
	except ValueError:
		logger.error("Please enter date in DD-MM-YYYY format")
		return JsonResponse({
			"status": "error",
			"data": None,
			"message": message
			})
	date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')

	performances = Performance.objects.filter(Q(performance_date=date) & Q(unit__id=panel_id)).values('hours')
	
	return JsonResponse({
		"status": "success",
		"data": list(performances),
		"message": None
		})

def send_daily_mail(request, panel_id):
	try:
		date = request.GET['date']
	except Exception as e:
		return JsonResponse({
		"status": "error",
		"data": None,
		"message": "No date is specified"
		})

	if date is not None:
		# Call url for getting data for the given date and panel.
		url = BASE_URL + str(panel_id) + '?date=' + date
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		response = response.read().decode('utf-8')
		subject = SUBJECT + ' for panel ' + str(panel_id)
		send_mail(subject, str(response), MAIL_FROM, MAIL_TO, fail_silently=False)
		logger.info('Mail Sent to user')

	return JsonResponse({
		"status": "success",
		"data": 'preference',
		"message": 'Mail sent'
		})

def prepare_daily_mail(request):
	today_date = datetime.datetime.now().date()
	date = today_date.strftime('%d-%m-%Y')
	units = Units.objects.all()
	for unit in units:
		url = BASE_URL + str(unit.id) + "/mail?date=" + str(date)
		request = urllib.request.Request(url)
		response = urllib.request.urlopen(request)
		response = response.read().decode('utf-8')
		logger.info(response)
	return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")


    
    
    
    
    
    
    
    
    
from django.http import HttpResponse
from .models import Units, PowerExpected, PowerActual, Performance
from .utils import validate
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("At panel Index")

def details(request, panel_id):
	message = "Please enter date in DD-MM-YYYY format"
	try:
		date = request.GET['date']
	except Exception as e:
		# In case no dates are specified, take today date.
		date = datetime.date.today()
		date = datetime.datetime.strptime(date, '%d-%m-%Y')
	try:
		validate(date)
	except ValueError:
		logger.error("Please enter date in DD-MM-YYYY format")
		return JsonResponse({
			"status": "error",
			"data": null,
			"message": message
			})
	date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')

	performances = Performance.objects.filter(Q(performance_date=date) & Q(unit__id=panel_id)).values('hours')
	
	return JsonResponse({
		"status": "success",
		"data": list(performances),
		"message": None
		})





    
    
    
    
    
    
    
    
    
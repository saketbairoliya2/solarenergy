import datetime
from django.core.mail import send_mail
from .models import Performance, Units
from django.db.models import Q
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
 

def validate(date_text):
    try:
    	datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
    	raise ValueError("Incorrect data format, should be DD-MM-YYYY")

def send_daily_mail():
	#At given time, call this function with content
	today_date = datetime.datetime.now().date()
	total_units = Units.objects.all()
	for each_units in total_units:
		performance = Performance.objects.filter(Q(performance_date=today_date) & Q(unit=each_units)).values('hours')
		## To-Do part here, Have to decide the format of things here## 
		# try:
		# 	performance = performance[0]
		# except Exception as e:
		# 	performance = {}
		# 	logger.info(e)
		# performance = performance.strftime('%H:%M')
		# print(str(performance))
		# print(type(performance)) 
		#send_mail('Daily report', performance, 'solarenergysaket@gmail.com', ['saketbairoliya2@gmail.com'], fail_silently=False)

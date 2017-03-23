from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail
from panel.models import Units, Performance
from datetime import date
import datetime
from django.http import HttpResponse
import urllib.request
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

BASE_URL = "https://solarenergy.herokuapp.com/panel/"

# @sched.scheduled_job('interval', minutes=2)
# def timed_job():
# 	logger.info('This job is run every two minutes.')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=15, minute=0)
def scheduled_job():
	logger.info('This job is run every day at 8:30pm.')
	today_date = datetime.datetime.now().date()
	date = today_date.strftime('%d-%m-%Y')
	units = Units.objects.all()
	for unit in units:
		url = BASE_URL + str(unit.id) + "/send_mails?date=" + str(date)
		request = urllib.request.Request(url)
	return HttpResponse(json.dumps({'success': 'true'}), content_type="application/json")
	logger.info('Daily reports sent for all panels')
sched.start()
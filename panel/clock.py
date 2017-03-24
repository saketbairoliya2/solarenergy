from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail
import urllib.request
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

BASE_URL = "https://solarenergy.herokuapp.com/panel/call"

@sched.scheduled_job('interval', minutes=3)
def timed_job():
	logger.info('This job is run every two minutes.')
	url = BASE_URL
	request = urllib.request.Request(url)
	logger.info('Daily reports sent for all panels')

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=14, minute=30)
def scheduled_job():
	logger.info('This job is run every day at 8:00pm.')
	url = BASE_URL
	request = urllib.request.Request(url)
	logger.info('Daily reports sent for all panels')


sched.start()
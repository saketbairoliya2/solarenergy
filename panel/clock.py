from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail
import urllib.request
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

BASE_URL = "https://solarenergy.herokuapp.com/panel/call"

# @sched.scheduled_job('interval', minutes=2)
# def timed_job():
# 	logger.info('This job is run every two minutes.')

#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=6, minute=00)
@sched.scheduled_job('interval', minutes=3)
def scheduled_job():
	logger.info('This job is run every day at 8:30pm.')
	url = BASE_URL
	request = urllib.request.Request(url)
	logger.info('Daily reports sent for all panels')

#@sched.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=30)
# def scheduled_job():
# 	logger.info('This job is run every day at 8:30pm.')
# 	url = BASE_URL
# 	request = urllib.request.Request(url)
# 	logger.info('Daily reports sent for all panels')

sched.start()
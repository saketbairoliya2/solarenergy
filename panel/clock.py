from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.scheduler import Scheduler
from django.core.mail import send_mail
# import schedule
# import time
import urllib.request
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

#sched = BlockingScheduler()

BASE_URL = "https://solarenergy.herokuapp.com/panel/call"

# Start the scheduler
sched = Scheduler()
sched.start()

def job_function():
	logger.info('This job is run every day at 8:00pm.')
	url = BASE_URL
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	response = response.read().decode('utf-8')
	logger.info('Daily reports sent for all panels')

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
sched.add_cron_job(job_function, day_of_week='mon-sun', hour=4, minute=4)
sched.add_cron_job(job_function, day_of_week='mon-sun', hour=9, minute=34)

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
# 	logger.info('This job is run every two minutes.')
# 	url = BASE_URL
# 	request = urllib.request.Request(url)
# 	response = urllib.request.urlopen(request)
# 	response = response.read().decode('utf-8')
# 	logger.info('Daily reports sent for all panels')

# To check for IST time acceptance, basically program call
# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=30)
# def scheduled_job():
# 	logger.info('This job is run every day at 8:00pm.')
# 	url = BASE_URL
# 	request = urllib.request.Request(url)
# 	response = urllib.request.urlopen(request)
# 	response = response.read().decode('utf-8')
# 	logger.info('Daily reports sent for all panels')

# # To test for UST time acceptance
# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, minute=00)
# def scheduled_job():
# 	logger.info('This job is run every day at 8:00pm.')
# 	url = BASE_URL
# 	request = urllib.request.Request(url)
# 	response = urllib.request.urlopen(request)
# 	response = response.read().decode('utf-8')
# 	logger.info('Daily reports sent for all panels')

# sched.start()

# def job():
# 	logger.info('This job is run every day at 8:00pm.')
# 	url = BASE_URL
# 	request = urllib.request.Request(url)
# 	response = urllib.request.urlopen(request)
# 	response = response.read().decode('utf-8')
# 	logger.info('Daily reports sent for all panels')

# schedule.every(2).minutes.do(job)

# # schedule.every().day.at("10:30").do(job)
# # schedule.every().monday.do(job)
# # schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

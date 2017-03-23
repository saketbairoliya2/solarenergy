from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail
import urllib.request
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

MAIL_FROM = "solarenergysaket@gmail.com"
MAIL_TO = ['saketbairoliya2@gmail.com']

@sched.scheduled_job('interval', minutes=2)
def timed_job():
	url = "https://solarenergy.herokuapp.com/panel/1/send_mails/?date=20-03-2017"
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	response = response.read().decode('utf-8')
	subject = "Demo Mail"
	send_mail(subject, str(response), MAIL_FROM, MAIL_TO, fail_silently=False)
	logger.info('Mail Sent to user')
	logger.info('This job is run every two minutes.')

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=20)
# def scheduled_job():
#     logger.info('This job is run every weekday at 8pm.')

sched.start()
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every three minutes.')
    logger.info('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=20)
def scheduled_job():
    print('This job is run every weekday at 8pm.')
    logger.info('This job is run every weekday at 8pm.')
sched.start()
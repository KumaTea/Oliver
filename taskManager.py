from apscheduler.schedulers.blocking import BlockingScheduler
from mdSYSU import send_greetings, send_flood

scheduler = BlockingScheduler()


def manager():
    scheduler.add_job(send_greetings, 'cron', hour=7, minute=30)
    scheduler.add_job(send_flood, 'cron', hour=21)

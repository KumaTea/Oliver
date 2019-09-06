from apscheduler.schedulers.blocking import BlockingScheduler
from mdSYSU import send_greetings, send_flood
from checkUrl import task_check

scheduler = BlockingScheduler()


def manager():
    scheduler.add_job(send_greetings, 'cron', hour=7, minute=30)
    scheduler.add_job(send_flood, 'cron', hour=21)
    scheduler.add_job(task_check, 'cron', hour='*/4')

from apscheduler.schedulers.blocking import BlockingScheduler
from mdSYSU import send_greetings, send_flood
from checkUrl import task_check
from mdTum import sync_posts, send_post

scheduler = BlockingScheduler()


def manager():
    scheduler.add_job(send_greetings, 'cron', hour=7, minute=30)
    scheduler.add_job(send_flood, 'cron', hour=21)
    scheduler.add_job(task_check, 'cron', hour='*/4')
    scheduler.add_job(sync_posts, 'cron', hour=6)
    scheduler.add_job(send_post, 'cron', hour='3,7,11,15,19,23')

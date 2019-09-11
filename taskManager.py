from apscheduler.schedulers.blocking import BlockingScheduler
from mdSYSU import send_greetings, send_flood, send_con
from checkUrl import task_check
from mdTum import sync_posts, send_post
from mdBackup import do_backup

scheduler = BlockingScheduler()


def manager():
    scheduler.add_job(send_greetings, 'cron', hour=7, minute=30)
    scheduler.add_job(send_flood, 'cron', hour=21)
    scheduler.add_job(task_check, 'cron', hour='*/4')
    scheduler.add_job(sync_posts, 'cron', hour=6)
    scheduler.add_job(send_post, 'cron', hour='0,4,8,12,16,20')
    scheduler.add_job(send_con, 'cron', hour=7, minute=59)
    scheduler.add_job(do_backup, 'cron', day_of_week='sat', hour=2)

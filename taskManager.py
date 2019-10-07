from apscheduler.schedulers.blocking import BlockingScheduler
from mdSYSU import send_greetings, send_flood, send_con
from checkUrl import check_url
from mdTum import sync_posts, send_post
from mdDra import send_news_zh, send_news_en
from mdBackup import do_backup

scheduler = BlockingScheduler(misfire_grace_time=60)


def manager():
    # mdSYSU
    scheduler.add_job(send_greetings, 'cron', hour=7, minute=30)
    scheduler.add_job(send_con, 'cron', hour=8, minute=30)
    scheduler.add_job(send_flood, 'cron', hour=21)

    # checkUrl
    # scheduler.add_job(check_url, 'cron', hour='*/4', minute=15)

    # mdTum
    scheduler.add_job(sync_posts, 'cron', hour=6)
    scheduler.add_job(send_post, 'cron', hour='1,7,13,19', day_of_week='0-4')
    scheduler.add_job(send_post, 'cron', hour='1,5,9,13,17,21', day_of_week='5,6')

    # mdDra
    scheduler.add_job(send_news_zh, 'cron', hour='2,8,13,14,15,20', minute=1)
    scheduler.add_job(send_news_en, 'cron', hour='2,8,13,14,15,20', minute=2)

    # mdBackup
    scheduler.add_job(do_backup, 'cron', day_of_week='sat', hour=2)

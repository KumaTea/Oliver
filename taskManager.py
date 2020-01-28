from apscheduler.schedulers.blocking import BlockingScheduler
from mdTum import sync_posts, send_post
from mdDra import send_news_all
from mdHostCmd import do_backup


scheduler = BlockingScheduler(misfire_grace_time=60)


def manager():
    # mdTum
    scheduler.add_job(sync_posts, 'cron', hour='6,18')
    scheduler.add_job(send_post, 'cron', hour='1,7,13,19')

    # mdDra
    scheduler.add_job(send_news_all, 'cron', hour='2,8,13,14,15,20', minute=1)
    # mdHostCommands
    scheduler.add_job(do_backup, 'cron', day_of_week='sat', hour=2)

from mdDra import send_news
from mdTum import sync_posts, send_post
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(misfire_grace_time=60)

available_tasks = [
    'sync_posts', 'send_post',
    'send_news',
    'do_backup'
]


def manager():
    # mdTum
    scheduler.add_job(sync_posts, 'cron', hour='0,6,12,18')
    scheduler.add_job(send_post, 'cron', hour='1,7,13,19')

    # mdDra
    scheduler.add_job(send_news, 'cron', hour='14', minute=1)

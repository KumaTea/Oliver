from taskManager import *
from datetime import datetime


def starting_tasks(filename='start_tasks.txt'):
    i = 0
    with open(filename, 'r') as f:
        tasks = f.read().split('\n')
    if 'send_greetings' in tasks:
        send_greetings()
        i += 1
    if 'send_flood' in tasks:
        send_flood()
        i += 1
    if 'send_con' in tasks:
        send_con()
        i += 1
    if 'task_check' in tasks:
        task_check()
        i += 1
    if 'sync_posts' in tasks:
        sync_posts()
        i += 1
    if 'send_post' in tasks:
        send_post()
        i += 1
    if 'do_backup' in tasks:
        do_backup()
        i += 1
    with open(filename, 'w') as f:
        f.write('')
    return True if i > 0 else None


def task_done(task=None):
    current = datetime.now()
    year = current.strftime('%Y')
    month = current.strftime('%m')
    day = current.strftime('%d')
    hour = current.strftime('%H')
    minute = current.strftime('%M')
    task = (lambda p: f'{p} ' if p else '')(task)
    msg = f'Task {task}done at {year}-{month}-{day} {hour}:{minute}.'
    print(msg)

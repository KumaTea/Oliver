import os
from taskManager import *
from tgapi.tools import set_proxy


def mkdir(folder=None):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('tum'):
        os.mkdir('tum')
    if not os.path.exists('dra'):
        os.mkdir('dra')
    if not os.path.exists('../vote'):
        os.mkdir('../vote')
    if folder:
        if type(folder) == list or type(folder) == tuple:
            for items in folder:
                if not os.path.exists(str(items)):
                    os.mkdir(str(items))
        else:
            os.mkdir(str(folder))


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


def starting():
    mkdir()
    set_proxy(port='10080')
    starting_tasks()
    print('Starting fine.')

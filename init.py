import os
import taskManager
from tgapi.tools import set_proxy


available_tasks = [
    'send_greetings', 'send_flood', 'send_con',
    'task_check', 'sync_posts', 'send_post',
    'send_news_zh', 'send_news_en',
    'do_backup'
]


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
    remain = ''
    with open(filename, 'r') as f:
        tasks = f.read().split('\n')
    for item in tasks:
        if item in available_tasks:
            getattr(taskManager, item)()
        else:
            if not item == '':
                print(f'Unavailable task: {item}')
                remain += f'{item}\n'
    with open(filename, 'w') as f:
        f.write(remain)
    return True


def starting():
    mkdir()
    set_proxy(port='10080')
    starting_tasks()
    print('Starting fine.')

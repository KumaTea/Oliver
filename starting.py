import os
import taskManager


def mkdir(folder=None):
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
            if not os.path.exists(str(folder)):
                os.mkdir(str(folder))


def starting_tasks(filename='start_tasks.txt'):
    remain = ''
    with open(filename, 'r') as f:
        tasks = f.read().split('\n')
    for item in tasks:
        if item in taskManager.available_tasks:
            getattr(taskManager, item)()
        else:
            if not item == '':
                print(f'Unavailable task: {item}')
                remain += f'{item}\n'
    with open(filename, 'w') as f:
        f.write(remain)
    return True


def starting():
    starting_tasks()
    print('[info] Starting fine.')

import os
from tools import starting_tasks
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


def starting():
    mkdir()
    set_proxy(port='10080')
    starting_tasks()
    print('Starting fine.')

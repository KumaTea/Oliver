import tgapi
from datetime import datetime
import requests


kuma = tgapi.bot(781791363)
dra = tgapi.bot(852069393)

no_proxy = requests.session()
no_proxy.trust_env = False


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

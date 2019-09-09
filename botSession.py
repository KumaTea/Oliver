import tgapi
from datetime import datetime


kuma = tgapi.bot(781791363)
dra = tgapi.bot(852069393)


def task_done(task=None):
    current = datetime.now()
    year = current.strftime('%Y')
    month = current.strftime('%m')
    day = current.strftime('%d')
    hour = current.strftime('%H')
    minute = current.strftime('%M')
    if task:
        msg = f'Task {task} done at {year}-{month}-{day} {hour}:{minute}.'
    else:
        msg = f'Task done at {year}-{month}-{day} {hour}:{minute}.'
    print(msg)

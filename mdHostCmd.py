import localDB
from botSession import kuma
from tools import task_done
from datetime import datetime
try:
    from botDb import vote_dir
except ImportError:
    vote_dir = '../vote'


def do_backup():
    year, month, date = datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')
    vote = f'{vote_dir}/vote.json'
    tum = 'tum/posts'
    kuma.send(localDB.chat['me']).file(vote, upload=True)
    kuma.send(localDB.chat['me']).file(tum, upload=True)
    kuma.send(localDB.chat['me']).message(f'Backup files on {year}-{month}-{date}')
    task_done('backup')
    return True

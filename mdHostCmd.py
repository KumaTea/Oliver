import localDB
from botSession import kuma
from botTools import task_done
from datetime import datetime


def do_backup():
    year, month, date = datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')
    with open('../vote/vote.json', 'rb') as f:
        kuma.send_document(localDB.chat['me'], f)
    with open('tum/posts.p', 'rb') as f:
        kuma.send_document(localDB.chat['me'], f)
    kuma.send(localDB.chat['me']).message(f'Backup files on {year}-{month}-{date}')
    task_done('backup')
    return True

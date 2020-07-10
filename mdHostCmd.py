import localDB
import subprocess
from botSession import kuma
from botTools import task_done
from datetime import datetime


def do_backup():
    year, month, date = datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')
    subprocess.run(['zip', '-r', '-9', f'{localDB.home_dir}/backup/{year}{month}{date}.zip',
                    f'{localDB.home_dir}/Oliver/tum', f'{localDB.home_dir}/Dragalia/life',
                    f'{localDB.home_dir}/vote'])
    with open(f'{localDB.home_dir}/backup/{year}{month}{date}.zip', 'rb') as f:
        kuma.send_document(localDB.chat['me'], f)
    kuma.send_message(localDB.chat['me'], f'Backup files on {year}-{month}-{date}')
    return task_done('backup')

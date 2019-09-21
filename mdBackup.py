import sys
import subprocess
import localDB
from datetime import datetime
from botSession import kuma
from tools import task_done


def do_backup():
    p = subprocess.Popen(['powershell.exe', 'C:/Users/Administrator/Documents/Oliver/backup.ps1'],
                         stdout=sys.stdout)
    p.communicate()
    year, month, date = datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d')
    filepath = f'D:/FS/Backup/{year}{month}{date}.zip'
    kuma.send(localDB.chat['me']).file(filepath, upload=True)
    task_done('backup')
    return True

import requests
from botSession import kuma
import localDB


def check_kw(url, keyword, exists=True):
    resp = requests.get(url).text
    kw_exist = resp.find(keyword)
    if exists:
        if kw_exist == -1:
            return False
        else:
            return True
    else:
        if kw_exist == -1:
            return True
        else:
            return False


def send_notify(result, url=None):
    msg = 'URL checked success!'
    if url:
        msg += f'\n{url}'
    if result:
        global version
        kuma.send(localDB.chat['me']).message(msg)
        version = str(float(version) + 0.01)
        with open('local_lol_ver.txt', 'w') as new_ver:
            new_ver.write(version)


lol_url = "http://lol.qq.com/download.shtml"
with open('local_lol_ver.txt', 'r') as ver:
    version = ver.read()


def task_check():
    send_notify(check_kw(lol_url, version, True), f'{lol_url}\n{str(float(version) - 0.01)}')

import requests
from botSession import kuma
from tools import task_done
import localDB


def check_kw(url, keyword, exists=True):
    resp = requests.get(url).text
    keyword = list(keyword)
    for item in keyword:
        kw_exist = resp.find(item)
        if exists:
            if not kw_exist == -1:
                return True
        else:
            if kw_exist == -1:
                return True

    return False


def send_notify(result, url=None):
    msg = 'URL checked success!'
    if url:
        msg += f'\n{url}'
    if result:
        global version
        kuma.send(localDB.chat['me']).message(msg)
        for item in range(len(version)):
            version[item] = str(float(version[item]) + 0.01)
        version = '\n'.join(version)
        with open('local_lol_ver.txt', 'w') as new_ver:
            new_ver.write(version)


lol_url = "http://lol.qq.com/download.shtml"
# lol_js = 'http://lol.qq.com/act/AutoCMS/publish/LOLWeb/OfficialWebsite/website_cfg.js'
with open('local_lol_ver.txt', 'r') as ver:
    version = ver.read().split('\n')
if '' in version:
    version.remove('')


def task_check():
    send_notify(check_kw(lol_url, version, True), f'{lol_url}\n{version[0]}')
    task_done('checkUrl')

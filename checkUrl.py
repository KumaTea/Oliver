from botSession import kuma, no_proxy
from tools import task_done
import localDB


def check_kw(url, kw, exists=True):
    resp = no_proxy.get(url)
    resp.encoding = resp.apparent_encoding
    web_content = resp.text
    kw_exist = web_content.find(kw)
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
        kuma.send(localDB.chat['me']).message(msg)


def check_url():
    with open('url/url.txt', 'r') as f1:
        url_list = (lambda p: p.remove('') if '' in p else p)(f1.read().split('\n'))
    with open('url/keyword.txt', 'r', encoding='utf-8') as f2:
        keyword = (lambda p: p.remove('') if '' in p else p)(f2.read().split('\n'))
    changed = False

    for i in range(len(url_list)):
        result = check_kw(url_list[i], keyword[i], True)
        send_notify(result, f'{url_list[i]}\n{keyword[i]}')
        if result:
            try:
                keyword[i] = str(float(keyword[i]) + 0.01)
                changed = True
            except ValueError:
                del url_list[i]
                del keyword[i]
                changed = True

    if changed:
        with open('url/url.txt', 'w') as f1:
            f1.write('\n'.join(url_list))
        with open('url/keyword.txt', 'w', encoding='utf-8') as f2:
            f2.write('\n'.join(keyword))
    task_done('checkUrl')

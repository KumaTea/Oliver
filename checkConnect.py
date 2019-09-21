from subprocess import check_output, CalledProcessError
from botSession import no_proxy


def check_con(url, pro='default', url_type=None):
    if str(pro) == '4':
        suffix = ' -4'
    elif str(pro) == '6':
        suffix = ' -6'
    else:
        suffix = ''
    command = f'ping {url}{suffix}'
    if url.replace('.', '').isdigit() or url.count(':') > 1 or url_type == 'ip':
        try:
            check_output(command)
            return True
        except CalledProcessError:
            return False
    else:
        if 'http' not in url:
            url = f'http://{url}'
        try:
            no_proxy.get(url, timeout=5)
            return True
        except:
            return False

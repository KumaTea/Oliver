import os


def mkdir(folder=None):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('../vote'):
        os.mkdir('../vote')
    if folder:
        if type(folder) == list or type(folder) == tuple:
            for items in folder:
                if not os.path.exists(str(items)):
                    os.mkdir(str(items))
        else:
            os.mkdir(str(folder))


def set_proxy(ip='127.0.0.1', port='1080', protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy


def starting():
    mkdir()
    set_proxy(port='1080')
    print('Starting fine.')

import base64
from datetime import datetime


def task_done(task=None):
    current = datetime.now()
    year = current.strftime('%Y')
    month = current.strftime('%m')
    day = current.strftime('%d')
    hour = current.strftime('%H')
    minute = current.strftime('%M')
    task = (lambda p: f'{p} ' if p else '')(task)
    msg = f'Task {task}done at {year}-{month}-{day} {hour}:{minute}.'
    print(msg)


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def write_file(content, filename, encrypt=False):
    if encrypt:
        with open(filename, 'wb') as f:
            f.write(base64.b64encode(content.encode('utf-8')))
        return True
    else:
        with open(filename, 'w') as f:
            f.write(content)
        return True


def query_token(token_id=None):
    return read_file(f'token_{token_id}', True)


"""
def set_proxy(ip='127.0.0.1', port='1080', protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
"""

from subprocess import check_output, CalledProcessError


def check_con(url, pro='default'):
    if str(pro) == '4':
        suffix = ' -4'
    elif str(pro) == '6':
        suffix = ' -6'
    else:
        suffix = ''
    command = f'ping {url}{suffix}'
    try:
        check_output(command)
        return True
    except CalledProcessError:
        return False

import subprocess
import mdWeather
from botSession import kuma
import token_db
import random

SYSU = ['中山大学', '中大', '中带', '双鸭山', '鸭大', '鸭鸭山', '双倍多多鸭', ]
student = ['学生', '学子', '大佬', '带佬', '高雅人士', '大手子', ]
greet_msg = ['快出来高强度水群', '学习使恁快乐', '憋睡辣', '高雅人士早就醒力', '起来批判一番']
greet_sticker = ['CAADBQADZQMAAtrNfQNfdW_Fq9VLjBYE', 'CAADBQADVgEAArL6ew4JTyVTbRYQlBYE',
                 'CAADBQADRQEAArL6ew6aNvPHLuAFDRYE', 'CAADBQADHAIAArL6ew7w7ukRYBfgERYE',
                 'CAADAQADOwEAAjg9ixwrtVwD8eJ00hYE', 'CAADAQAD_wADOD2LHOJSQakxlemCFgQ',
                 'CAADBQADRAEAArL6ew7rEnfWOPQ_dhYE', 'CAADBQADEgADpc1iJrCMCke01ilSFgQ',
                 ]


def check_connection(url):
    try:
        subprocess.check_output(f'ping {url}')
    except subprocess.CalledProcessError:
        return False

    return True


# TASKS


def send_flood():
    result = mdWeather.weather_status()
    if result == 0:
        flood_msg = '今天双鸭山大学可能淹水了'
    elif result == 1:
        flood_msg = '今天中大淹水了'
    else:
        flood_msg = '今天中大没有淹水'

    kuma.send(token_db.chat['ooxx']).text(flood_msg)
    return True


def send_greetings():
    temp, temp_max, weather_desc = mdWeather.check_forecast()
    grt_msg = f'各位{random.choice(SYSU)}的{random.choice(student)}早上好！\n' \
              f'今日{weather_desc}，{temp}~{temp_max}度。\n\n' \
              f'{random.choice(greet_msg)}，，，'

    kuma.send(token_db.chat['sbddy']).text(grt_msg)
    kuma.send(token_db.chat['sbddy']).sticker(random.choice(greet_sticker))
    return True

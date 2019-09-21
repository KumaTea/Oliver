from checkConnect import check_con
import mdWeather
from botSession import kuma
from tools import task_done
import localDB
import random

SYSU = ['中山大学', '中大', '中带', '双鸭山', '鸭大', '鸭鸭山', '双倍多多鸭', ]
student = ['学生', '学子', '大佬', '带佬', '高雅人士', '大手子', ]
greet_msg = ['快出来高强度水群', '学习使恁快乐', '憋睡辣', '高雅人士早就醒力', '起来批判一番']
greet_sticker = ['CAADBQADZQMAAtrNfQNfdW_Fq9VLjBYE', 'CAADBQADVgEAArL6ew4JTyVTbRYQlBYE',
                 'CAADBQADRQEAArL6ew6aNvPHLuAFDRYE', 'CAADBQADHAIAArL6ew7w7ukRYBfgERYE',
                 'CAADAQADOwEAAjg9ixwrtVwD8eJ00hYE', 'CAADAQAD_wADOD2LHOJSQakxlemCFgQ',
                 'CAADBQADRAEAArL6ew7rEnfWOPQ_dhYE', 'CAADBQADEgADpc1iJrCMCke01ilSFgQ',
                 ]

Guangzhou_code = 101280101
Zhuhai_code = 101280701
Shenzhen_code = 101280601

dow_cn = {
    0: '一',
    1: '二',
    2: '三',
    3: '四',
    4: '五',
    5: '六',
    6: '天',
}

urls = {
    'google': 'https://www.google.com',
    'tg': '2001:b28:f23f:f005::a',
    'zhwp': 'https://zh.wikipedia.org',
    'enwp': 'https://en.wikipedia.org',
    'fb': 'https://www.facebook.com',
    'twi': 'https://twitter.com',
    'ins': 'https://www.instagram.com'
}


def emoji(result):
    return '✅' if result else '❌'


# TASKS


def send_flood():
    result = mdWeather.weather_status()
    if result == 0:
        flood_msg = '今天双鸭山大学可能淹水了'
    elif result == 1:
        flood_msg = '今天中大淹水了'
    else:
        flood_msg = '今天中大没有淹水'

    kuma.send(localDB.chat['ooxx']).text(flood_msg)
    task_done('checkFlood')
    return True


def send_greetings():
    g_temp, g_temp_max, g_weather_desc = mdWeather.check_forecast(Guangzhou_code)
    z_temp, z_temp_max, z_weather_desc = mdWeather.check_forecast(Zhuhai_code)
    s_temp, s_temp_max, s_weather_desc = mdWeather.check_forecast(Shenzhen_code)
    month, day, weekday = mdWeather.check_date()
    lunar_month, lunar_day, lunar_term = mdWeather.check_lunar()
    grt_msg = f'各位{random.choice(SYSU)}的{random.choice(student)}早上好！' \
              f'今天是{month}月{day}日星期{dow_cn[weekday]}，农历{lunar_month}月{lunar_day}{lunar_term}。\n' \
              f'广州{g_weather_desc}，{g_temp}~{g_temp_max}度；' \
              f'珠海{z_weather_desc}，{z_temp}~{z_temp_max}度；' \
              f'深圳{s_weather_desc}，{s_temp}~{s_temp_max}度。\n\n' \
              f'{random.choice(greet_msg)}，，，'

    kuma.send(localDB.chat['sbddy']).text(grt_msg)
    kuma.send(localDB.chat['sbddy']).sticker(random.choice(greet_sticker))
    task_done('greetings')
    return True


def send_con():
    month, day, weekday = mdWeather.check_date()
    res_g_4 = emoji(check_con(urls['google'], '4'))
    g_6_status = check_con(urls['google'], '6')
    res_g_6 = emoji(g_6_status)
    enwp_status = check_con(urls['enwp'], '4') or check_con(urls['enwp'], '6')
    res_enwp = emoji(enwp_status)
    res_zhwp = emoji(check_con(urls['zhwp'], '4') or check_con(urls['zhwp'], '6'))
    res_fb = emoji(check_con(urls['fb'], '4') or check_con(urls['fb'], '6'))
    res_twi = emoji(check_con(urls['twi'], '4') or check_con(urls['twi'], '6'))
    res_ins = emoji(check_con(urls['ins'], '4') or check_con(urls['ins'], '6'))
    tg_status = check_con(urls['tg'])
    res_tg = emoji(tg_status)
    con_msg = f'中大校园网连通性报告\n' \
              f'2019年{month}月{day}日\n\n' \
              f'Google: v4 {res_g_4}  v6 {res_g_6}\n' \
              f'Telegram: {res_tg}\n' \
              f'Wikipedia: en {res_enwp}  zh {res_zhwp}\n' \
              f'SNS: FB {res_fb}  Twi {res_twi}  ins {res_ins}\n' \
              f'（注：技术升级为GET结果）'

    kuma.send(localDB.chat['sbddy']).message(con_msg)
    if not tg_status or not g_6_status or not enwp_status:
        kuma.send(localDB.chat['sbddy']).sticker('CAADBQADEgADpc1iJrCMCke01ilSFgQ')
    task_done('net con')
    return True

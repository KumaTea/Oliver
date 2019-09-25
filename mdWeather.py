from botSession import no_proxy
from tgapi import tools
from datetime import datetime
import re
from bs4 import BeautifulSoup


weather_token = tools.read_file('token_weather', 'base64')
current_api = 'https://api.openweathermap.org/data/2.5/weather'
forecast_api = 'http://flash.weather.com.cn/wmaps/xml/guangdong.xml'
lunar_api = 'https://www.sojson.com/open/api/lunar/json.shtml'

weather_id = {'maybe': [210, 211, 212, 311, 312, 313, 314, 321, 502, 503, 504],
              'must': [221, 230, 231, 232, 511, 520, 521, 522, 531],
              }
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.132 Safari/537.36',
}

events = {
    '2019-10-01': '国庆节',
    '2019-10-28': ['期中考试周', '期中考试周到了，祝大家考试顺利！'],
    '2019-11-01': '考试周结束',
    '2019-11-12': '95周年校庆',
    '2020-01-01': '2020年元旦',
    '2020-01-06': ['期末考试周', '期末考试周到了，祝大家考试顺利！'],
    '2020-01-16': '寒假',
    '2020-01-25': '春节',
    '2020-02-08': ['元宵（开学）', '祝大家元宵节快乐！'],
}


def check_current(item='code'):
    weather_data = {
        'appid': weather_token,
        'q': 'Guangzhou',
        'lang': 'zh_cn'
    }
    result = no_proxy.get(current_api, params=weather_data).json()
    if 'code' in item:
        return result['weather'][0]['id']
    elif 'desc' in item:
        return result['weather'][0]['description']


def check_forecast():
    forecast = {}
    result = no_proxy.get(forecast_api)
    result.encoding = result.apparent_encoding
    soup = BeautifulSoup(result.text, features='lxml')
    for item in soup.find_all('city'):
        if item.get('cityname') == '广州':
            forecast['g'] = [item.get('tem2'), item.get('tem1'), item.get('statedetailed')]
        elif item.get('cityname') == '深圳':
            forecast['s'] = [item.get('tem2'), item.get('tem1'), item.get('statedetailed')]
        elif item.get('cityname') == '珠海':
            forecast['z'] = [item.get('tem2'), item.get('tem1'), item.get('statedetailed')]

    return forecast


def weather_status():
    code = check_current()
    if code in weather_id['maybe']:
        return 0
    elif code in weather_id['must']:
        return 1
    else:
        return -1


def check_lunar():
    date_str = str(int(datetime.now().strftime('%d')))
    result = no_proxy.get(lunar_api, headers=headers).json()
    month = result['data']['cnmonth']
    day = result['data']['cnday']
    term = result['data']['jieqi'].get(date_str, '')

    return month, day, term


def check_date():
    return int(datetime.now().strftime('%m')), int(datetime.now().strftime('%d')), datetime.weekday(datetime.now())


def check_event_int():
    for item in events:
        interval = (datetime.fromisoformat(item) - datetime.now()).days
        if interval == 0:
            if type(events[item]) == str:
                return f'{events[item]}快乐！'
            else:
                return events[item][1]
        elif interval > 0:
            if type(events[item]) == str:
                return f'距离{events[item]}还有{interval}天。'
            else:
                return f'距离{events[item][0]}还有{interval}天。'

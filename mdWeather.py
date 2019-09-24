from botSession import no_proxy
from tgapi import tools
from datetime import datetime
import re


weather_token = tools.read_file('token_weather', 'base64')
current_api = 'https://api.openweathermap.org/data/2.5/weather'
forecast_api = 'http://t.weather.sojson.com/api/weather/city/'
lunar_api = 'https://www.sojson.com/open/api/lunar/json.shtml'

weather_id = {'maybe': [210, 211, 212, 311, 312, 313, 314, 321, 502, 503, 504],
              'must': [221, 230, 231, 232, 511, 520, 521, 522, 531],
              }
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.132 Safari/537.36',
}

events = {
    '国庆节': '2019-10-01',
    '期中考试周': '2019-10-28',
    '考试周结束': '2019-11-01',
    '95周年校庆': '2019-11-12',
    '2020年元旦': '2020-01-01',
    '期末考试周': '2020-01-06',
    '寒假': '2020-01-16',
    '春节': '2020-01-25',
    '元宵（开学）': '2020-02-08',
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


def check_forecast(location):
    result = no_proxy.get(f'{forecast_api}{location}').json()
    today = datetime.now().strftime('%d')
    index = 0
    for i in range(len(result['data']['forecast'])):
        if result['data']['forecast'][i]['date'] == today:
            index = i
            break
    low = re.sub(r'\D', '', result['data']['forecast'][index]['low'])
    high = re.sub(r'\D', '', result['data']['forecast'][index]['high'])
    description = result['data']['forecast'][index]['type']

    return low, high, description


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
        interval = (datetime.fromisoformat(events[item]) - datetime.now()).days
        if interval == 0:
            return f'{item}快乐！'
        elif interval > 0:
            return f'距离{item}还有{interval}天。'

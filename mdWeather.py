import requests
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


def check_current(item='code'):
    weather_data = {
        'appid': weather_token,
        'q': 'Guangzhou',
        'lang': 'zh_cn'
    }
    result = requests.get(current_api, params=weather_data).json()
    if 'code' in item:
        return result['weather'][0]['id']
    elif 'desc' in item:
        return result['weather'][0]['description']


def check_forecast(location):
    result = requests.get(f'{forecast_api}{location}').json()
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
    result = requests.get(lunar_api, headers=headers).json()
    month = result['data']['cnmonth']
    day = result['data']['cnday']
    term = result['data']['jieqi'].get(date_str, '')

    return month, day, term


def check_date():
    return int(datetime.now().strftime('%m')), int(datetime.now().strftime('%d')), datetime.weekday(datetime.now())

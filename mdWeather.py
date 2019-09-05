import requests
from tgapi import tools

Guangzhou_code = 1809858
weather_token = tools.read_file('token_weather', 'base64')
current_api = 'https://api.openweathermap.org/data/2.5/weather'
forecast_api = 'https://api.openweathermap.org/data/2.5/forecast'
weather_data = {
    'appid': weather_token,
    'id': Guangzhou_code,
    'lang': 'zh_cn'
}

weather_id = {'maybe': [210, 211, 212, 311, 312, 313, 314, 321, 502, 503, 504],
              'must': [221, 230, 231, 232, 511, 520, 521, 522, 531],
              }


def check_current(item='code'):
    result = requests.get(current_api, params=weather_data).json()
    if 'code' in item:
        return result['weather'][0]['id']
    elif 'desc' in item:
        return result['weather'][0]['description']


def check_forecast(duration=12):
    length = int(int(duration)/3)
    result = requests.get(forecast_api, params=weather_data).json()
    compare = {
        'temp': [],
        'temp_max': [],
        'description': [],
    }
    for i in range(length):
        compare['temp'].append(int(result['list'][i]['main']['temp']-273.15))
        compare['temp_max'].append(int(result['list'][i]['main']['temp_max']-273.15))
        compare['description'].append(result['list'][i]['weather'][0]['description'])
    temp = min(compare['temp'])
    temp_max = max(compare['temp_max'])
    description = max(set(compare['description']), key=compare['description'].count)

    return temp, temp_max, description



def weather_status():
    code = check_current()
    if code in weather_id['maybe']:
        return 0
    elif code in weather_id['must']:
        return 1
    else:
        return -1

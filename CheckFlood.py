import DataIO
import requests
import tgapi

Guangzhou = 1809858
weather_token = DataIO.get_item('token_weather.txt', decode='base64')
weather_api = f'https://api.openweathermap.org/data/2.5/weather?appid={weather_token}&id={Guangzhou}'

weather_id = {'maybe': [210, 211, 212, 311, 312, 313, 314, 321, 502, 503, 504],
              'must': [221, 230, 231, 232, 511, 520, 521, 522, 531]
              }


def check_weather():
    result = requests.get(weather_api).json()
    weather_code = result['weather'][0]['id']
    if weather_code in weather_id['maybe']:
        return 0
    elif weather_code in weather_id['must']:
        return 1
    else:
        return 0


def send_weather():
    result = check_weather()
    if result == 0:
        tgapi.Send(DataIO.channels['ooxx']).text('今天双鸭山大学可能淹水了')
    elif result == 1:
        tgapi.Send(DataIO.channels['ooxx']).text('今天中大淹水了')
    else:
        tgapi.Send(DataIO.channels['ooxx']).text('今天中大没有淹水')

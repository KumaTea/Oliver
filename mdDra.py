import requests
from botSession import dra
from datetime import datetime
from botTools import task_done

dra_api = "https://dragalialost.com/api/index.php"


def get_news_data(lang="zh_cn", priority=None):
    params = {
        "format": "json",
        "type": "information",
        "category_id": 0,
        "action": "information_list",
        "lang": lang,
        "priority_lower_than": priority
    }
    return requests.get(dra_api, params=params).json()


def send_news(lang='zh_cn'):
    news_data = get_news_data(lang)
    news_list = news_data.copy()["data"]["category"]["contents"]
    latest_news = news_list[0]
    time_delta = datetime.now().timestamp() - latest_news['date']
    if time_delta > 3600:
        return dra.send_message(-1001157490282, '感觉真安静啊')


def send_news_all():
    send_news()
    # send_news("en_us")
    task_done("send dra news")

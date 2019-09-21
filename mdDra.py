import requests
from datetime import datetime
from botSession import dra
# from bs4 import BeautifulSoup
# import json
from tools import task_done
import localDB


dra_api = 'https://dragalialost.com/api/index.php'


def send_news():
    sent = None
    try:
        with open('dra/sent.txt', 'r') as file:
            sent = int(file.read())
    except FileNotFoundError:
        pass

    params = {
        'format': 'json',
        'type': 'information',
        'category_id': '0',
        'action': 'information_list',
        'lang': 'zh_cn',
        'priority_lower_than': '',
    }
    news_data = requests.get(dra_api, params=params).json()

    news_list = news_data['data']['category']['contents']
    oldest = int(news_data['data']['category']['priority_lower_than'])
    latest = news_list[0]['priority']

    to_send = []

    if sent:
        for news in news_list:
            cat = news['category_name']
            title = news['title_name']
            date = datetime.fromtimestamp(news['date']).strftime('%m-%d %H:%M')
            article_id = news['article_id']
            priority = news['priority']

            msg = f'【{cat}】  {date}\n' \
                  f'[{title}](https://dragalialost.com/chs/news/detail/{article_id})'

            if priority > sent:
                to_send.insert(0, msg)
            else:
                break

        if sent < oldest:
            params['priority_lower_than'] = oldest
            older_news_data = requests.get(dra_api, params=params).json()
            older_news_list = older_news_data['data']['category']['contents']

            for news in older_news_list:
                cat = news['category_name']
                title = news['title_name']
                date = datetime.fromtimestamp(news['date']).strftime('%m-%d %H:%M')
                article_id = news['article_id']
                priority = news['priority']

                msg = f'【{cat}】  {date}\n' \
                      f'[{title}](https://dragalialost.com/chs/news/detail/{article_id})'

                if priority > sent:
                    to_send.insert(0, msg)
                else:
                    break

    else:
        for news in news_list:
            cat = news['category_name']
            title = news['title_name']
            date = datetime.fromtimestamp(news['date']).strftime('%m-%d %H:%M')
            article_id = news['article_id']

            msg = f'【{cat}】  {date}\n' \
                  f'[{title}](https://dragalialost.com/chs/news/detail/{article_id})'

            to_send.insert(0, msg)

    if not to_send == []:
        for item in to_send:
            dra.send(localDB.chat['me']).message(item, parse='Markdown', no_preview=True)

    with open('dra/sent.txt', 'w') as file:
        file.write(str(latest))

    task_done('send Dra news')
    return True

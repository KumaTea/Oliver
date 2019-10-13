import requests
import localDB
import json
from datetime import datetime
from botSession import dra
from tools import task_done

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


def get_sent_log(lang="zh_cn"):
    try:
        with open(f"dra/{lang}.json", "r") as file:
            try:
                sent = json.load(file)
            except json.decoder.JSONDecodeError:
                sent = False
    except FileNotFoundError:
        sent = False
    return sent


def format_news(raw, lang='zh_cn'):
    cat = raw['category_name']
    title = raw['title_name'].replace('[', ' (').replace(']', ')')
    article_id = raw['article_id']

    if 'zh' in lang:
        date = datetime.fromtimestamp(raw['date']).strftime('%m-%d %H:%M')
        msg = f'【{cat}】  {date}\n' \
              f'[{title}](https://dragalialost.com/chs/news/detail/{article_id})'
    else:
        msg = f'*{cat}*\n' \
              f'[{title}](https://dragalialost.com/en/news/detail/{article_id})'

    return msg


def send_news(lang='zh_cn'):
    sent = get_sent_log(lang)

    news_data = get_news_data(lang)
    news_list = news_data["data"]["category"]["contents"]

    to_send = []

    if sent:
        if sent[0]['title_name'] == news_list[0]['title_name'] and sent[0]['article_id'] == news_list[0]['article_id'] \
                and sent[0]['priority'] == news_list[0]['priority']:
            pass
        else:
            not_found = True
            renew = 0
            with open(f"dra/{lang}.json", "w") as file:
                json.dump(news_list, file)

            while not_found:
                for news in news_list:
                    for old_news in sent:
                        if news['title_name'] == old_news['title_name'] and news['article_id'] == old_news['article_id']:
                            not_found = False
                            break

                    if not not_found:
                        break

                    msg = format_news(news, lang)
                    to_send.append(msg)

                smallest_priority = news_list[-1]['priority']
                news_list = get_news_data(lang, smallest_priority)
                renew += 1
                if renew > 2:
                    not_found = False

    else:
        for news in news_list:
            msg = format_news(news, lang)
            to_send.append(msg)

        with open(f"dra/{lang}.json", "w") as file:
            json.dump(news_list, file)

    if to_send:
        for item in reversed(to_send):
            dra.send(localDB.chat[f'dra_{lang}']).message(item, parse='Markdown', no_preview=True)

    return True


def send_news_all():
    send_news()
    send_news("en_us")
    task_done("send dra news")

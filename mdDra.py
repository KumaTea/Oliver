import requests
import localDB
import json
from datetime import datetime
from botSession import dra
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
    dra_db = {}
    try:
        with open(f"dra/dra.json", "r") as file:
            try:
                dra_db = json.load(file)
                try:
                    sent = dra_db[lang]
                except KeyError:
                    sent = False
            except json.decoder.JSONDecodeError:
                sent = False
    except FileNotFoundError:
        sent = False

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

            dra_db[lang] = news_list
            with open(f"dra/dra.json", "w") as file:
                json.dump(dra_db, file)

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

        dra_db[lang] = news_list
        with open(f"dra/dra.json", "w") as file:
            json.dump(dra_db, file)

    if to_send:
        """
        for item in reversed(to_send):
            return dra.send_message(
                localDB.chat[f'dra_{lang}'], item, parse_mode='Markdown', disable_web_page_preview=True)
        """
        pass
    else:
        if lang == 'zh_cn' and int(datetime.now().strftime('%H')) == 14:
            return dra.send_message(-1001157490282, '感觉真安静啊')
        else:
            return True


def send_news_all():
    send_news()
    # send_news("en_us")
    task_done("send dra news")

import requests
import localDB
from datetime import datetime
from botSession import dra
from tools import task_done

dra_api = "https://dragalialost.com/api/index.php"


def get_news(lang="zh_cn", priority=""):
    params = {
        "format": "json",
        "type": "information",
        "category_id": 0,
        "action": "information_list",
        "lang": lang,
        "priority_lower_than": priority
    }
    return requests.get(dra_api, params=params).json()


def format_news(news, lang="chs"):
    cat = news["category_name"]
    title = news["title_name"].replace("[", " (").replace("]", ")")
    date = datetime.fromtimestamp(news["date"]).strftime("%m-%d %H:%M")
    article_id = news["article_id"]
    return f"*[{cat}]*  {date}\n[{title}](https://dragalialost.com/{lang}/news/detail/{article_id})"


def send_message(msg, lang="zh"):
    dra.send(localDB.chat[f"dra_{lang}"]).message(msg, parse="Markdown", no_preview=True)
    task_done("send Dra news")


def send_news(lang="zh_cn"):
    try:
        with open(f"dra/{lang}.txt") as file:
            try:
                sent = int(file.read())
            except ValueError:
                if file.tell() == 0:
                    task_done("Empty file")
                else:
                    task_done("File not readable or does not contain the news index")
                return False
    except FileNotFoundError:
        task_done("News index file not found")
        return False

    news_data = get_news(lang=lang)
    news_list = news_data["data"]["category"]["contents"]
    oldest = int(news_data["data"]["category"]["priority_lower_than"])
    latest = news_list[0]["priority"]

    while sent < oldest:
        news_data = get_news(lang=lang, priority=oldest)
        news_list.extend(news_data["data"]["category"]["contents"])
        oldest = int(news_data["data"]["category"]["priority_lower_than"])
    for news in reversed(news_list):
        if news["priority"] > sent:
            send_message(format_news(news, "chs" if lang == "zh_cn" else "en"), lang[:2])

    with open(f"dra/{lang}.txt", "w") as file:
        file.write(str(latest))

    return True


def send_news_zh():
    return send_news()


def send_news_en():
    return send_news("en_us")

import requests
from bs4 import BeautifulSoup
from tgapi import tools


blog = 'oudoubleyang.tumblr.com'
tum_api = f'https://api.tumblr.com/v2/blog/{blog}/posts'
params = {
    'api_key': tools.read_file('token_tum', True),
    'before': None
}


def process_photo(raw_post, index=None):
    post = {
        "type": "photo",
        "id": raw_post['id'],
        "time": raw_post['timestamp'],
        "tags": raw_post['tags'],
        "summary": raw_post['summary'],
        "photo": [],
        "link": raw_post['short_url']
    }
    photo_list = []
    for item in raw_post['photos']:
        photo_list.append(raw_post['photos'][item]['original_size']['url'])
    post['photo'] = photo_list
    if index:
        post['index'] = index

    return post


def process_text(raw_post, index=None):
    post = {
        "type": "text",
        "id": raw_post['id'],
        "time": raw_post['timestamp'],
        "tags": raw_post['tags'],
        "summary": raw_post['summary'],
        "photo": [],
        "link": raw_post['short_url']
    }
    photo_list = []
    raw_text = raw_post['body']
    soup = BeautifulSoup(raw_text)
    images = soup.findAll('img')
    for item in images:
        photo_list.append(item['src'])
    post['photo'] = photo_list
    if index:
        post['index'] = index

    return post


def init_ret_posts():
    posts_len = 1
    index = 0

    while posts_len > 0:
        tum_posts = requests.get(tum_api, params=params).json()['response']['posts']
        posts_len = len(tum_posts)

        for item in tum_posts:
            index += 1

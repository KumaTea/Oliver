import json
import time
import pickle
import requests
from botSession import dra
from bs4 import BeautifulSoup
from datetime import datetime
from voteGenerator import create_vote
from botTools import task_done, read_file
from telegram.utils.helpers import escape_markdown
try:
    from localDB import chat, blog
except ImportError:
    chat = {}
    blog = 'example.tumblr.com'

tum_api = f'https://api.tumblr.com/v2/blog/{blog}/posts'


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
        photo_list.append(item['original_size']['url'])
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
    soup = BeautifulSoup(raw_text, features='lxml')
    images = soup.findAll('img')
    for item in images:
        photo_list.append(item['src'])
    post['photo'] = photo_list
    if index:
        post['index'] = index

    return post


def init_ret_posts():
    posts_db = {}
    posts_len = 1
    params = {
        'api_key': read_file('token_tum', True),
        'before': None
    }
    index = requests.get(tum_api, params=params).json()['response']['total_posts']

    while posts_len > 0:
        tum_posts = requests.get(tum_api, params=params).json()['response']
        posts_len = len(tum_posts['posts'])

        for item in tum_posts['posts']:
            if item['type'] == 'photo':
                posts_db[index] = process_photo(item, index)
                # print('Processed: ', item['id'], ' at ', item['date'])
            elif item['type'] == 'text':
                posts_db[index] = process_text(item, index)
                # print('Processed: ', item['id'], ' at ', item['date'])
            else:
                posts_db[index] = json.dumps(item)
                # print('Unknown type: ', item['type'], '\n', json.dumps(item))

            index -= 1

        try:
            params['before'] = tum_posts['posts'][-1]['timestamp'] - 1
        except IndexError:
            break

    return posts_db


def sync_posts():
    need_sync = True
    db_changed = False
    try:
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)
    except FileNotFoundError:
        need_sync = False
        db_changed = True
        tum_posts = init_ret_posts()
        tum_db = {
            'info': {
                'total': len(tum_posts),
                'sent': 0,
            },
            'posts': tum_posts
        }

    if need_sync:
        params = {
            'api_key': read_file('token_tum', True),
            'before': None
        }
        tum_posts = requests.get(tum_api, params=params).json()['response']
        local_count = tum_db['info']['total']
        local_latest = tum_db['posts'][local_count]['id']
        # online_count = tum_posts['total_posts']
        online_latest = tum_posts['posts'][0]['id']
        if local_latest < online_latest:
            db_changed = True
            new_count = 0
            while not tum_posts['posts'][new_count]['id'] == local_latest:
                new_count += 1
            for i in range(new_count):
                index = local_count+new_count-i
                if tum_posts['posts'][i]['type'] == 'photo':
                    tum_db['posts'][index] = process_photo(tum_posts['posts'][i], index)
                    print('  Processed: ', tum_posts['posts'][i]['id'], ' at ', tum_posts['posts'][i]['date'])
                elif tum_posts['posts'][i]['type'] == 'text':
                    tum_db['posts'][index] = process_text(tum_posts['posts'][i], index)
                    print('  Processed: ', tum_posts['posts'][i]['id'], ' at ', tum_posts['posts'][i]['date'])
                else:
                    tum_db['posts'][index] = tum_posts['posts'][i]
                    print('  Unknown type: ', tum_posts['posts'][i]['type'], '\n', json.dumps(tum_posts['posts'][i]))

        tum_db['info']['total'] = len(tum_db['posts'])

    if db_changed:
        tum_db['posts'] = dict(sorted(tum_db['posts'].items()))

        with open('tum/posts.p', 'wb') as file:
            pickle.dump(tum_db, file, protocol=4)
        with open('tum/posts.json', 'w') as file:
            json.dump(tum_db, file)

        task_done('sync')
        return True
    else:
        return None


def skip_sending(sent, total, schedule=None, base=25):
    if schedule is None:
        schedule = [1, 7, 13, 19]
    now = int(datetime.now().strftime('%H'))
    diff = total - sent

    if now in schedule:
        if diff < base:
            return False if now == schedule[0] else True
        elif diff < base * 2:
            return False if now in schedule[:2] else True
        elif diff < base * 3:
            return False if now in schedule[:3] else True
        else:
            return False
    else:
        return False


def send_post():
    try:
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)
    except FileNotFoundError:
        sync_posts()
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)

    if not tum_db['info']['sent'] == tum_db['info']['total']:
        if skip_sending(tum_db['info']['sent'], tum_db['info']['total']):
            return 'Skipped'
        to_send = tum_db['info']['sent'] + 1
        skip = True
        while skip:
            if 'skip' in tum_db['posts'][to_send]['tags'] or 'wallpaper' in tum_db['posts'][to_send]['tags']:
                to_send += 1
            else:
                skip = False
        if 'first' in tum_db['posts'][to_send]['tags']:
            sending = [tum_db['posts'][to_send]['photo'][0]]
        elif 'last' in tum_db['posts'][to_send]['tags']:
            sending = [tum_db['posts'][to_send]['photo'][-1]]
        else:
            sending = tum_db['posts'][to_send]['photo']
        for item in sending:
            try:
                if item.endswith('gif'):
                    dra.send_animation(chat['st'], item, timeout=60)
                else:
                    dra.send_photo(chat['st'], item, timeout=60)
            except:
                time.sleep(10)

        post_desc = tum_db['posts'][to_send]['summary']
        post_link = tum_db['posts'][to_send]['link']
        tag = ''
        if 'NSFW' in tum_db['posts'][to_send]['tags']:
            tag = 'Tags: #NSFW\n'
        msg = f'Index: {to_send}\n' \
              f'Description: {escape_markdown(post_desc)}\n' \
              f'{tag}Link: [click me]({post_link})'
        vote_id, vote_markup = create_vote(['😍', '👍', '👎'])
        dra.send_message(chat['st'], msg, 'Markdown', True, reply_markup=vote_markup)

        tum_db['info']['sent'] = to_send
        tum_db['posts'][to_send]['vote'] = vote_id
        with open('tum/posts.p', 'wb') as file:
            pickle.dump(tum_db, file, protocol=4)

    task_done('send post')
    return True

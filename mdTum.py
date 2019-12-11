import requests
from bs4 import BeautifulSoup
import json
import re
import pickle
import localDB
from botSession import dra
from botTools import task_done, read_file
from voteGenerator import create_vote


blog = 'oudoubleyang.tumblr.com'
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
    try:
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)
    except FileNotFoundError:
        need_sync = False
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
        current_count = tum_db['info']['total']
        latest_count = tum_posts['total_posts']
        if current_count < latest_count:
            index = latest_count
            for i in range(latest_count - current_count):
                if tum_posts['posts'][i]['type'] == 'photo':
                    tum_db['posts'][index] = process_photo(tum_posts['posts'][i], index)
                    print('  Processed: ', tum_posts['posts'][i]['id'], ' at ', tum_posts['posts'][i]['date'])
                elif tum_posts['posts'][i]['type'] == 'text':
                    tum_db['posts'][index] = process_text(tum_posts['posts'][i], index)
                    print('  Processed: ', tum_posts['posts'][i]['id'], ' at ', tum_posts['posts'][i]['date'])
                else:
                    tum_db['posts'][index] = json.dumps(tum_posts['posts'][i])
                    print('  Unknown type: ', tum_posts['posts'][i]['type'], '\n', json.dumps(tum_posts['posts'][i]))
                index -= 1

        tum_db['info']['total'] = latest_count

    tum_db['posts'] = dict(sorted(tum_db['posts'].items()))

    with open('tum/posts.p', 'wb') as file:
        pickle.dump(tum_db, file, protocol=4)
    with open('tum/posts.json', 'w') as file:
        json.dump(tum_db, file)

    task_done('sync')
    return True


def desc_format(desc):
    re_url = re.sub(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'[\g<0>]', desc)
    in_url = False
    esc_desc = ''
    for i in re_url:
        if i == '[':
            in_url = True
            esc_desc += i
        elif i == ']':
            in_url = False
            esc_desc += i
        elif i == '_' or i == '*':
            if in_url:
                esc_desc += i
            else:
                esc_desc += f'\\{i}'
        else:
            esc_desc += i
    fm_url = (lambda p: p if p else None)(esc_desc.replace('([', '(').replace(')]', ')'))
    return fm_url


def send_post():
    try:
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)
    except FileNotFoundError:
        sync_posts()
        with open('tum/posts.p', 'rb') as file:
            tum_db = pickle.load(file)

    if not tum_db['info']['sent'] == tum_db['info']['total']:
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
            if item.endswith('gif'):
                dra.send_animation(localDB.chat['st'], item)
            else:
                dra.send_photo(localDB.chat['st'], item)

        post_desc = desc_format(tum_db['posts'][to_send]['summary'])
        post_link = tum_db['posts'][to_send]['link']
        tag = ''
        if 'NSFW' in tum_db['posts'][to_send]['tags']:
            tag = 'Tags: #NSFW\n'
        msg = f'Index: {to_send}\n' \
              f'Description: {post_desc}\n' \
              f'{tag}Link: [click me]({post_link})'
        vote_id, vote_markup = create_vote(['😍', '👍', '👎'])
        dra.send(localDB.chat['st']).message(msg, parse='Markdown', no_preview=True, reply_markup=vote_markup)

        tum_db['info']['sent'] = to_send
        tum_db['posts'][to_send]['vote'] = vote_id
        with open('tum/posts.p', 'wb') as file:
            pickle.dump(tum_db, file, protocol=4)

    task_done('send post')
    return True

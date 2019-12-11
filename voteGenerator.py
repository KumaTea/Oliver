import json
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_vote(options, output='all'):
    vote_time = int(time.time())
    vote_id = f'vote{vote_time}'
    if type(options) == tuple:
        options = list(options)
    for i in range(len(options)):
        options[i] = str(options[i])
    vote_json = {
        'info': {
            'id': vote_id,
            'time': vote_time,
            'options': options,
            'participants': 0,
        },
        'options': {},
    }
    for item in options:
        vote_json['options'][item] = []

    with open('../vote/vote.json', 'r') as file:
        vote_data = json.load(file)
    vote_data[vote_id] = vote_json
    with open('../vote/vote.json', 'w') as file:
        json.dump(vote_data, file)

    if 'id' in output:
        return vote_id
    elif 'raw' in output or 'json' in output:
        return vote_json
    elif 'markup' in output:
        return gen_reply_markup(vote_id, options, True)
    else:
        return vote_id, gen_reply_markup(vote_id, options, True)


def gen_reply_markup(vote_id, options=None, new=False, vote_json=None):
    inline_keyboard = [[]]
    if new:
        for item in options:
            button = InlineKeyboardButton(item, callback_data=json.dumps({'id': vote_id, 'e': item}))
            inline_keyboard[0].append(button)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
    else:
        if not vote_json:
            with open('../vote/vote.json', 'r') as file:
                vote_data = json.load(file)
            vote_json = vote_data[vote_id]
        options = vote_json['info']['options']
        for item in options:
            button = InlineKeyboardButton(item + choice_count(len(vote_json['options'][item])),
                                          callback_data=json.dumps({'id': vote_id, 'e': item}))
            inline_keyboard[0].append(button)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
    return reply_markup


def choice_count(count):
    if count > 0:
        return f' - {count}'
    else:
        return ''

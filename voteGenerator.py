import json
import time
try:
    from botDb import vote_dir
except ImportError:
    vote_dir = '../vote'


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

    with open(f'{vote_dir}/vote.json', 'r') as file:
        vote_data = json.load(file)
    vote_data[vote_id] = vote_json
    with open(f'{vote_dir}/vote.json', 'w') as file:
        json.dump(vote_data, file)

    if 'id' in output:
        return vote_id
    elif 'raw' in output or 'json' in output:
        return vote_json
    elif 'markup' in output:
        return gen_reply_markup(vote_id, options, True)
    else:
        return vote_id, gen_reply_markup(vote_id, options, True)


def gen_reply_markup(vote_id, options=None, new=False):
    reply_markup = {
        'inline_keyboard': [[]]
    }
    if new:
        for item in options:
            option_dict = {
                'text': item,
                'callback_data': json.dumps({'id': vote_id, 'e': item})
            }
            reply_markup['inline_keyboard'][0].append(option_dict)
        return reply_markup
    else:
        with open(f'{vote_dir}/vote.json', 'r') as file:
            vote_data = json.load(file)
        vote_json = vote_data[vote_id]
        options = vote_json['info']['options']
        for item in options:
            option_dict = {
                'text': item + choice_count(len(vote_json['options'][item])),
                'callback_data': json.dumps({'id': vote_id, 'e': item})
            }
            reply_markup['inline_keyboard'][0].append(option_dict)
        return reply_markup


def choice_count(count):
    if count > 0:
        return f' - {count}'
    else:
        return ''

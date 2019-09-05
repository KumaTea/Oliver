# VOTE MESSAGE STANDARD

## REPLY MARKUP

```python
reply_markup = {
        'inline_keyboard': [[
            {
                'text': '👍',
                'callback_data': {'id': 'vote_id', 'e': '👍'},
                # better to be: json.dumps({'id': 'test001', 'e': '👍'})
            },
            {
                'text': '👎',
                'callback_data': {'id': 'vote_id', 'e': '👎'},
            }
        ]
        ]
    }
```

## STORAGE

```python
vote_data = {
      "info": {
            "id": "vote_id",
            "time": 1145141919,
            "options": ["A", "B", "C"], 
            "participants": 0
      },
      "options": {
            "A": [], 
            "B": [],
            "C": []
      }
}
```

### TELEGRAM INCOMING UPDATE
```python
update = {
    'update_id': 123456789,
    'callback_query': {
        'id': '123456789123456789',
        'from': {
            'id': 123456789,
            'is_bot': False,
            'first_name': '',
            'last_name': '',
            'username': '',
            'language_code': 'en'
        },
        'message': {
            'message_id': 114,
            'from': {
                'id': 123456789,
                'is_bot': True,
                'first_name': '',
                'username': ''
            },
            'chat': {
                'id': 123456789,
                'first_name': '',
                'last_name': '',
                'username': '',
                'type': 'private'
            },
            'date': 1145141919,
            'text': '123',
            'reply_markup': {
                'inline_keyboard': [
                    [
                        {
                            'text': '😍',
                            'callback_data':
                                '{"id": "test001", "e": \\ud83d\\ude0d"}'
                        },
                        {
                            'text': '🤔',
                            'callback_data':
                                '{"id": "test001", "e": "\\ud83e\\udd14"}'
                        }
                    ]
                ]
            }
        },
        'chat_instance': '2615732782354785246',
        'data':
            '{"id": "test001", "e": "\\ud83e\\udd14"}'
    }
}
```

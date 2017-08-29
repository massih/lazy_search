#!/usr/bin/env python
from __future__ import unicode_literals

import json
import requests
from pprint import pprint
from prompt_toolkit import prompt

STACKOVERFLOW_URL = 'https://api.stackexchange.com/2.2/search/advanced'

def ask_for(search_prompt):
    return prompt(search_prompt)

def print_stuff(data, extra=False):
    print('='*20)
    print('Remaining: {}'.format(data['quota_remaining']))
    print('Items:')
    for item in data['items']:
        print('=========')
        print(item)
        print('=========')
#     print('\n'.join(data['items']))
    if extra:
        print('Extra:')
        print('Has more: {}'.format(data['has_more']))

def api_call(search_text, payload=None):
    payload = payload or {
        'order': 'desc',
        'sort':'activity',
        'site': 'stackoverflow',
        'q': '',
        'accepted': True,
        'body': '',
        'nottagged': '',
        'tagged': '',
        'title': search_text
    }
    response = requests.get(STACKOVERFLOW_URL, params=payload)
    print_stuff(json.loads(response.text))

def main():
    search_text = ask_for('Search: ')
    api_call(search_text)


if __name__ == '__main__':
    main()
    # p = '/2.2/search/advanced?order=desc&sort=activity&accepted=True&answers=3&tagged=redis&title=How do i view my&site=stackoverflow'

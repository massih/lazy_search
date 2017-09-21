#!/usr/bin/env python
from __future__ import unicode_literals

import json
import requests
from prompt_toolkit import prompt

STACKOVERFLOW_URL = 'https://api.stackexchange.com/2.2/search/advanced'


def ask_user(prompt_msg):
    prompt(prompt_msg)


def print_stackoverflow_result(data, extra=False):
    print('=' * 20)
    print('Remaining: {}'.format(data['quota_remaining']))
    print('Items:')
    for item in data['items']:
        print('=========')
        print(item)
        print('=========')
    if extra:
        print('Extra:')
        print('Has more: {}'.format(data['has_more']))


def stackoverflow_call(query):
    payload = {
        'order': 'desc',
        'sort': 'activity',
        'site': 'stackoverflow',
        'q': query,
        'accepted': True,
        'body': '',
        'nottagged': '',
        'tagged': '',
        'title': ''
    }
    return json.loads(requests.get(STACKOVERFLOW_URL, params=payload).text)


def main():
    query = ask_user('Search:')
    response = stackoverflow_call(query)
    print_stackoverflow_result(response)


if __name__ == '__main__':
    main()
    # p = '/2.2/search/advanced?order=desc&sort=activity&accepted=True&answers=3&tagged=redis&title=How do i view my&site=stackoverflow'

#!/usr/bin/env python
from __future__ import unicode_literals

import json
import redis
import requests
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from urllib.parse import urlencode

STACKOVERFLOW_URL = 'https://api.stackexchange.com/2.2/search/advanced'
GOOGLE_API_URL = 'https://www.googleapis.com/customsearch/v1?'
GOOGLE_API_KEY = 'AIzaSyCsvMyihM721N7NeLyXiHDnPL4VuTTUjTk'
GOOGLE_SEARCH_ENGINE_ID = '013660192571711199708:cvztt0fd1vw'
GOOGLE_API_PARAM = {
    'q': '',
    'cx': GOOGLE_SEARCH_ENGINE_ID,
    'key': GOOGLE_API_KEY,
    'num': 10,
    'fields': 'items(title,link,snippet)'
}
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_TTL = 2500


def ask_user(prompt_msg, all_keys):
    suggestion_list = WordCompleter(all_keys)
    return prompt(prompt_msg, completer=suggestion_list)


def save_response(_redis, key, value):
    _redis.set(key, value, ex=2500)


def search_in_cache(_redis, key):
    return _redis.get(key)


def get_all_keys(_redis):
    return _redis.keys()


def create_google_url(text):
    GOOGLE_API_PARAM['q'] = text
    return GOOGLE_API_URL + urlencode(GOOGLE_API_PARAM)


def api_call(text):
    GOOGLE_API_PARAM['q'] = text
    return requests.get(GOOGLE_API_URL, params=GOOGLE_API_PARAM).text


def print_results(results):
    print(results)


def print_stackoverflow_result(data, extra=False):
    print('-' * 20)
    print('Remaining: {}'.format(data['quota_remaining']))
    print('Items:')
    for item in data['items']:
        print('----------')
        print(item)
        print('----------')
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
    _redis = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB, decode_responses=True)
    all_keys = get_all_keys(_redis)
    print(all_keys)
    q = ask_user('Search: ', all_keys)
    response = search_in_cache(_redis, q) or api_call(q)
    save_response(_redis, q, response)
    print_results(response)

    # create_google_url(q)
    # query = ask_user('Search:')
    # response = stackoverflow_call(query)
    # print_stackoverflow_result(response)


if __name__ == '__main__':
    main()

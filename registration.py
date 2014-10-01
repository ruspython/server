import pymysql
import hashlib
import json
import socket
import time
from exceptions import UserAlreadyeExists, InvalidValue



SYMBOLS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A',
           'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
           '2', '3', '4', '5', '6', '7', '8', '9',)

POSSIBLE_FIELDS = ('nickname', 'first_name', 'last_name', 'age',)


def is_user_exists(id):
    conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='messenger')
    cursor = conn.cursor()

    cursor.execute('select user_id from users')

    cursor.close()
    conn.close()

    return id in [id for cur in cursor for id in cur]


def is_name_correct(name):
    for char in name:
        if char not in SYMBOLS:
            return False
    return True


def surround_quotes(the_list):
    new_list = []
    for elem in the_list:
        new_list.append('\'%s\'' % elem)
    return new_list


def register(nickname, passwd, **kwargs):
    conn = pymysql.connect(host='ifmo', unix_socket='/tmp/mysql.sock', user='root', passwd="ajtdmw", db='messenger')
    cursor = conn.cursor()

    args = {}
    args['password'] = hashlib.md5(bytes(passwd, 'utf-8')).hexdigest()
    if is_name_correct(nickname):
        args['nickname'] = nickname

    for key in kwargs:
        if is_name_correct(kwargs[key]) and key in POSSIBLE_FIELDS:
            args[key] = kwargs[key]

    fields = ', '.join(args.keys())
    values = ','.join(surround_quotes(args.values()))

    request = 'insert into users (%s) values (%s)' % (fields, values)
    cursor.execute(request)
    print(request)
    conn.commit()

    cursor.close()
    conn.close()


def json_valid(js):
    if 'password' in js and 'nickname' in js:
        return True
    return False


if __name__ == '__main__':
    f = open('file.json')
    json_obj = json.load(f)
    print(json_valid(json_obj))
    reg_nickname = json_obj['nickname']
    reg_password = json_obj['password']

    print('Free registration')
    sock = socket.socket()
    sock.bind(('178.62.237.133', 7777))
    sock.listen(1)

    while True:
        try:
            conn, addr = sock.accept()

            print('What does that man want -> ?', addr)

            while True:
                time.sleep(1)
                data = conn.recv(1024)
                time.sleep(1)
                if not data:
                    break
                data = data.decode('utf-8')
                if json_valid(data):
                    register(data['user'], passwd=data['password'])
            time.sleep(1)
        finally:
            conn.close()
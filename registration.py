import pymysql
import hashlib
import json
import socket
import time
from socket import error as SocketError
from exceptions import UserAlreadyeExists, InvalidValue



SYMBOLS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A',
           'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
           '2', '3', '4', '5', '6', '7', '8', '9',)

POSSIBLE_FIELDS = ('nickname', 'first_name', 'last_name', 'age',)
POSSIBLE_PORTS = (port for port in range(1000, 2000))

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


def register(nickname, passwd, addr, kwargs):
    conn = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd="ajtdmw", db='messenger')

    cursor = conn.cursor()

    args = {}
    args['password'] = hashlib.md5(bytes(passwd, 'utf-8')).hexdigest()
    if is_name_correct(nickname):
        args['nickname'] = nickname
    args['address'] = addr
    for key in kwargs:
        if is_name_correct(kwargs[key]) and key in POSSIBLE_FIELDS:
            args[key] = kwargs[key]

    cursor.execute('select port from users');
    print([port for port in cursor])

    notallowed_ports = [port for port in cursor]
    for port in POSSIBLE_PORTS:
        if port not in notallowed_ports:
            args['port'] = port
            print('port', args['port'])
            break

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
    print('Free registration')
    sock = socket.socket()
    sock.bind(('178.62.237.133', 7777))
    sock.listen(3)

    while True:
        try:
            conn, addr = sock.accept()

            print('What does that man want -> ', addr)

            while True:
                time.sleep(1)
                data = conn.recv(1024)
                time.sleep(1)
                if not data:
                    break
                data = data.decode('utf-8').replace('\'', '\"')
                f = open('file.json', 'w')
                f.write(data)
                f.close()
                f = open('file.json', 'r')
                try:
                    data = json.load(f)
                except ValueError:
                    break
                finally:
                    f.close()
                if json_valid(data):
                    register(nickname=data['nickname'], passwd=data['password'], addr=addr, kwargs=data)
            time.sleep(1)
        except SocketError:
            pass
        finally:
            conn.close()
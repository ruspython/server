#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from socket import error as SocketError
import json
import pymysql


HOST = '178.62.237.133'


def send_message(message, port):
    sock = socket.socket()
    sock.connect((HOST, int(port)))
    sock.send(bytes(message), 'UTF-8')
    data = sock.recv(1024)
    sock.close()


def main():
    print(socket.gethostname())
    sock = socket.socket()
    client_sock = socket.socket()
    sock.bind((HOST, 6666))
    sock.listen(3)

    while True:
        try:
            conn, addr = sock.accept()

            print('connected:', addr)

            while True:
                data = conn.recv(1024)
                print('data:', data)
                if not data:
                    break

                data = data.decode('utf-8').replace('\'', '\"')
                f = open('file.json', 'w')
                f.write(data)
                f.close()
                f = open('file.json', 'r')
                print('data', data)
                try:
                    data = json.load(f)
                except ValueError:
                    break
                finally:
                    f.close()
                print('data:', data)
                conn = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root',
                                       passwd="ajtdmw", db='messenger')

                cursor = conn.cursor()

                request = 'select port from users where user_id=%d' % int(data['id'])
                print('request', request)
                cursor.execute(request)
                port = [port for port in cursor][0][0]
                print('port:', port)

                client_sock.bind((HOST, port))
                client_sock.listen(5)

                send_message(data['massage'], port)

                print('%s: %s' % (addr, data.decode('UTF-8')))
                conn.send(data)
        except SocketError:
            print('SocketError')
            pass
        # except Exception as e:
        #     print('except', e)
        #     conn.close()
        #     client_sock.close()
        #     exit()


if __name__ == '__main__':
    main()
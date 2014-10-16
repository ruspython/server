#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from socket import error as SocketError
import json
import pymysql
import time
import threading


HOST = '178.62.237.133'


def main():
    print(socket.gethostname())
    sock = socket.socket()
    client_sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, 6666))
    sock.listen(13)

    while True:
        try:
            conn, addr = sock.accept()

            print('connected:', addr)

            #-----------------------
            data = conn.recv(1024)
            print('data:', data)
            if not data:
                break

            data = data.decode('utf-8').replace('\'', '\"')
            # f = open('file.json', 'w')
            # f.write(data)
            # f.close()
            # f = open('file.json', 'r')
            # print('data', data)
            try:
                data = json.dumps(data)
            except ValueError:
                break
            # finally:
            #     f.close()
            print('data:', data)
            conn_mysql = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root',
                                   passwd="ajtdmw", db='messenger')

            cursor = conn_mysql.cursor()

            request = 'select port from users where user_id=%d' % int(data['id'])
            print('request', request)
            cursor.execute(request)
            port = [port for port in cursor][0][0]
            print('port:', port)

            client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_sock.bind((HOST, int(port)))
            client_sock.listen(15)
            print('sending...')

            #print(conn_c, addr_c)
            print('before sending')

            def do():
                while True:
                    port = 10000
                    print('while')
                    great_sock = socket.socket()
                    great_sock.connect((HOST, port))
                    conn_c, addr_c = client_sock.accept()
                    if conn_c:
                        print('connected:', addr_c)
                        try:
                            time.sleep(1)
                            print(data['message'], port, HOST)
                            great_sock.send(bytes(str(data['message']), 'UTF-8'))
                            print('sent: ', data['message']+'\n', 'to port ', port)
                        except Exception as e:
                            print(e)

            th = threading.Thread(target=do)
            th.start()

            print('after sending')

            print(data)
        except SocketError as e:
            print('SocketError', e)
            pass
        except Exception as e:
            print('except', e)
            conn.close()
            #client_sock.close()
            #sock.close()
            exit()


if __name__ == '__main__':
    main()
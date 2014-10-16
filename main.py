#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from socket import error as SocketError
import json
import pymysql
import time
import threading


HOST = '178.62.237.133'

import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


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
            conn_mysql = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root',
                                   passwd="ajtdmw", db='messenger')

            cursor = conn_mysql.cursor()

            request = 'select port from users where user_id=%d' % int(data['id'])
            cursor.execute(request)
            port = int([port for port in cursor][0][0])

            client_server = socketserver.TCPServer((HOST, 10000), MyTCPHandler)
            client_server.serve_forever()

            client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client_sock.bind((HOST, port))
            client_sock.listen(15)
            client_sock.send(bytes(str(data['message']), 'UTF-8'))

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
    PORT = 6666

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
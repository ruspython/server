#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from socket import error as SocketError
import json
import pymysql
import time
import threading
import socketserver


HOST = '178.62.237.133'
MAIN_PORT = 6666


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased


class MyThreads(threading.Thread):
    def __init__(self, port):
        self.server = None;
        self.port = port
        threading.Thread.__init__(self);

    def run(self):
        if self.server == None:
            address = (HOST, self.port);
            self.server = socketserver.TCPServer(address, MyTCPHandler);
        self.server.serve_forever()


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

            # -----------------------
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
            print(data)
            conn_mysql = pymysql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock', user='root',
                                         passwd="ajtdmw", db='messenger')

            cursor = conn_mysql.cursor()

            request = 'select port from users where user_id=%d' % int(data['id'])
            cursor.execute(request)
            client_port = int([port for port in cursor][0][0])
            print(client_port+1)

            my_bytes = bytes(data, 'UTF-8')

            print(my_bytes)

            socket_thread = MyThreads(client_port);
            #socket_thread.setDaemon(True);
            socket_thread.start();

            print('herax')

            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect((HOST, client_port))
            client_sock.send(bytearray(my_bytes))


        except SocketError as e:
            print('SocketError', e)
            pass
        except Exception as e:
            print('except', e)
            conn.close()
            # client_sock.close()
            #sock.close()
            exit()


if __name__ == '__main__':
    main()
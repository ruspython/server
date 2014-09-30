#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import json


def main():
    sock = socket.socket()
    while True:

        sock.connect(('178.62.237.133', 6666))
        f = open('file.json')
        json_obj = json.load(f)

        sock.send(bytes(json_obj, 'UTF-8'))

        data = sock.recv(1024)
        sock.close()

if __name__ == '__main__':
    main()
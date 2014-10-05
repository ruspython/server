#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import json


def main():
    sock = socket.socket()
    while True:

        sock.connect(('178.62.237.133', 10000))

        data = sock.recv(1024)
        print(data)
        sock.close()

if __name__ == '__main__':
    main()
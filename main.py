#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


def main():
    print(socket.gethostname())
    sock = socket.socket()
    sock.bind(('178.62.237.133', 6666))
    sock.listen(1)

    while True:
        try:
            conn, addr = sock.accept()

            print('connected:', addr)

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('%s: %s' % (addr, data.decode('UTF-8')))
                conn.send(data)
        finally:
            conn.close()


if __name__ == '__main__':
    main()
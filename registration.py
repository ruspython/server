import pymysql
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
    conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='messenger')
    cursor = conn.cursor()

    args = {}
    args['password'] = passwd
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


if __name__ == '__main__':
    register('stepanych2', passwd='der_parol', first_name='Ivan2', last_name='Ftoroe2', hren='tot2')

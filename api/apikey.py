#!/usr/bin/env python
# -*- coding:utf-8 -*-
import string
import random
import MySQLdb
import traceback
# from application.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
DATABASE_NAME = 'airewall'  # 仅mysql使用

# 数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "12345678*"


def generate():
    candidates = string.digits+string.ascii_letters
    apikey = ''.join([random.choice(candidates) for i in range(64)])  # apikey
    print(apikey)
    return apikey


def load():
    results = dict()
    fields = ('username', 'apikey', 'num_usable', 'num_day_usable')
    conn = cursor = None
    try:
        conn = MySQLdb.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            db=DATABASE_NAME,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `%s` FROM aire_system_apikey" % ('`, `'.join(fields)))
        _results = cursor.fetchall()
        for item in _results:
            results[item[1]] = dict(zip(fields, item))
    except:
        print(traceback.format_exc())
    finally:
        cursor.close()
        conn.close()
    return results


if __name__ == '__main__':
    # generate()
    print(load())

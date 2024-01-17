#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sqlite3

sql = 'INSERT INTO "TextClassify"."TxtCustom" ("Id", "Text", "TxtCustomTypeId", "RiskLevel", "MatchType", "IsRepeatWords", "IntervalWrods", "CreateTime", "IsDelete") VALUES'
value_template = '({id}, "{keyword}", 13, 2, 0, 0, 0, "2024-01-13 19:21:02", 0)'
keywords = """拔白旗、插红旗
城工部事件
大肃托
第二次整風整社
第二次整风整社
第一次整風整社
第一次整风整社
反AB团
反和平演变
反師道尊嚴運動
反师道尊严运动
反右倾运动
反右傾回潮運動
反右倾回潮运动
反右运动
揭批查运动
坑口事变
农业学大寨运动
批陳整風運動
批陈整风运动
批邓、反击右倾翻案风
批邓反右倾翻案
批林批孔运动
人民公社化运动
三反五反运动
三视教育运动
三忠於四無限运动
三忠于四无限
上山下乡运动
四大（大鸣大放、大字报、大辩论）
四清五反运动
新冠肺炎清零
一打三反运动
真理标准大讨论
整风运动
抓綱治國
抓纲治国""".split('\n')

values = list()
for i in range(len(keywords)):
    values.append(value_template.format(id=86643+1+i, keyword=keywords[i]))

sql += ',\n'.join(values) + ';'
print(sql)


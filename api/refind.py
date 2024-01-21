#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from id_validator import validator


# 大陆居民身份证/港澳居民居住证/台湾居民居住证18位
# 不提取15位大陆居民身份证
idcard_pattern = re.compile(r'\b\d{17}(?:\d|x|X)\b')


def check_idcard(idcard):
    return validator.is_valid(idcard)


def find_idcard(text):
    text = str(text)
    # return [x for x in idcard_pattern.findall(text) if x]
    return [x for x in idcard_pattern.findall(text) if check_idcard(x)]


# https://github.com/VincentSit/ChinaMobilePhoneNumberRegex
phone_pattern = (
    re.compile(r'\b(?:\+?86)?'
               r'1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[235-8]\d{2}|4(?:0\d|1[0-2]|9\d))|9[0-35-9]\d{2}|66\d{2})'
               r'\d{6}\b'))


def find_phone(text):
    text = str(text)
    return phone_pattern.findall(text)


if __name__ == '__main__':
    print(find_phone('13269397627,15247859643'))

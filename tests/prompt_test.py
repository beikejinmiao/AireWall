#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import requests
import pandas as pd

headers = dict()
headers['apikey'] = 'efsBsrVp82K8tDkccYOM1b1wSVPDdXnBTsZKbRVssKyxveUn8u1DrGxAIYzoZZrt'
headers['Content-Type'] = 'application/json'

url = 'https://api.jzatech.com/api/v1/llm/interceptor/prompt/input'


def detect(content):
    while True:
        try:
            time.sleep(0.05)
            resp = requests.post(url, headers=headers, json={'content': content}).json()
        except:
            time.sleep(1)
            continue
        else:
            break
    #
    data = resp.get('data')
    risk_type = 'ERROR'
    if data:
        _risk_types = data.get('risk_types', ())
        if not _risk_types:
            risk_type = 'normal'
        else:
            risk_type = ','.join(_risk_types)
    return risk_type, resp


def prompt_xlsx():
    # excel = pd.read_excel('prompts.xlsx', sheet_name=None)
    # for sheet_name in excel.keys():
    #     df = excel[sheet_name]
    #     print(df.shape)
    df = pd.read_excel('prompts.xlsx', sheet_name=0)
    results = list()
    _detected = dict()
    for content in df['name_correct'].values:
        if content not in _detected:
            risk_type, resp = detect(content)
            results.append(risk_type)
            _detected[content] = (risk_type, resp)
            print(content, risk_type)
        else:
            risk_type, resp = _detected[content]
            results.append(risk_type)
    df['risk_type'] = pd.Series(results)
    df.to_excel("prompts2.xlsx")


def prompt_txt():
    prompts = list()
    with open('prompts.txt', encoding='utf-8') as fopen:
        while True:
            line = fopen.readline()
            if not line:
                break
            line = line.strip()
            prompts.append(line)

    # prompts = list(prompts)
    results = list()
    for content in prompts:
        risk_type, resp = detect(content)
        result = '{content},{msg},{risk_type}'.format(content=content, msg=resp['msg'], risk_type=risk_type)
        results.append(result)
        print(result)

    df = pd.DataFrame(results, columns=['content', 'msg', 'risk_type'])
    df.to_csv('prompt_result.csv', index=False)


if __name__ == '__main__':
    prompt_xlsx()

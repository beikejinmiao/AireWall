#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import requests
import traceback
from flask import Flask
from flask import request, jsonify
import sys
sys.path.insert(0, '/opt/AireWall/python/AireWall/api')
from constant import *
from decode import try_decode
from apikey import load as load_apikey


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class ApiResp(object):
    def __init__(self, code=0, msg='success', data=None):
        self.code = code
        self.msg = msg
        if data is not None:
            self.data = data


class PromptResult(object):
    def __init__(self, decoded=None, risk_level=RiskLevel.BENIGN, risk_score=0.0,
                 risk_types=None, action=RiskAction.PASS, hits=None):
        if decoded:
            self.decoded = decoded
        self.risk_level = risk_level
        self.risk_score = risk_score
        self.action = action
        if risk_types:
            self.risk_types = risk_types
        if hits:
            self.hits = hits


def prompt_detect(text):
    text = text.strip()
    if not text:
        return ApiResp()
    #
    decoded = try_decode(text)
    _decoded_ = re.sub(r'[\x00-\x1F\x7f]+', ' ', text)  # 替换ASCII控制字符后送检
    try:
        result = requests.post('http://localhost:9191/api/v1/text/harmful/locate', json={'txt': _decoded_}).json()
        code = result['code'] if 'code' in result else 0
        msg = result['message'] if 'message' in result else 'success'
        details, contacts = result.get('details', ()), result.get('contacts', ())
        #
        risk_score = 0
        risk_types, hits = set(), list()
        for item in details:
            _type = rtype_map[item.get('riskCode')]
            _text = item.get('text', '')
            if len(_text) <= 1:
                risk_score += 8
            elif _type in (RiskType.POLITIC, RiskType.TERRORISM, RiskType.DRUG):
                risk_score += 32
            else:
                risk_score += 16
            risk_types.add(_type)
            hit = {'risk_type': _type, 'text': item.get('text', ''), 'indices': item.get('position')}
            hits.append(hit)
        for item in contacts:
            _type = rtype_map[item.get('contactType')]
            if _type != RiskType.DEFAULT:
                risk_score += 4
                risk_types.add(_type)
                hit = {'risk_type': _type, 'text': item.get('contactString', ''), 'indices': item.get('position')}
                hits.append(hit)
        #
        if risk_score <= 0:
            risk_level, action = RiskLevel.BENIGN, RiskAction.PASS
        elif risk_score <= 30:
            risk_level, action = RiskLevel.LOW, RiskAction.REJECT
        elif risk_score <= 60:
            risk_level, action = RiskLevel.MEDIUM, RiskAction.REJECT
        elif risk_score <= 90:
            risk_level, action = RiskLevel.HIGH, RiskAction.REJECT
        else:
            risk_level, action = RiskLevel.CRITICAL, RiskAction.REJECT
    except Exception as e:
        print(traceback.format_exc())
        return ApiResp(code=1, msg=str(e))

    return ApiResp(code=code,
                   msg=msg,
                   data=PromptResult(decoded=None if decoded == text else decoded,
                                     risk_level=risk_level, risk_score=min(100, risk_score)/100,
                                     risk_types=list(risk_types), action=action, hits=hits).__dict__
                   )


# with open('index.html', encoding='utf-8') as fopen:
#     homepage = fopen.read()
#
#
# @app.route('/', methods=['GET'])
# def home():
#     return homepage
apikeys = load_apikey()


@app.route('/api/v1/llm/interceptor/prompt/input', methods=['POST'])
def prompt_input():
    try:
        apikey = request.headers.get('apikey')
        if not apikey or apikey not in apikeys:
            resp = ApiResp(code=1, msg='头字段\'apikey\'不存在或\'apikey\'无效')
        # elif apikeys[apikey]['num_usable'] <= 0:
        #     resp = ApiResp(code=1, msg='当前apikey使用额度已耗尽, 请联系管理员购买')
        else:
            params = json.loads(request.data)
            if 'content' not in params:
                resp = ApiResp(code=1, msg='参数字段\'content\'不存在')
            else:
                resp = prompt_detect(str(params['content']))
    except Exception as e:
        resp = ApiResp(code=1, msg=str(e))
    return jsonify(resp.__dict__)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


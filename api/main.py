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
from refind import find_idcard

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
                 risk_class=None, action=RiskAction.PASS, description='未发现风险内容', hits=None):
        if decoded:
            self.decoded = decoded
        self.risk_level = risk_level
        self.risk_score = risk_score
        self.action = action
        self.description = description
        if risk_class:
            self.risk_class = risk_class
        if hits:
            self.hits = hits


def prompt_detect(text, risks=all_risk_class):
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
        risk_class_hits, illegal_hits, privacy_hits = set(), list(), list()
        descriptions = set()
        #
        if len(details) > 0:
            for item in details:
                _type = rtype_map[item.get('riskCode')]
                _text = item.get('text', '')
                # 针对性处理Prompt注入攻击
                if RiskClass.ATTACK in risks and _type == RiskType.OTHER and re.match(r'^(忽略|ignore|forget) ', _text):
                    risk_class_hits.add(RiskClass.ATTACK)
                    descriptions.add('发现Prompt注入攻击')
                    risk_score += 40
                    continue
                #
                if RiskClass.ILLEGAL in risks:
                    if len(_text) <= 1:
                        risk_score += 8
                    elif _type in (RiskType.POLITIC, RiskType.TERRORISM, RiskType.DRUG):
                        risk_score += 32
                    else:
                        risk_score += 16
                    hit = {'risk_type': _type, 'text': item.get('text', ''), 'indices': item.get('position')}
                    risk_class_hits.add(RiskClass.ILLEGAL)
                    illegal_hits.append(hit)
                    descriptions.add('发现非法内容')
        #
        if RiskClass.PRIVACY in risks:
            idcards = find_idcard(text)
            for idcard in idcards:
                privacy_hits.append({'risk_type': RiskType.IDCARD, 'text': idcard})
            for item in contacts:
                _type = rtype_map[item.get('contactType')]
                if _type != RiskType.DEFAULT:
                    risk_score += 4
                    hit = {'risk_type': _type, 'text': item.get('contactString', '')}
                    privacy_hits.append(hit)
                    descriptions.add('发现隐私泄露')
            if len(privacy_hits) > 0:
                risk_class_hits.add(RiskClass.PRIVACY)
        #
        if len(descriptions) > 0:
            description = ';'.join(descriptions)
        else:
            description = '未发现风险内容'
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
                                     risk_class=list(risk_class_hits), action=action,
                                     description=description, hits=illegal_hits+privacy_hits).__dict__
                   )


apikeys = load_apikey()
jdict = lambda resp: jsonify(resp.__dict__)


@app.route('/api/v1/llm/interceptor/prompt/input', methods=['POST'])
def prompt_input():
    try:
        apikey = request.headers.get('apikey')
        if not apikey or apikey not in apikeys:
            return jdict(ApiResp(code=1, msg='头字段\'apikey\'不存在或\'apikey\'无效'))
        # elif apikeys[apikey]['num_usable'] <= 0:
        #     return jdict(ApiResp(code=1, msg='当前apikey使用额度已耗尽, 请联系管理员购买'))
        ##
        params = json.loads(request.data)
        if 'content' not in params:
            return jdict(ApiResp(code=1, msg='参数字段\'content\'不存在'))
        if 'risk' not in params:
            risks = all_risk_class
        else:
            risks = params['risk']
            if not isinstance(risks, list) or len(risks) <= 0:
                return jdict(ApiResp(code=1, msg='参数字段\'risk\'格式或内容错误'))
            for item in set(risks):
                if item not in all_risk_class:
                    return jdict(ApiResp(code=1, msg='参数字段\'risk\'内容错误, 仅支持:illegal,privacy,attack'))
        #
        resp = prompt_detect(str(params['content']), risks=risks)
    except Exception as e:
        resp = ApiResp(code=1, msg=str(e))
    return jdict(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


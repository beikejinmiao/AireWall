#!/usr/bin/env python
# -*- coding:utf-8 -*-
import enum
from collections import defaultdict


class RiskLevel(enum.StrEnum):
    BENIGN = 'benign'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class RiskAction(enum.StrEnum):
    PASS = 'pass'
    REVIEW = 'review'
    REJECT = 'reject'


class RiskTypeO(enum.StrEnum):
    CHAR = 'Char'                 # 非正常字符
    POLITICS = 'Politics'         # 涉政文本
    TERRORISM = 'Terrorism'       # 涉恐文本
    PORN = 'Porn'                 # 涉黄文本
    GAMBLE = 'Gamble'             # 涉赌文本
    DRUG = 'Drug'                 # 涉毒文本
    CONTRABAND = 'Contraband'     # 非法交易
    ABUSE = 'Abuse'               # 辱骂文本
    OTHER = 'Other'               # 推广引诱诈骗
    CUSTOM = 'Custom'             # 自定义敏感词
    #
    ACCOUNT = '1'           # 账号
    EMAIL = '2'             # 邮箱
    WEBSITE = '3'           # 网址
    PHONE = '4'             # 手机号
    QQ = '5'                # QQ号
    WECHAT = '6'            # 微信号
    QQ_GROUP = '7'          # Q群号


class RiskType(enum.StrEnum):
    NORMAL = 'normal'             # 正常
    POLITIC = 'politic'           # 涉政
    TERRORISM = 'terrorism'       # 涉恐
    PORN = 'porn'                 # 涉黄
    GAMBLE = 'gamble'             # 涉赌
    DRUG = 'drug'                 # 涉毒
    CONTRABAND = 'contraband'     # 违禁物品
    ABUSE = 'abuse'               # 辱骂
    CUSTOM = 'custom'             # 自定义敏感词
    OTHER = 'other-harmful'       # 其他(推广引诱诈骗)
    DEFAULT = 'other-harmful'     # 默认
    #
    CREDIT = 'credit'       # 银行卡号
    IDCARD = 'idcard'       # 身份证号
    EMAIL = 'email'         # 邮箱
    PHONE = 'phone'         # 座机/手机号码
    QQ = 'qq'               # QQ号
    WECHAT = 'wechat'       # 微信号


rtype_map = defaultdict(lambda: RiskType.DEFAULT)
rtype_map.update({
    RiskTypeO.CHAR:        RiskType.OTHER,
    RiskTypeO.POLITICS:    RiskType.POLITIC,
    RiskTypeO.TERRORISM:   RiskType.TERRORISM,
    RiskTypeO.PORN:        RiskType.PORN,
    RiskTypeO.GAMBLE:      RiskType.GAMBLE,
    RiskTypeO.DRUG:        RiskType.DRUG,
    RiskTypeO.CONTRABAND:  RiskType.CONTRABAND,
    RiskTypeO.ABUSE:       RiskType.ABUSE,
    RiskTypeO.OTHER:       RiskType.OTHER,
    RiskTypeO.CUSTOM:      RiskType.CUSTOM,
    #
    RiskTypeO.EMAIL:     RiskType.EMAIL,
    RiskTypeO.PHONE:     RiskType.PHONE,
    RiskTypeO.QQ:        RiskType.QQ,
    RiskTypeO.WECHAT:    RiskType.WECHAT,
})

risk_type_cn = {
    RiskType.POLITIC: '涉政',
    RiskType.TERRORISM: '涉恐',
    RiskType.PORN: '涉黄',
    RiskType.GAMBLE: '涉赌',
    RiskType.DRUG: '涉毒',
    RiskType.CONTRABAND: '违禁物品',
    RiskType.ABUSE: '辱骂',
    RiskType.OTHER: '推广引诱诈骗',
    RiskType.CREDIT: '银行卡号',
    RiskType.IDCARD: '身份证号',
    RiskType.EMAIL: '邮箱',
    RiskType.PHONE: '手机号码',
    RiskType.QQ: 'QQ号',
    RiskType.WECHAT: '微信号',
}


class RiskClass(enum.StrEnum):
    ILLEGAL = 'illegal'     # 非法
    PRIVACY = 'privacy'     # 隐私
    ATTACK = 'attack'       # 攻击


all_risk_class = (RiskClass.ILLEGAL, RiskClass.PRIVACY, RiskClass.ATTACK)

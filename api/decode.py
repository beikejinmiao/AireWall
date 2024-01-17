#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from urllib import parse as urlparse
import html
import base64
from regex import maybe_base64


def full2half(text):
    """
    全角字符处理
    :param text:
        # Example:
        # %u0025%u0075%u0066%u0066%u0031%u0063%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065%u0061%u006c%u0065%u0072%u0074%u0028%u0018%u0058%u0053%u0053%u0019%u0029%u003b%u0025%u0075%u0066%u0066%u0031%u0063%u002f%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065
        # %uff1cscript%uff1ealert(XSS);%uff1c/script%uff1e
    :return:
    """
    # http://www.fileformat.info/info/unicode/char/search.htm?q=%3C&preview=entity
    # https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters
    # while True:
    #     _text = text.replace("%u00", "\\u00").replace("%uff", "\\uff")
    #     # 还是有内存泄露情况
    #     _text = str(re.sub(u"[\uff01-\uff60]", lambda x: chr(ord(x.group(0)) - 0xfee0), _text.decode('unicode-escape')))
    #     # unicodedata.normalize方法会造成严重的内存泄露
    #     # _text = str(unicodedata.normalize('NFKC', _text.decode('unicode-escape')))
    #     if _text == text:
    #         break
    #     text = _text
    # return text

    # return str(text.replace("%u00", "\\u00").decode('unicode-escape'))    # memory leak
    return text


def hex_decode(text, charset="utf-8"):
    """
    解析16进制字符串.
    :param text:
    :param charset:
    :return:
    """
    # %u0025%u0075%u0066%u0066%u0031%u0063%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065%u0061%u006c%u0065%u0072%u0074%u0028%u0018%u0058%u0053%u0053%u0019%u0029%u003b%u0025%u0075%u0066%u0066%u0031%u0063%u002f%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065
    # %uff1cscript%uff1ealert(XSS);%uff1c/script%uff1e
    try:
        _text = re.sub(r'(%u00|%uff|\\u00|\\uff|\\x)', '', text)
        return bytes.fromhex(_text).decode(charset)
    except:
        pass
    return text


def base64_decode(content):
    decoded = content
    if maybe_base64(content):
        decoded = base64.b64decode(content)
        _plain_text = re.sub(b'[^\x00-\x7F]+', b'', decoded)
        # base64解码后出现乱码(控制字符/扩展字符) 且占比超过50%, 意味着原始数据不是base64编码
        if len(_plain_text) / len(decoded) < 0.5:
            return content
        decoded = _plain_text.decode("utf-8")   # base64解码后返回类型为bytes
    return decoded


def try_decode(text, charset="utf-8", depth=2):
    """ decode valid content by base64&hex """
    while depth:
        try:
            # /?post=The+Width+of+Soldinafel%3A+%26lt%3Ba+href%3D%22+http%3A%2F%2Ft.co%2FHuLVrdWp+%22%26gt%3Bsildenafil+price%26lt%3B%2Fa%26gt%3B
            # 1. URL decode
            text = urlparse.unquote(text)
            """ 
            html.unescape (https://www.compart.com/en/unicode/U+0045)
            HTML Entity:  &#x45; -->  E  
                          &lt;   -->  <
            """
            # 2. HTML unescape
            text = html.unescape(text)
            # 3. Base64 decode
            text = base64_decode(text)
            # 4.
            text = hex_decode(text, charset=charset)
        except:
            return text
        depth -= 1
    return text


if __name__ == '__main__':
    print(try_decode('?post=The+Width+of+Soldinafel%3A+%26lt%3Ba+href%3D%22+http%3A%2F%2Ft.co%2FHuLVrdWp+%22%26gt%3Bsildenafil+price%26lt%3B%2Fa%26gt%3B'))
    print(try_decode('https://www.baidu.com/s?wd=%E4%B8%80%E5%B9%B4%E7%9A%84%E7%BB%BC%E8%89%BA%E9%87%8C%2C%E6%9C%89%E4%B8%80%E5%B9%B4%E7%9A%84%E5%B9%B4%E8%BD%BB%E4%BA%BA&rsv_spt=1'))
    print(try_decode('%u0025%u0075%u0066%u0066%u0031%u0063%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065%u0061%u006c%u0065%u0072%u0074%u0028%u0018%u0058%u0053%u0053%u0019%u0029%u003b%u0025%u0075%u0066%u0066%u0031%u0063%u002f%u0073%u0063%u0072%u0069%u0070%u0074%u0025%u0075%u0066%u0066%u0031%u0065'))
    print(try_decode('ZnVjayB5b3UgZXZlcnkgZGF5'))



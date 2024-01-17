#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re


base64 = re.compile(r"^([A-Za-z0-9+/]{4})+([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$")


def maybe_base64(text):
    if re.match(r'^([a-zA-Z]*|\d+)$', text):
        return False
    if base64.match(text):
        return True
    return False


if __name__ == '__main__':
    assert maybe_base64('12314') is False
    assert maybe_base64('qwerZXCtyu') is False
    assert maybe_base64('cXdyZXdyMzQyNGRmc2Rm') is True



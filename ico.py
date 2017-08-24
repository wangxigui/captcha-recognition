#!/usr/bin/env python

import requests
import json
import io
import os
import base64
import shutil
import sys
import numpy as py
import string
import time
from PIL import Image, ImageFilter, ImageEnhance
from train import predict

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiIzaWNvLmNvbSIsImlhdCI6MTUwMzU2ODczNywiZXhwIjoxNTAzNTc5NTM3LCJ1aWQiOjY0NTAsInVjb2RlIjoiMTUzMzYiLCJtb2JpbGUiOiIxODYyMDYzOTgwMiIsInJvbGUiOjN9.q26VCCpCwUgggCbIw-YPhOE8WKmTAgZxfMZ_ehy7ysWfMVEk1EBFzuW9FmDB3mMb1BWjXO_UWlxR9k9AKLYcgA',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=5265DCD6DA984361D656BC620423E2F9; Hm_lvt_f899f0c468ac63b3d0db98500652ef7e=1503375354,1503448568; Hm_lpvt_f899f0c468ac63b3d0db98500652ef7e=1503471761',
    'Host': 'www.3ico.com',
    'Origin': 'https://www.3ico.com',
    'Referer': 'https://www.3ico.com/fe/project/16.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',

}

target = os.path.abspath('.') + '/target/target.jpg'

def predict_captcha(captcha_info):
    data = captcha_info.get('captcha')
    im = Image.open(io.BytesIO(base64.b64decode(data)))
    im.save(target)
    return predict(target)

def getCaptcha():
    url = 'https://www.3ico.com/api/assist/captcha'
    res = requests.get(url=url, headers=headers, verify=False)
    return json.loads(res.text)

def format_data(data):
    query_str = []
    for key, val in data.items():
        item = '%s=%s'%(key, val)
        query_str.append(item)
    return '&'.join(query_str)

def main():
    data ={
        'pid': 17,
        'amount': 0.4,
        'captcha': 'a606',
        'captcha_id': '2qb2h2'
    }

    while True:
        captcha_info = getCaptcha()
        captcha = predict_captcha(captcha_info)

        data['captcha_id'] = captcha_info.get('captcha_id')
        data['captcha'] = captcha
        print data

        url = 'https://www.3ico.com/api/user/invest/do?' + format_data(data)
        print url
        res = requests.post(url=url, json=data, headers=headers, verify=False)
        print res.status_code, res.text
        time.sleep(1)
        return

if __name__ == '__main__':
    main()

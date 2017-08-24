# -*- coding: utf-8 -*-

import requests
import json
import string
import time
import io
import base64
import os
import sys
import shutil
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


PROJECT_HOME = os.path.abspath('.')
DATA_HOME = os.path.join(PROJECT_HOME, 'input/ico3')

category_dirs = DATA_HOME + '/category'
cut_dirs = DATA_HOME + '/cut'
train_data_file = DATA_HOME + '/train_data.txt'


def download_captcha():
    url = 'https://www.3ico.com/api/assist/captcha'
    data ={
        'pid': 17,
        'amount': 0.4
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiIzaWNvLmNvbSIsImlhdCI6MTUwMzUzOTE1NCwiZXhwIjoxNTAzNTQ5OTU0LCJ1aWQiOjY0NTAsInVjb2RlIjoiMTUzMzYiLCJtb2JpbGUiOiIxODYyMDYzOTgwMiIsInJvbGUiOjN9.9mwWqShUSFZwRBqli2RMjRhATfPtGm0XtV5biuv77kEvi7o9snO0G0LHUhusUITG5ng7vS358QOCd8CPW5Zgsg',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=5265DCD6DA984361D656BC620423E2F9; Hm_lvt_f899f0c468ac63b3d0db98500652ef7e=1503375354,1503448568; Hm_lpvt_f899f0c468ac63b3d0db98500652ef7e=1503471761',
        'Host': 'www.3ico.com',
        'Origin': 'https://www.3ico.com',
        'Referer': 'https://www.3ico.com/fe/project/16.html',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    res = requests.get(url=url, json=data, headers=headers, verify=False)
    return json.loads(res.text)

def downloading():
    for i in range(100):
        res = download_captcha()
        data = res.get('captcha')
        im = Image.open(io.BytesIO(base64.b64decode(data)))
        f = '%s/%d.jpg'%(DATA_HOME, int(time.time() * 1000000))
        im.save(f)
        cutPictures(f, cut_dirs)
        time.sleep(2)

def segment(im):
    s = 0  # left
    t = 0 # top
    w = 35 # width
    h = 40 # height
    im_new = []

    # first digit
    im1 = im.crop((0, 0, 0+35, 40)) #left, top, right, bottom
    im2 = im.crop((38, 0, 38+35, 40)) #left, top, right, bottom
    im3 = im.crop((78, 0, 78+35, 40)) #left, top, right, bottom
    im4 = im.crop((115, 0, 115+35, 40)) #left, top, right, bottom
    im_new.append(im1)
    im_new.append(im2)
    im_new.append(im3)
    im_new.append(im4)

    #for i in range(4):
    #    im1 = im.crop((s+w*i, t, t+w*(i+1), h))
    #    im_new.append(im1)
    return im_new

def imgTransfer(f_name):
    im = Image.open(f_name)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = im.convert('L')

    return im

def cutPictures(img, dest_dir):
    im = imgTransfer(img)
    pics = segment(im)
    for pic in pics:
        path = dest_dir + '/%s.jpg'%(int(time.time() * 1000000))
        pic.save(path, 'jpeg')

def cuting():
    cutPictures('/home/wxg/blockchain/captcha-recognition/image.jpg', cut_dirs)
    return

    path = DATA_HOME
    for img in os.listdir(path):
        if not img.endswith('.jpg'):
            continue
        img_path = os.path.join(path, img)
        cutPictures(img_path, cut_dirs)


def getBinayPix(im):
    im = Image.open(im)
    img = np.array(im)
    rows, cols = img.shape
    for i in range(rows):
       for j in range(cols):
            if(img[i, j] <= 200):
                img[i, j] = 0
            else:
                img[i, j] = 1
    binpix = np.ravel(img)
    return binpix

def extractFeature():
    words = [w for w in string.lowercase]
    digits = [str(d) for d in range(10)]
    candinate = words + digits
    for cd in candinate:
        digit_dir = os.path.join(category_dirs, cd)
        for f in os.listdir(digit_dir):
            if not f.endswith('.jpg'):
                continue
            f_abs_path = os.path.join(digit_dir, f)
            pixs = getBinayPix(f_abs_path).tolist()
            label = cd
            pixs.append(label)
            pixs = [str(i) for i in pixs ]
            content = ','.join(pixs)

            with open(train_data_file, 'a+') as f:
                f.write(content)
                f.write('\n')
                f.close()

if __name__ == '__main__':
    #downloading()
    extractFeature()

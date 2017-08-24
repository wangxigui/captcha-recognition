# -*- coding: utf-8 -*-

import requests
import time
import os
import sys
import shutil
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from pytesseract import *


PROJECT_HOME = os.path.abspath('.')
DATA_HOME = os.path.join(PROJECT_HOME, 'input/test')

category_dirs = DATA_HOME + '/category'
cut_dirs = DATA_HOME + '/cut'
train_data_file = DATA_HOME + '/train_data.txt'

def downloads_pic(pic_name):
	url = 'http://smart.gzeis.edu.cn:8081/Content/AuthCode.aspx'
	res = requests.get(url, stream=True)
	with open('%s/%s.jpg'%(DATA_HOME, pic_name), 'wb') as f:
		for chunk in res.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
        f.close()

def downloading():
    for i in range(300):
        pic_name = int(time.time() * 1000000)
        downloads_pic(pic_name)

def segment(im):
    s = 9  # hori.. start
    t = 0 # top
    w = 44 # width
    h = 81 # height
    im_new = []
    # first digit

    im1 = im.crop((9, 0, 9+44, 81)) #left, top, right, bottom
    im2 = im.crop((46, 0, 46+44, 81)) #left, top, right, bottom
    im3 = im.crop((91, 0, 91+44, 81)) #left, top, right, bottom
    im4 = im.crop((130, 0, 130+44, 81)) #left, top, right, bottom
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
    #cutPictures('/home/wxg/blockchain/captcha-recognition/input/1503544554541331.jpg')
    #return

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
    #category_dirs = os.path.abspath('.') + '/input/category/'
    #train_data_file = os.path.abspath('.') + '/input/train_data.txt'
    for digit in range(9):
        digit_dir = os.path.join(category_dirs, str(digit))
        for f in os.listdir(digit_dir):
            if not f.endswith('.jpg'):
                continue
            f_abs_path = os.path.join(digit_dir, f)
            pixs = getBinayPix(f_abs_path).tolist()
            label = digit
            pixs.append(label)
            pixs = [str(i) for i in pixs ]
            content = ','.join(pixs)

            with open(train_data_file, 'a+') as f:
                f.write(content)
                f.write('\n')
                f.close()

if __name__ == '__main__':
    #downloading()
    cuting()
    #extractFeature()

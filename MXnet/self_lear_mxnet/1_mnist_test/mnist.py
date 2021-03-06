#!/usr/bin/env python
#-*- coding:utf-8 -*-
import numpy as np
import os
import urllib
import gzip
import struct
##下载数据
def download_data(url, force_download=True):
    fname = url.split("/")[-1]
    if force_download or not os.path.exists(fname):
        urllib.urlretrieve(url,fname)
    return fname
##读取数据
def read_data(label_url, image_url):
    with gzip.open(download_data(label_url))as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        label = np.fromstring(flbl.read(), dtype=np.int8)
    with gzip.open(download_data(image_url),'rb')as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        image = np.fromstring(fimg.read(), dtype=np.uint8).reshape(len(label), rows, cols)
    return (label, image)

path='http://yann.lecun.com/exdb/mnist/'
(train_lbl, train_img)= read_data(
    path+'train-labels-idx1-ubyte.gz', path+'train-images-idx3-ubyte.gz')
(val_lbl, val_img) = read_data(
   path+'t10k-labels-idx1-ubyte.gz', path+'t10k-images-idx3-ubyte.gz')


'''
Title           :make_predictions_1.py
Description     :This script makes predictions using the 1st trained model and generates a submission file.
Author          :Adil Moujahid
Date Created    :20160623
Date Modified   :20160625
version         :0.2
usage           :python make_predictions_1.py
python_version  :2.7.11
'''

import os
import glob
import cv2
import caffe
import lmdb
import numpy as np
from caffe.proto import caffe_pb2

caffe.set_mode_cpu() 

#Size of images
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

'''
Image processing helper function
'''

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img



#Read model architecture and trained model's weights
net = caffe.Net('../models/net12_deploy_def.prototxt',
                '../models/snapshots/net12_iter_1000.caffemodel',
                caffe.TEST)

#Define image transformers
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))

'''
Making predicitions
'''
#Reading image paths
test_img_paths = [img_path for img_path in glob.glob("../input/train/*jpg")]

#Making predictions
test_ids = []
preds = []
# for img_path in test_img_paths:
# for i in range(len(test_img_paths):
for i in range(50):
    img_path = test_img_paths[i] 
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    
    net.blobs['data'].data[...] = transformer.preprocess('data', img)
    out = net.forward()
    pred_probas = out['prob']

    test_ids = test_ids + [img_path.split('/')[-1][:-4]]
    preds = preds + [pred_probas.argmax()]

    print img_path
    print pred_probas.argmax()
    print '-------'

import os
import glob
import random
import numpy as np
import cv2

from genericCreateLMDB import *


train_data = [img for img in glob.glob("../input/train/*jpg")]
random.shuffle(train_data)

#Size of images
img_width = 227
img_height = 227

noImages = len(train_data)

images = np.zeros([noImages, img_height, img_width, 3])
labels = np.zeros(noImages)

for i, dir in enumerate(train_data):
	image = cv2.imread(train_data[i], cv2.IMREAD_COLOR)
	image = transform_img(image, img_width, img_height)
	print image.shape
	images[i] = image
	print images.shape

	if 'cat' in train_data[i]:
            labels[i] = 0
        else:
            labels[i] = 1

createLMDB(images, labels, '../input/train_lmdb')

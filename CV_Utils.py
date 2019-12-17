#!/usr/bin/python
# -*- coding: utf-8 -*

import cv2

def rotate_img(src, angle=90):
    height, width, channel = src.shape
    matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    dst = cv2.warpAffine(src, matrix, (width, height))
    return dst

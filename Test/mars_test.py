#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:mars
@file: mars_test.py
@time: 2019/03/07
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open('test1.png'))
print(text)
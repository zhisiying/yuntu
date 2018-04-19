#!/usr/bin/env python
# encoding: utf-8
"""
@version: python3.6
@author: zsy
@contact: 643424678@qq.com
@software: PyCharm
@file: QQ空间词云设计.py
@time: 2018/4/17/017 17:33
"""

import jieba.analyse
import os
import re
from scipy.misc import imread
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

plt.rc('figure', figsize=(15, 15))
import pymongo

client = pymongo.MongoClient()
db = client['QQ']
collection = db['Mood']
shuo = []
d = os.path.dirname(__file__)
for i in collection.find():
    txt = i['Mood_cont']
    list = re.findall('[\u4e00-\u9fa5]', txt)
    if list == []:
        pass
    else:
        txt = re.sub('转载内容', '', ''.join(list).strip('评语'))
        seg_list = jieba.cut_for_search(txt)
        words = ' '
        for seg in seg_list:
            words = words + seg + ' '
        print(words)
        shuo.append(words)
        # f = open('shuoshuo.txt','a+',encoding='utf8')
        # f.write(''.join(shuo))
        # f.close()

seg_list = jieba.analyse.extract_tags(''.join(shuo), topK=100, withWeight=True, allowPOS=())
for v, n in seg_list:
    print(v + '\t' + str(int(n * 10000)))
# back_coloring = imread(os.path.join(d, "./ce.jpg"))
wordcloud = WordCloud(random_state=42, font_path=r'C:/Users/Windows/fonts/simkai.ttf',
                      background_color="black",
                      max_words=2000,
                      # mask=back_coloring,#背景图
                      max_font_size=50,
                      min_font_size=20,
                      ).generate(''.join(shuo))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

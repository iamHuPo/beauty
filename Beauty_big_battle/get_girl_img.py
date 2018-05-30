# -*- coding:utf-8 -*-

import requests

import os

import time

import uuid

import random

import codecs

from config import USER_AGENT_LIST,REQUEST_DELAY

from lxml import etree


#------------------

#这个网站不难爬取， 只要更换伪装头和随机爬取时间就可以完美爬完整站

#获取当前文件路径，当然你也可以自定义

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#开始url， {}是占位符

start_url = 'http://www.meizitu.com/a/more_{}.html'

#XPATH规则匹配当前页所有图片的链接地址

Xpath_url = '//ul[@class="wp-list clearfix"]/li[@class="wp-item"]/div[@class="con"]/h3[@class="tit"]/a'

#匹配当前页所有图片的src

Xpath_img = '//p/img'


#------------------

#获取页面

def get_url(url,headers):
    res = requests.get(url=url,headers=headers)
    res.encoding = 'gb2312'
    doc = etree.HTML(res.text)
    return doc

if __name__ == '__main__':
    i = 0
    k = 0
    while i<75:
        i+=1
        start_url =start_url.format(1)
        print(start_url)
        headers = {'User-Agent':USER_AGENT_LIST[random.randint(0,len(USER_AGENT_LIST)-1)]}
        doc = get_url(url=start_url.format(i),headers=headers)
        results = doc.xpath(Xpath_url)
        print(requests)
        global k
        for result in results:
            k += 1
            title = result.xpath('.//child::text()')
            print(title[0])
            src = BASE_DIR+'/'+unicode(k)
            if not os.path.exists(src):
                os.mkdir(src)
                with codecs.open(src+"/"+title[0]+'.text','w',encoding='utf-8') as ff:
                    ff.write(title[0])
            urls = result.xpath('attribute::href')[0]
            print(urls)
            doc = get_url(url=urls,headers=headers)
            results2 = doc.xpath(Xpath_img)
            for result2 in results2:
                img_src = result2.xpath('attribute::src')[0]
                time.sleep(1)
                img = requests.get(url=result2.xpath('attribute::src')[0],headers=headers).content
                # print(img)
                with open(src+'/'+unicode(uuid.uuid4())+img_src[img_src.rindex('.'):],'wb') as f:
                    f.write(img)
# -*- coding:utf-8 -*-


import requests

import os

import time

import uuid

import random

import codecs

from config import USER_AGENT_LIST

from lxml import etree


class MyReptilian(object):
    # 这个网站不难爬取， 只要更换伪装头和随机爬取时间就可以完美爬完整站

    # 获取当前文件路径，当然你也可以自定义

    BASE_DIR = os.path.dirname(__file__)

    # 开始url， {}是占位符

    start_url = 'http://www.meizitu.com/a/more_{}.html'

    # XPATH规则匹配当前页所有图片的链接地址

    Xpath_url = '//ul[@class="wp-list clearfix"]/li[@class="wp-item"]/div[@class="con"]/h3[@class="tit"]/a'

    # 匹配当前页所有图片的src

    Xpath_img = '//p/img'

    k = 0

    def __init__(self,you_strat_page,you_page):
        '''
        :param you_strat_page: 从第几页开始爬取
        :param you_page: 你要爬取以后的多少页
        '''
        self.you_strat_page = you_strat_page
        self.you_page = you_page
        self.__start_url ='http://www.meizitu.com/a/more_{}.html'
        self.headers={'User-Agent':USER_AGENT_LIST[random.randint(0,len(USER_AGENT_LIST)-1)]}



    def __get_url(self,url, headers):
        res = requests.get(url=url, headers=headers)
        res.encoding = 'gb2312'
        doc = etree.HTML(res.text)
        return doc

    def run(self):
        i = self.you_strat_page
        print(self.you_strat_page+self.you_page)

        #循环体用来控制获取取次数

        while i <= (self.you_strat_page+self.you_page):
            #开始地址，这个地址是最好爬取位置
            start_url = self.start_url.format(i)
            print(self.headers)
            doc = self.__get_url(start_url,headers=self.headers)
            results = doc.xpath(self.Xpath_url)
            for result in results:
                self.k += 1
                title = result.xpath('.//child::text()')
                print(title[0])

                # 设置存储路径，并创建存储文件夹
                src = self.BASE_DIR + '/' + unicode(self.k)
                if not os.path.exists(src):
                    os.mkdir(src)

                    #标识一下该文件夹下图片的内容标题
                    with codecs.open(src + "/" + title[0] + '.text', 'w', encoding='utf-8') as ff:
                        ff.write(title[0])
                urls = result.xpath('attribute::href')[0]
                print(urls)
                doc = self.__get_url(url=urls, headers=self.headers)
                results2 = doc.xpath(self.Xpath_img)
                for result2 in results2:
                    img_src = result2.xpath('attribute::src')[0]

                    #设置睡眠时间，利用一个伪随机数

                    time.sleep(random.randint(0,3))

                    #这里用来下载图片

                    img = requests.get(url=result2.xpath('attribute::src')[0], headers=self.headers).content



                    try:
                        with open(src + '/' + unicode(uuid.uuid4()) + img_src[img_src.rindex('.'):], 'wb') as f:
                            f.write(img)
                    except BaseException as e:
                        print(e.message)

            i +=1


if __name__ == '__main__':
    my =MyReptilian(1,2)
    my.run()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-14 13:33:04
# @Author  : Xu Kang Xie (1391963397@qq.com)
# @Link    : https://blog.csdn.net/wudibaba21
# @Version : $Id$
import threading
import time
import os
import requests
import re
import eventlet#导入eventlet这个模块
import random
from urllib import request
from lxml import etree
from queue import Queue
class Procuder(threading.Thread):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                print("生产结束了")
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        titles =html.xpath('//*[@id="home"]/div/div[2]/a/div[1]')
        for index,title in enumerate(titles):
            print(title.text)
            try:

                os.mkdir(title.text)
            except: 
                print("文件已经存在")
            imgs = html.xpath('//*[@id="home"]/div/div[2]/a[%d]/div[2]/div/img'% (index+1))
            # image = html.xpath('//*[@id="home"]/div/div[2]/a[4]/div[2]/div[1]/img')
            # for img in image:
            #     print(img.xpath('@data-backup'))
            for img in imgs:
                src = img.xpath('@data-backup')
                #print(src)
                alt = img.xpath('@alt')
                #print(alt)
                if src == [] or alt ==[] or src == [''] or alt ==['']:
                    pass
                else:
                    alt = re.sub(r'[\?？,，。！!]','',alt[0])
                    
                    suffix = os.path.splitext(src[0])[1]
                    image_name = alt +suffix
                    path = './%s'% title.text
                    self.img_queue.put((src[0],os.path.join(path,image_name)))
                    #print(image_name)
                

class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                print("消费结束了")
                break
            img_url,filename = self.img_queue.get()
            opener=request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')]
            request.install_opener(opener)
            
            #可能会碰到图片不存在的情况
            try:
                print(img_url,"正在下载")
                flag = 0
                with eventlet.Timeout(8,False):#设置超时时间为4秒
                    flag = 1
                    request.urlretrieve(img_url,filename)
                if flag ==0:
                    print("超时了，没有下载")

            except:
                print("此图片存在问题，跳过下载!!!")

def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    #start_time = time.clock()
    for x in range(1,10):
        url = 'http://www.doutula.com/article/list/?page=%d'% x
        page_queue.put(url)

    for x in range(5):
        print("生产")
        t = Procuder(page_queue,img_queue)
        t.start()

    for x in range(5):
        print('测试')
        t1 = Consumer(page_queue,img_queue)
        t1.start()

    #print("花费时间:",(time.clock()-start_time))

if __name__ == '__main__':
    main()
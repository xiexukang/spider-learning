#encoding:utf-8
import threading
import time
import os
import requests
import re
import eventlet#导入eventlet这个模块
import random
from urllib import request
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
eventlet.monkey_patch()
def parse_page(url):
    response = requests.get(url,headers=headers)
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
                #print(image_name)
                opener=request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')]
                request.install_opener(opener)
                path = './%s'% title.text
                #可能会碰到图片不存在的情况
                try:
                    print(src[0],"正在下载")
                    flag = 0
                    with eventlet.Timeout(8,False):#设置超时时间为8秒
                        flag = 1
                        request.urlretrieve(src[0],os.path.join(path,image_name))
                    if flag ==0:
                        print("超时了，没有下载")

                except:
                    print("此图片存在问题，跳过下载!!!")
                #time.sleep(1)

def download(url,path,image_name):
    request.urlretrieve(url,os.path.join(path,image_name))

def recordtime(start_time):
    end_time = time.clock()
    if (end_time-start_time) >5:
        print("超时")



def main():
    #目前爬取10页内容下载下来
    start_time = time.clock()
    for i in range(5,6):
        url = 'http://www.doutula.com/article/list/?page=%d'% i
        parse_page(url)
    print((time.clock()-start_time))
if __name__ == '__main__':
    main()
#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import re
import urllib
import urllib2
import urlparse
import subprocess
import threading
import helper

sys.path.append("threadpool/src")
from threadpool import *

class MMCrawler:

    def __init__(self,threads,output,limits):
        self.threads = threads #任务线程数
        self.output = output #图片保存目录
        self.limits = limits  #抓取图片数量限制
        self.tasks = 0 #已完成任务数
        self.stop = False #停止任务
        self.threadpool = ThreadPool(self.threads) #初始化线程池

    def recursion_category(self,category_index_page):
        """递归抓取所有分类页面
        :param category_index_page: 分类首页地址
        """
        while(True):
            if self.stop == True: break;
            self.fetch_category_page(category_index_page) #抓取当前页
            nextpage = self.get_next_category_page(category_index_page) #获得下一页地址
            if nextpage != "":
                self.recursion_category(nextpage)
            else:
                break

    def fetch_category_page(self,category_page_url):
        """抓取分类页中的所有图片
        :param category_page_url: 分页类地址
        """
        suites  = self.fetch_suites(category_page_url) 
        print "当前分类页中套图数量：",len(suites)
        for suite_url in suites:
            suite_images = self.fetch_suite_images(suite_url) 
            print "当前套图中图片数量：",len(suite_images)
            for image_url in suite_images:
                if not self.stop:
                    self.fetch_image(image_url)
                else:
                    return

    def get_next_category_page(self,category_page_url):
        """获取分类的下一页地址
        :param category_page_url: 分类页地址
        """
        html            = helper.http_get(category_page_url)
        next_page_re    = re.compile('<a href=\'(index_\\d+.html)\'>></a>')
        next_page       = next_page_re.findall(html)
        if len(next_page) > 0:
            return urlparse.urljoin(category_page_url,next_page[0])
        return ""

    def fetch_suites(self,category_page_url):
        """抓取分类页中的所有套图
        :param category_page_url: 分类页地址
        """
        html = helper.http_get(category_page_url)
        real_urls = []
        link_re   = re.compile('<a.?href="(.*?)"')
        link_list = link_re.findall(html)
        for link in link_list:
            realurl = urlparse.urljoin(category_page_url,link)
            #过滤掉站外链接
            if  realurl.endswith(".html") and (realurl.find('/top/') == -1) :
                real_urls.append(realurl)
        return real_urls

    def fetch_suite_images(self,pageurl):
        """获取套图中的所有图片列表
        :param pageurl: 套图首页地址
        """
        html = helper.http_get(pageurl)
        if html == "":  return []
        #获得图片数量
        image_count_re  = re.compile('</span>/(\\d+)</strong><a href=')
        image_count     = image_count_re.findall(html)
        image_count     = len(image_count) == 1 and image_count[0] or 0
        #分析:最后一页中包含了所有的图片地址,因此抓取最后一页即可
        pageurl = pageurl[0:-5] + '-' + image_count + '.html'
        html    = helper.http_get(pageurl)
        if html == "":  return []
        #解析出所有图片地址
        link_re   = re.compile('\]="(.*?)"')
        link_list = link_re.findall(html)
        link_list = map(lambda url: url.replace("big","pic"),link_list)
        return link_list

    def fetch_image(self,image_url):
        """抓取网络图片
        :param image_url: 图片地址
        """
        if not self.__completed():
            #创建图片保存目录
            output_dir,filename = helper.make_subdir(self.output,image_url)
            realpath = os.path.join(output_dir,filename)
            #将抓取任务放入线程池
            self.threadpool.putRequest(WorkRequest(self.__retrieve_net_image,[realpath,image_url]))
        else:
            self.threadpool.wait()

    def __retrieve_net_image(self,realpath,image_url):
        """将网络图片并保存到本地目录(该函数在将会多线程访问)
        :param realpath: 保存到本地的绝对路径
        :param image_url: 图片网络地址
        """
        thread_current = threading.current_thread().getName()
        # print "current_thread: ",thread_current
        try:
            urllib.urlretrieve(image_url,realpath)
        except:
           print "[Error]:[retrieve_net_image]",sys.exc_info()[:2]

    def __completed(self):
        """检查是否满足条件停止程序"""
        if  self.stop == False and self.limits != 0 and self.tasks >= self.limits:
            self.stop = True
            return True
        else:
            print "Limits:",self.limits,"Threads:",len(threading.enumerate())," Completed:",self.tasks
            self.tasks += 1
            return False

if __name__ == "__main__":
    options = helper.get_options()
    mm_crawler = MMCrawler(options.threads,options.output,options.limits)
    #22MM美女网
    # mm_crawler.recursion_category("http://www.22mm.cc/mm/qingliang/index.html")
    # mm_crawler.recursion_category("http://www.22mm.cc/mm/jingyan/index.html")
    # mm_crawler.recursion_category("http://www.22mm.cc/mm/bagua/index.html")
    # mm_crawler.recursion_category("http://www.22mm.cc/mm/suren/index.html")

    #美女私房照
    mm_crawler.recursion_category("http://www.mnsfz.com/h/qingchun/index.html")
    # mm_crawler.recursion_category("http://www.mnsfz.com/h/meihuo/index.html")
    # mm_crawler.recursion_category("http://www.mnsfz.com/h/yangguang/index.html")
    # mm_crawler.recursion_category("http://www.mnsfz.com/h/qiaopi/index.html")

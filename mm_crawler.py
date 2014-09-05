#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import getopt
import re
import urllib
import urllib2
import urlparse
import ThreadPool
import subprocess

class MMCrawler:

    M_THREAD_SIZE      = 10
    M_OUTPUT_DIRECTORY = "pics"
    M_IMAGES_LIMIT     = 0
    M_TASKS_COUNT      = 0
    M_TASKS_STOP       = False
        
    def help(self):
        print "用法: python /path/mm_crawler.py [参数]"
        print "参数:"
        print "     -h                    帮助"
        print "     -n [size]             线程并发数"
        print "     -o [path]             图片保存目录"
        print "     -l [size]             抓取图片的个数"

    def options(self):
        optlist, args = getopt.getopt(sys.argv[1:], 'hn:o:l:')
        for op,value in optlist:
            if op == "-h":
                self.help()
                sys.exit()
            elif op == "-n":
                    MMCrawler.M_THREAD_SIZE         = int(value)
            elif op == "-o":
                    MMCrawler.M_OUTPUT_DIRECTORY    = value
            elif op == "-l":
                    MMCrawler.M_IMAGES_LIMIT        = int(value)

    def http_get(self,url):
        try:
            req     = urllib2.Request(url)
            opener  = urllib2.build_opener()
            f       = opener.open(req,timeout=10)
            isGzip  = f.headers.get('Content-Encoding')
            if isGzip :
                compresseddata      = f.read()
                compressedstream    = StringIO.StringIO(compresseddata)
                gzipper             = gzip.GzipFile(fileobj=compressedstream)
                data                = gzipper.read()
            else:
                data = f.read()

            return data
        except:
            print "[Error]: [request ",url,"]",sys.exc_info()[:2]
            return ""


    def main(self):
        self.options()
        #初始化线程池
        self.wm = ThreadPool.WorkerManager(MMCrawler.M_THREAD_SIZE,timeout=10)
        #按分类抓取
        self.recursion_category("http://www.22mm.cc/mm/qingliang/index.html");
        self.recursion_category("http://www.22mm.cc/mm/jingyan/index.html");
        self.recursion_category("http://www.22mm.cc/mm/bagua/index.html");
        self.recursion_category("http://www.22mm.cc/mm/suren/index.html");

    def recursion_category(self,category_index_page):
        ''' 递归抓取所有分类'''
        while(True):
            if(MMCrawler.M_TASKS_STOP):
                break;
            #当前页
            self.fetch_category_page(category_index_page)
            #下一页
            nextpage = self.get_next_category_page(category_index_page)
            if nextpage != '':
                self.recursion_category(nextpage)
            else:
                break;

    def fetch_category_page(self,category_page_url):
        '''
            1、抓取当前页面中的所有套图首页
            2、抓取套图中的各图片地址
            3、将抓取任务丢入线程池
        '''
        suites  = self.fetch_suites(category_page_url) 
        print "套图数量：",len(suites)
        for suite_url in suites:
            suite_images = self.fetch_suite_images(suite_url) 
            print "图片数量：",len(suite_images)
            for image_url in suite_images:
                #将任务加入到线程池
                self.wm.add_job(self.save_image,MMCrawler.M_OUTPUT_DIRECTORY,image_url)
                #超过限制数量则退出
                MMCrawler.M_TASKS_COUNT += 1
                if MMCrawler.M_IMAGES_LIMIT != 0 and MMCrawler.M_TASKS_COUNT >= MMCrawler.M_IMAGES_LIMIT:
                    MMCrawler.M_TASKS_STOP = True
                    self.wm.wait_for_complete()
                    return
    

    def get_next_category_page(self,category_page_url):
        '''
            给出一个大类地址,返回下一页的地址。
            如果是最后一页，则返回空字符串。
        '''
        html            = self.http_get(category_page_url)
        next_page_re    = re.compile('<a href=\'(index_\\d+.html)\'>></a>')
        next_page       = next_page_re.findall(html)
        if(len(next_page)>0): 
            return urlparse.urljoin(category_page_url,next_page[0]);
        return ""


    def fetch_suites(self,category_page_url):
        '''
            给出分类的页面,返回所有套图首页
        '''
        html = self.http_get(category_page_url)
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
        '''
            给出套图首页,返回所有图片列表
        '''
        html = self.http_get(pageurl)
        if html == "":  return []
        #获得图片数量
        image_count_re  = re.compile('</span>/(\\d+)</strong><a href=')
        image_count     = image_count_re.findall(html)
        image_count     = len(image_count) == 1 and image_count[0] or 0
        #分析:最后一页中包含了所有的图片地址,因此抓取最后一页即可
        pageurl = pageurl[0:-5] + '-' + image_count + '.html'
        html    = self.http_get(pageurl)
        if html == "":  return []
        #解析出所有图片地址
        link_re   = re.compile('\]="(.*?)"')
        link_list = link_re.findall(html)
        link_list = map(lambda url: url.replace("big","pic"),link_list)
        return link_list


    def save_image(self,save_dir,image_url):
        #根目录
        output_dir = os.path.join(os.getcwd(),save_dir)
        #子目录
        split_result    = urlparse.urlsplit(image_url)
        relative_path   = os.path.split(split_result.path)[0].replace("/pic/","")
        image_dir       = os.path.join(output_dir,relative_path)
        #保存图片
        command = "mkdir -p "+image_dir+" && cd "+image_dir + " && curl -O " + image_url
        subprocess.check_output(command,shell=True)
        #方式2
        #urllib.urlretrieve(image_url,filepath)
        return image_url


if __name__ == "__main__":
    MMCrawler().main()
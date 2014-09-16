#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import urllib
import urllib2
import urlparse
import StringIO
import gzip
from optparse import OptionParser

def get_options():
    parser = OptionParser(add_help_option=False)
    parser.add_option("-n", "--threads", dest = "threads", help=u"线程并发数", default = 10)
    parser.add_option("-o", "--output", dest = "output", help=u"图片保存目录",default = 'pics')
    parser.add_option("-l", "--limits", dest = "limits", help=u"图片抓取数量限制,默认抓取全站",default = 0)
    parser.add_option("-h", "--help", action="help")
    options, args   = parser.parse_args()
    options.threads = int(options.threads)
    options.limits  = int(options.limits)
    return options

def http_get(url):
    try:
        req     = urllib2.Request(url)
        req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14')
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


def make_subdir(save_dir,image_url):
    root_dir        = os.path.join(os.getcwd(),save_dir)
    #创建子目录
    split_result    = urlparse.urlsplit(image_url)
    split_result    = os.path.split(split_result.path)
    filepath        = split_result[0]
    filename        = split_result[1]
    #创建子目录
    output_dir = os.path.join(root_dir,filepath[1:])
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)
    return (output_dir,filename)

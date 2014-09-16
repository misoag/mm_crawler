#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import threading
import sys
sys.path.append("threadpool/src")
from threadpool import *

def doWork(i):
    time.sleep(i)
    print threading.currentThread().getName()," has sleeped ",i," seconds"
    print "Thread count:",len(threading.enumerate()),"\r\n"

pool = ThreadPool(10)
for i in range(60):
    pool.putRequest(WorkRequest(doWork, [i]))

pool.wait()

#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import threading
import sys
sys.path.append("threadpool/src")
from threadpool import *


main = ThreadPool(10)

def doWork(i):
    time.sleep(i)
    print threading.currentThread().getName()," has sleeped ",i," seconds"
    print "Thread count:",len(threading.enumerate()),"\r\n"
    if(i == 4):
        main.dismissWorkers(10)


for i in range(10):
    main.putRequest(WorkRequest(doWork, [i]))

try:
    main.wait()
except NoWorkersAvailable:
    None

#!/usr/bin/env python

import os
import time
from datetime import datetime

def main():
    while True:
        print datetime.now()
        print 'Checking active connections'
        ret = os.system('netstat -t | grep -e viper:1234 -e viper:ssh')
        if ret != 0:
            print 'No active connection found, going to sleep'
            os.system('sudo pm-suspend')
        print
        time.sleep(60*10)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys
import os
import time
from wmctrl import Window

def main():

    arglist = ['"%s"' % arg for arg in sys.argv[1:]]
    arglist = ' '.join(arglist)
    os.system('keyjnote --fullscreen -g 1024x768 %s &' % arglist)

    while True:
        windows = Window.by_name_startswith('KeyJnote')
        if not windows:
            time.sleep(0.5)
            continue
        for win in windows:
            win.resize_and_move(0, 0, 1024, 768)
        break

if __name__ == '__main__':
    main()

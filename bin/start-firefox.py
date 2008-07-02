#!/usr/bin/env python

import os
import time
import wmctrl

def main():
    os.system('firefox &')

    while True:
        windows = wmctrl.win_by_name_endswith('Mozilla Firefox')
        if not windows:
            time.sleep(0.5)
            continue
        for win in windows:
            wmctrl.set_geometry(win, os.environ['FIREFOX_GEOMETRY'])
        break

if __name__ == '__main__':
    main()

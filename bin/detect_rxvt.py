#!/usr/bin/env python

import sys
import rxvtlib

if __name__ == '__main__':
    sys.exit(not rxvtlib.RXVT_TERMINAL)

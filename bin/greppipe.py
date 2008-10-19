#!/usr/bin/env python

import sys
import os.path
import rxvtlib
from color import color, GREEN, YELLOW, BLUE, MAGENTA, CYAN

def cat():
    for line in sys.stdin:
        sys.stdout.write(line)

def parseline(line):
    if line == '--':
        return line
    try:
        filename, lineno, line2 = line.split(':', 2)
        int(lineno) # check that it's a number
        return filename, lineno, line2
    except ValueError:
        pass
    return '', '', line

def main():
    if not rxvtlib.RXVT_TERMINAL:
        cat()
        return
    
    for line in sys.stdin:
        filename, lineno, line = parseline(line)
        #link = '%s:%s' % (color(filename, CYAN), color(lineno, GREEN))
        #link = '%s:%s' % (filename, lineno)
        link = color(filename, CYAN, bg=0)
        #link = filename
        line = rxvtlib.openfile_format(line, os.path.abspath(filename), lineno)
        line = '%s:%s' % (link, line)
        sys.stdout.write(line)

if __name__ == '__main__':
    main()

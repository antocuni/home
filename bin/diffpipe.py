#!/usr/bin/env python

import sys
from color import color, YELLOW, GRAY

def main():
    for line in sys.stdin:
        if line.startswith('+'):
            sys.stdout.write(color(line, YELLOW))
        elif line.startswith('-'):
            sys.stdout.write(color(line, GRAY, bg=0))
        else:
            sys.stdout.write(line)

if __name__ == '__main__':
    main()

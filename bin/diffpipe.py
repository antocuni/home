#!/usr/bin/env python

import sys

def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[00m'
    return template % (bg, fg, s)

YELLOW = 33
GRAY = 30

for line in sys.stdin:
    if line.startswith('+'):
        sys.stdout.write(color(line, YELLOW))
    elif line.startswith('-'):
        sys.stdout.write(color(line, GRAY))
    else:
        sys.stdout.write(line)


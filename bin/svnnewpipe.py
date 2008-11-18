#!/usr/bin/env python

import sys
from svnshow import parse_args
from blamepipe import parseline, cycle

def main():
    assert len(sys.argv) == 2
    minrev = sys.argv[1]
    assert minrev.startswith('-r')
    minrev = minrev[2:]
    minrev = int(minrev)

    rev2color = {}
    author2color = {}
    for line in sys.stdin:
        try:
            rev, author, text = parseline(line)
            rev = int(rev)
        except ValueError:
            sys.stdout.write(' %s\n' % text)
            continue

        if rev > minrev:
            text = cycle(rev, rev2color, bg=1, text=text)
            sys.stdout.write('*%s\n' % text)
        else:
            sys.stdout.write(' %s\n' % text)

if __name__ == '__main__':
    main()

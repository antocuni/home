#!/usr/bin/env python

import os
import sys

def get_repo_root(wcpath):
    g = os.popen('svn info "%s"' % (wcpath,))
    lines = g.readlines()
    g.close()
    for line in lines:
        if line.startswith('Repository Root: '):
            return line[len('Repository Root: '):].strip()
    raise Exception("cannot find the repository root")

def main():
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog [options] [TARGET]')
    parser.add_option('-r', '--rev', dest='rev', default='1:HEAD',
                      help='svn revision number')

    options, args = parser.parse_args()
    if len(args) == 0:
        wcpath = '.'
    elif len(args) == 1:
        wcpath = args[0]
    else:
        parser.print_help()
        parser.exit(1)

    rev = options.rev
    root = get_repo_root(wcpath)
    os.system('svn log -v -r %s %s' % (rev, root))
    print
    if ':' not in rev:
        try:
            r = int(rev)
        except ValueError:
            pass
        else:
            rev = '%d:%d' % (r-1, r)
    os.system('svn diff -r%s %s | diffpipe.py' % (rev, root))

if __name__ == '__main__':
    main()

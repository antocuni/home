#!/usr/bin/env python

import sys
import os.path
import rxvtlib
import svnshow
from color import color, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GRAY

COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GRAY]

def cat():
    for line in sys.stdin:
        sys.stdout.write(line)

def parseline(line):
    line = line.lstrip()
    rev, line = line.split(' ', 1)
    int(rev) # may raise ValueError
    line = line.lstrip()
    if ' ' not in line:
        author = line
        return rev, author, ''
    author, line = line.split(' ', 1)
    return rev, author, line


def test_parseline():
    import py
    assert parseline(' 12345   antocuni bla bla') == ('12345', 'antocuni', 'bla bla')
    assert parseline(' 12345   antocuni     bla') == ('12345', 'antocuni', '    bla')
    assert parseline(' 12345   antocuni')         == ('12345', 'antocuni', '')
    assert parseline(' 12345   antocuni  ')        == ('12345', 'antocuni', ' ')
    assert parseline('12345    antocuni bla bla')  == ('12345', 'antocuni', 'bla bla')
    py.test.raises(ValueError, parseline, ' xxx   antocuni bla bla')

def cycle(key, key2color, bg):
    col = key2color.get(key)
    if not col:
        col = COLORS[len(key2color) % len(COLORS)]
        key2color[key] = col
    return color(key, col, bg=bg)

def main():
    if not rxvtlib.RXVT_TERMINAL:
        cat()
        return

    _, wcpath = svnshow.parse_args()
    root = svnshow.get_repo_root(wcpath)
    wcpath = os.path.abspath(wcpath)

    rev2color = {}
    author2color = {}
    for line in sys.stdin:
        try:
            rev, author, text = parseline(line)
        except ValueError:
            sys.stdout.write(line)
            continue
        
        cmd = 'svn show --rev %s "%s"' % (rev, wcpath)
        cmd = rxvtlib.command_in_term(cmd)
        
        rev = cycle(rev, rev2color, bg=1)
        rev = rxvtlib.format_command(rev, cmd)
        author = cycle(author, author2color, bg=0)
        sys.stdout.write(' %s   %s %s' % (rev, author, text))
        

if __name__ == '__main__':
    main()

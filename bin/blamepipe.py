#!/usr/bin/env python

import re
import sys
import os.path
import rxvtlib
import svnshow
from color import color, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GRAY

COLORS = [CYAN, RED, GREEN, YELLOW, BLUE, MAGENTA, GRAY]

regexp = re.compile(r'( *[0-9]+)( *[^ ]+)(.*)')
def parseline(line):
    match = regexp.match(line)
    if not match:
        raise ValueError
    return match.groups()

def test_parseline():
    import py
    assert parseline(' 12345   antocuni bla bla') == (' 12345', '   antocuni', ' bla bla')
    assert parseline(' 12345   antocuni     bla') == (' 12345', '   antocuni', '     bla')
    assert parseline(' 12345   antocuni')         == (' 12345', '   antocuni', '')
    assert parseline(' 12345   antocuni  ')       == (' 12345', '   antocuni', '  ')
    assert parseline('123456       anto bla bla') == ('123456', '       anto', ' bla bla')
    py.test.raises(ValueError, parseline, ' xxx   antocuni bla bla')

def cycle(key, key2color, bg):
    col = key2color.get(key)
    if not col:
        col = COLORS[len(key2color) % len(COLORS)]
        key2color[key] = col
    return color(key, col, bg=bg)

def main():
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
        rev = rxvtlib.format_command(rev, cmd, force=True)
        author = cycle(author, author2color, bg=0)
        sys.stdout.write('%s%s%s\n' % (rev, author, text))
        

if __name__ == '__main__':
    main()

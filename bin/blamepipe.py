#!/usr/bin/env python

import re
import sys
import os.path
import rxvtlib
import svnshow
from color import color, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, GRAY

COLORS = [CYAN, RED, GREEN, YELLOW, BLUE, MAGENTA, GRAY]

regexps = [
    re.compile(r'( *[0-9]+)( *[^ ]+)(.*)'), # for svn
    re.compile(r'( *[^ ]+)( *[0-9]+:)(.*)') # for hg
    ]

def parseline(line):
    for regexp in regexps:
        match = regexp.match(line)
        if match:
            return match.groups()
    raise ValueError

def test_parseline():
    import py
    # format for svn blame
    assert parseline(' 12345   antocuni bla bla') == (' 12345', '   antocuni', ' bla bla')
    assert parseline(' 12345   antocuni     bla') == (' 12345', '   antocuni', '     bla')
    assert parseline(' 12345   antocuni')         == (' 12345', '   antocuni', '')
    assert parseline(' 12345   antocuni  ')       == (' 12345', '   antocuni', '  ')
    assert parseline('123456       anto bla bla') == ('123456', '       anto', ' bla bla')
    # format for hg blame -u -n
    assert parseline('anto 12345: bla bla')   == ('anto', ' 12345:', ' bla bla')
    assert parseline('  anto 12345: bla bla') == ('  anto', ' 12345:', ' bla bla')
    assert parseline('anto   12345: bla bla') == ('anto', '   12345:', ' bla bla')
    #
    py.test.raises(ValueError, parseline, ' xxx   antocuni bla bla')

def cycle(key, key2color, bg, text=None):
    if text is None:
        text = key
    col = key2color.get(key)
    if not col:
        col = COLORS[len(key2color) % len(COLORS)]
        key2color[key] = col
    return color(text, col, bg=bg)

def main():
    #_, wcpath = svnshow.parse_args()
    #root = svnshow.get_repo_root(wcpath)
    #wcpath = os.path.abspath(wcpath)

    rev2color = {}
    author2color = {}
    for line in sys.stdin:
        try:
            rev, author, text = parseline(line)
        except ValueError:
            sys.stdout.write(line)
            continue
        
        ## cmd = 'svn show --rev %s "%s"' % (rev, wcpath)
        ## cmd = rxvtlib.command_in_term(cmd)
        
        rev = cycle(rev, rev2color, bg=0)
        ## rev = rxvtlib.format_command(rev, cmd, force=True)
        author = cycle(author, author2color, bg=0)
        sys.stdout.write('%s%s%s\n' % (rev, author, text))
        

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import py
import sys
from urlparse import urlsplit
import re
import webbrowser

def main():
    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: viewwc.py FILE'
        return 1

    try:
        svninfo = py.path.svnwc(sys.argv[1]).info()
    except py.error.ENOENT:
        print >> sys.stderr, 'No such file or not under version control: %s' % sys.argv[1]
        return 2
    
    svnurl = svninfo.url
    rev = svninfo.rev
    svnurl_info = urlsplit(svnurl)
    svnhost = svnurl_info[1]
    svnpath = svnurl_info[2]

    # XXX: it might not work on windows
    wwwpath = re.sub('^/svn/', 'viewvc/', svnpath)
    wwwurl = 'http://%s/%s?annotate=%s' % (svnhost, wwwpath, rev)
    webbrowser.open(wwwurl)

sys.exit(main())

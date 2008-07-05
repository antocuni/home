#!/usr/bin/env python

"""
Usage: done2.py [pypy-exe] -[suffix]

This copies:

  - pypy-c executable   to ./pypy-c-REV-suffix

  - pypy-cli executable to ./pypy-cli-REV-suffix
    and exe and dll     to ./pypy-cli-REV-suffix-data

  - pypy-jvm executable to ./pypy-jvm-REV-suffix
    and pypy-jvm jar to    ./pypy-jvm-REX-suffix.jar

If pypy-exe is not specified, the most recent one in the current
directory is picked.

Use '-' if you don't want any suffix.
"""

import sys
import os
import os.path
import glob
from commands import getstatusoutput
import py

def queryrev(exe):
    exe = os.path.abspath(exe)
    cmd = "%s -c 'import sys; print sys.pypy_version_info[-1]'"
    status, out = getstatusoutput(cmd % exe)
    if status != 0:
        print >> sys.stderr, "Cannot determine revision number"
        print >> sys.stderr, out
        raise SystemExit(3)
    lines = out.splitlines()
    return int(lines[-1]) # discard other possible messages, like 'import site failed'

def parse_args(argv):
    n = len(argv)
    if n == 2:
        assert argv[1].startswith('-')
        return None, argv[1]
    elif n == 3:
        assert argv[2].startswith('-')
        return argv[1], argv[2]
    else:
        assert False

def do(cmd):
    print '*', cmd
    os.system(cmd)

def find_most_recent_exe():
    pypys = []
    for f in py.path.local('.').listdir('pypy-*'):
        if f.check(file=True, link=False):
            pypys.append((f.stat().mtime, f))
    pypys.sort()
    if not pypys:
        print >> sys.stderr, 'Cannot find pypy executables'
        raise SystemExit(5)
    exe = pypys[-1][1]
    print 'Picking %s' % exe
    return str(exe)

def done(exe, suffix):
    if exe is None:
        exe = find_most_recent_exe()

    rev = queryrev(exe)
    if 'pypy-jvm' in exe:
        basename = 'pypy-jvm'
        datasuffixes = ['.jar']
    elif 'pypy-cli' in exe:
        basename = 'pypy-cli'
        datasuffixes = ['-data']
    elif 'pypy-c' in exe:
        basename = 'pypy-c'
        datasuffixes = []
    else:
        print >> sys.stderr, 'Unknown backend: %s' % exe
        raise SystemExit(4)

    dest = '%s-%s%s' % (basename, rev, suffix)
    if os.path.realpath(exe) == os.path.realpath(dest):
        print 'No need to rename %s' % exe
        return

    do('mv %s %s' % (exe, dest))
    for s in datasuffixes:
        do('mv %s%s %s%s' % (exe, s, dest, s))

    do('ln -sf %s %s' % (dest, basename))

if __name__ == '__main__':
    try:
        exe, suffix = parse_args(sys.argv)
        if suffix == '-':
            suffix = ''
    except AssertionError:
        print __doc__.strip()
        sys.exit(2)
    sys.exit(done(exe, suffix))

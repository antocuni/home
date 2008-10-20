#!/usr/bin/env python

import os.path

home = os.path.expanduser('~')
path = os.path.dirname(os.path.abspath(__file__))
excludes = ['create_symlinks.py', 'scripts', 'elisp']

def symlink(src, dst):
    # check if dst is already a symlink to src
    try:
        link = os.readlink(dst)
        if link == src:
            return # nothing to do
    except OSError:
        pass
    os.symlink(src, dst)

def main():
    for f in os.listdir(path):
        if (f.startswith('.') or
            f.endswith('~') or
            f.endswith('.pyc') or
            f in excludes):
            continue
        
        dst = os.path.join(home, '.' + f)
        src = os.path.abspath(f)
        try:
            print '%s -> %s' % (src.replace(path, '.'), dst.replace(home, '~')),
            symlink(src, dst)
            print
        except Exception, msg:
            print "Failed: %s" % (msg,)

if __name__ == '__main__':
    main()

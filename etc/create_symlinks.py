#!/usr/bin/env python

import os.path

home = os.path.expanduser('~')
path = os.path.dirname(os.path.abspath(__file__))
excludes = ['create_symlinks.py', 'scripts', 'elisp']

def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[0m'
    return template % (bg, fg, s)

def symlink(src, dst):
    # check if dst is already a symlink to src
    try:
        link = os.readlink(dst)
        if link == src:
            return # nothing to do
    except OSError:
        pass
    os.symlink(src, dst)

def do_symlink(src, dst):
    try:
        print '%s -> %s' % (src.replace(path, '.'), dst.replace(home, '~')),
        symlink(src, dst)
        print
    except Exception, msg:
        print color("Failed: %s" % (msg,), 31)


def main():
    for f in os.listdir(path):
        if (f.startswith('.') or
            f.endswith('~') or
            f.endswith('.pyc') or
            f in excludes):
            continue
        dst = os.path.join(home, '.' + f)
        src = os.path.abspath(f)
        do_symlink(src, dst)

    more_links = [
        ('~/pypy/user/antocuni/hack/pdbrc.py', '~/.pdbrc.py'),
        ]
    for src, dst in more_links:
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        do_symlink(src, dst)

if __name__ == '__main__':
    main()

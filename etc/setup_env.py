#!/usr/bin/env python

import os.path
import glob

home = os.path.expanduser('~')
etc_dir = os.path.dirname(os.path.abspath(__file__))
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
        if link.startswith('/home/antocuni/pypy/user/antocuni/') or\
           link.startswith('pypy/user/antocuni'):
            # old location, kill it
            os.remove(dst)
    except OSError:
        pass
    os.symlink(src, dst)

def do_symlink(src, dst):
    try:
        print '%s -> %s' % (src.replace(etc_dir, '.'), dst.replace(home, '~')),
        symlink(src, dst)
        print
    except Exception, msg:
        print color("Failed: %s" % (msg,), 31)


def create_symlinks():
    print color('Creating symlinks', 33)
    for f in os.listdir(etc_dir):
        if (f.startswith('.') or
            f.endswith('~') or
            f.endswith('.pyc') or
            f in excludes):
            continue
        dst = os.path.join(home, '.' + f)
        src = os.path.abspath(f)
        do_symlink(src, dst)

    more_links = [
        ('~/env/src/pdb/pdbrc.py', '~/.pdbrc.py'),
        ('~/env/bin', '~/bin'),
        ('~/env/src', '~/src'),
        ]
    for src, dst in more_links:
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        do_symlink(src, dst)

def install_py_packages():
    orig_dir = os.getcwd()
    envdir = os.path.dirname(etc_dir)
    pattern = os.path.join(envdir, 'src', '*', 'setup.py')
    for setup_py in glob.glob(pattern):
        print
        print color('Installing %s' % setup_py, 33)
        path = os.path.dirname(setup_py)
        os.chdir(path)
        os.system('python "%s" develop --user' % setup_py)
    os.chdir(orig_dir)

if __name__ == '__main__':
    create_symlinks()
    install_py_packages()

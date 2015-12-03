#!/usr/bin/env python

import sys
import os.path
import glob
import subprocess

# ==============================================================
# configuration
#

PYLIB = 'https://bitbucket.org/pytest-dev/py'
REPOS = [
    ('hg', PYLIB, '~/src/py'),
    ('hg', 'https://bitbucket.org/antocuni/env', '~/env'),
    ('hg', 'https://bitbucket.org/antocuni/fancycompleter', '~/src/fancycompleter'),
    ('hg', 'https://bitbucket.org/antocuni/wmctrl', '~/src/wmctrl'),
    ('hg', 'https://bitbucket.org/antocuni/pdb', '~/src/pdb'),
    ('hg', 'https://bitbucket.org/antocuni/pytest-emacs', '~/src/pytest-emacs'),
    ('hg', 'https://bitbucket.org/pypy/pyrepl', '~/src/pyrepl'),
]

APT_PACKAGES = ['emacs', 'git', 'build-essential', 'python-dev']
APT_PACKAGES_GUI = ['wmctrl', 'libgtk2.0-dev', 'fonts-inconsolata', 'xsel']

#
# end of configuration
# ==============================================================

# misc utility functions
# ----------------------

RED = 31
GREEN = 32
YELLOW = 33

def color(s, fg=1, bg=1):
    template = '\033[%02d;%02dm%s\033[0m'
    return template % (bg, fg, s)

def system(cmd):
    ret = os.system(cmd)
    if ret != 0:
        print color('Command failed: ', RED), cmd
        sys.exit(ret)

# ==============================================================
# import the py lib: automatically download/install it if needed
#
def bootstrap():
    print color('bootstraping the pylib...', YELLOW)
    src = os.path.expanduser('~/src')
    if not os.path.exists(src):
        os.makedirs(src)
    pydir = os.path.join(src, 'py')
    system('hg clone %s %s' % (PYLIB, pydir))
    sys.path.append(pydir)

try:
    import py
except ImportError:
    bootstrap()
    import py

# end of the automagically pylib importing/boostraping
# ==============================================================

HOME = py.path.local('~', expanduser=True)
GUI_SENTINEL = HOME.join('.gui')

home = os.path.expanduser('~')
env_dir = os.path.join(home, 'env')
etc_dir = os.path.join(env_dir, 'dotfiles')

def main():
    gui = '--gui' in sys.argv or GUI_SENTINEL.check(file=True)
    write_hgrc_auth()
    clone_repos()
    create_symlinks()
    apt_install(APT_PACKAGES)
    if gui:
        apt_install(APT_PACKAGES_GUI)
        GUI_SENTINEL.write('this file tells home_setup.py that this is a GUI environment\n')
        compile_terminal_hack()
        import_dconf()
        install_desktop_apps()
    elif 'SSH_CLIENT' not in os.environ:
        print color('WARNING: did you forget --gui?', RED)


def write_hgrc_auth():
    import textwrap
    from getpass import getpass
    TEMPLATE = textwrap.dedent("""
        [auth]
        bb.prefix = https://bitbucket.org/
        bb.username = antocuni
        bb.password = %s
    """)
    hgrc_auth = HOME.join('.hgrc.auth')
    if hgrc_auth.check(file=True):
        print color('~/.hgrc.auth already exists', GREEN)
        return
    print color('Generating ~/.hgrc.auth...', YELLOW)
    bbpasswd = getpass("    antocuni's bitbucket.org password: ")
    hgrc_auth.write(TEMPLATE % bbpasswd)
    print color('    DONE', GREEN)

def clone_repos():
    print
    print color('Cloning repos:', YELLOW)
    for kind, url, dst in REPOS:
        clone_one_repo(kind, url, dst)

def clone_one_repo(kind, url, dst):
    dst = os.path.expanduser(dst)
    if os.path.exists(dst):
        print '    %s: ' % dst, color('already exists', GREEN)
        return
    print '    %s: ' % dst, color('cloning from %s' % url, YELLOW)
    system('%s clone %s %s' % (kind, url, dst))
    print

def symlink(src, dst):
    # check if dst is already a symlink to src
    try:
        link = os.readlink(dst)
        if link == src:
            return # nothing to do
        if not os.path.exists(link):
            # old location, kill it
            os.remove(dst)
    except OSError:
        pass
    os.symlink(src, dst)

def do_symlink(src, dst):
    try:
        print '    %s -> %s' % (src.replace(etc_dir, '.'), dst.replace(home, '~')),
        symlink(src, dst)
        print
    except Exception, msg:
        print color("Failed: %s" % (msg,), RED)

def create_symlinks():
    print
    print color('Creating symlinks', YELLOW)
    for f in os.listdir(etc_dir):
        dst = os.path.join(home, '.' + f)
        src = os.path.join(etc_dir, f)
        src = os.path.abspath(src)
        if (f.startswith('.') or
            f.endswith('~') or
            f.endswith('.pyc')):
            continue
        do_symlink(src, dst)

    more_links = [
        ('~/env/bin', '~/bin'),
        ('~/env/hacks/gnome-terminal-hack/gtk.css', '~/.config/gtk-3.0/gtk.css'),
        ('~/env/dotfiles/bash_profile', '~/.profile'),
        ('~/env/dotfiles/icons', '~/.icons'),
        ('~/env/hacks/fijalcolor.py', '~/.xchat2/fijalcolor.py'),
        ('~/src/pdb/pdbrc.py', '~/.pdbrc.py'),
        ]
    for src, dst in more_links:
        src = os.path.expanduser(src)
        dst = os.path.expanduser(dst)
        do_symlink(src, dst)

def apt_install(package_list):
    packages = ' '.join(package_list)
    ret = os.system('dpkg -s %s >/dev/null 2>&1' % packages)
    if ret != 0:
        print
        print color('install apt-packages', YELLOW)
        system('sudo apt-get install %s' % packages)

def compile_terminal_hack():
    print
    print color('gnome-terminal-hack', YELLOW)
    dirname = os.path.join(home, 'env', 'hacks', 'gnome-terminal-hack')
    system('make -C %s' % dirname)

def import_dconf():
    print
    print color('import dconf settings', YELLOW)
    dirname = os.path.join(env_dir, 'dconf')
    for filename in glob.glob('%s/*.sh' % dirname):
        print '    ', filename
        system(filename)

def install_desktop_apps():
    print
    print color('installing apps/*.desktop', YELLOW)
    dirname = os.path.join(env_dir, 'apps')
    for fullname in glob.glob('%s/*.desktop' % dirname):
        basename = os.path.basename(fullname)
        dst = os.path.join('~/.local/share/applications/', basename)
        dst = os.path.expanduser(dst)
        do_symlink(fullname, dst)

if __name__ == '__main__':
    main()

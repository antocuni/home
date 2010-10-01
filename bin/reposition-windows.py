#!/usr/bin/env python

import os
from wmctrl import Window

def main():
    for win in Window.by_name_endswith('Mozilla Firefox'):
        win.set_geometry(os.environ['FIREFOX_GEOMETRY'])
        
    for win in Window.by_name_endswith('Thunderbird'):
        win.set_geometry(os.environ['THUNDERBIRD_GEOMETRY'])
        
##     for win in wmctrl.win_by_role('autoterm'):
##         wmctrl.set_geometry(win, os.environ['AUTOTERM_GEOMETRY'])

    for win in Window.by_class('autorxvt.XTerm'):
        win.set_geometry(os.environ['AUTOTERM_GEOMETRY'])

    for win in Window.by_class('emacs.Emacs'):
        win.set_geometry(os.environ['EMACS_GEOMETRY'])

if __name__ == '__main__':
    main()

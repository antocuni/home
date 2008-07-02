#!/usr/bin/env python

import os
import wmctrl

def main():
    for win in wmctrl.win_by_name_endswith('Mozilla Firefox'):
        wmctrl.set_geometry(win, os.environ['FIREFOX_GEOMETRY'])
        
    for win in wmctrl.win_by_name_endswith('Thunderbird'):
        wmctrl.set_geometry(win, os.environ['THUNDERBIRD_GEOMETRY'])
        
    for win in wmctrl.win_by_role('autoterm'):
        wmctrl.set_geometry(win, os.environ['AUTOTERM_GEOMETRY'])

    for win in wmctrl.win_by_class('emacs.Emacs'):
        wmctrl.set_geometry(win, os.environ['EMACS_GEOMETRY'])

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import sys
import os
#open('/tmp/foo', 'a').write(str(sys.argv) + '\n')
import wmctrl

if len(sys.argv) == 2:
    arg = sys.argv[1]
else:
    print 'Usage: show.py [term|emacs]'
    sys.exit(1)

wlist = []
if arg == 'term':
    wlist = wmctrl.Window.by_role("autoterm")
elif arg == 'emacs':
    wlist = wmctrl.Window.by_class('emacs.Emacs24')
    wlist += wmctrl.Window.by_class('emacs24.Emacs24')
elif arg == 'xchat':
    wlist = wmctrl.Window.by_class('xchat.Xchat')
elif arg == 'zeal':
    # start zeal if it's not already
    wlist = wmctrl.Window.by_class('zeal.Zeal')
    if not wlist:
        os.system('zeal')



if wlist:
    wlist[0].activate()
else:
    print 'No windows found'

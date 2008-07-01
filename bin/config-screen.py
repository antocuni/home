#!/usr/bin/env python

import os
from commands import getoutput

xrandr_cmds = {
    'single-head': 'xrandr --output VGA --off --fb 1280x800',
    'dual-head':   'xrandr --output VGA --auto --right-of LVDS'
    }

def xrandr_query():
    "Return the list of connected outputs"
    out = getoutput('xrandr -q')
    res = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == 'connected':
            res.append(parts[0])
    res.sort()
    return res

def getconfig():
    outputs = xrandr_query()
    if outputs == ['LVDS']:
        return 'single-head'
    elif outputs == ['LVDS', 'VGA']:
        return 'dual-head'
    assert False, 'Unknown configuration for outputs %s' % outputs


def main():
    import sys
    if len(sys.argv) >= 2:
        config = sys.argv[1]
    else:
        config = getconfig()
    # load the config files from config-manager
    os.system('sudo config-manager.py load %s' % config)

    cmd = xrandr_cmds[config]
    os.system(cmd)                                # change the geometry of the screen
    os.system('/home/antocuni/bin/start-desktop') # restart the desklets & co.

if __name__ == '__main__':
    main()

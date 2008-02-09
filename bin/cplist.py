#!/usr/bin/env python

import sys
import shutil

dest = sys.argv[1]
f = open('/tmp/list')
for line in f:
    line = line.strip()
    print line
    shutil.copy(line, dest)


#!/usr/bin/env python

import sys
import os.path

f = open('/tmp/list', 'a')
name = sys.argv[1]
f.write(os.path.abspath(name))
f.write('\n')
f.close()

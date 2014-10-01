#!/usr/bin/env python

import os
import sys

os.system('coverage run run-tests.py')
os.system('coverage html -d ' + os.path.join('.testOutput', 'html'))
output = os.path.join('.testOutput', 'html', 'index.html')
if sys.platform == 'linux' or sys.platform == 'cygwin':
    os.system('xdg-open ' + output)
elif sys.platform == 'darwin':
    os.system('open ' + os.path.join('.testOutput', 'html'))
elif sys.platform == 'win32':
    os.system('start ' + output)
else:
    print('The coverage-report is located at ' + output)

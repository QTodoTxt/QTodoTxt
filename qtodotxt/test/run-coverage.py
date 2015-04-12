#!/usr/bin/env python

from os import path
from subprocess import call
from sys import platform

OUTPUT_DIR = path.join('.testOutput', 'html')

if platform == 'win32':
    from os import startfile

    def openfile():
        startfile(path.join(OUTPUT_DIR, 'index.html'))
else:
    def openfile():
        call(['xdg-open', path.join(OUTPUT_DIR, 'index.html')])

call(['coverage', 'run', 'run-tests.py'])
call(['coverage', 'html', '-d', OUTPUT_DIR])
openfile()

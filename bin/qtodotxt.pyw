#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
  __file__
except NameError:
  __file__ = sys.argv[0]

def reroute_py2exe_logs():
    appdata = os.path.expandvars("%AppData%\\QTodoTxt")
    if not os.path.isdir(appdata):
        os.makedirs(appdata)
    sys.stdout = open(appdata + "\\stdout.log", "w")
    sys.stderr = open(appdata + "\\stderr.log", "w")

if sys.argv[0].lower().endswith('.exe'):
# If something goes wrong, logging information might help.
# Uncommenting line below allows logging to be stored at same location where exe resides
    reroute_py2exe_logs()
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qtodotxt import app

app.run()


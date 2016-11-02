#! python
# -*- coding: utf-8 -*-

import os

    def getsubs(dir):
        # get all
        dirs = []
        files = []
        src = []
        for dirname, dirnames, filenames in os.walk(dir):
            dirs.append(dirname)
        for subdirname in dirnames:
            dirs.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
        src = filter(lambda x: x.endswith('.py'), files)
        return src

files = getsubs(os.curdir)
text  = "pylupdate5 qtodotxt/{1} -ts -noobsolete i18n/ru_RU.ts"
for file in files
	text.replace()
	os.system("pylupdate5 qtodotxt/app.py -ts -noobsolete i18n/ru_RU.ts")

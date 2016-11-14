#! python3
# -*- coding: utf-8 -*-

import os
import sys


# change to value of your locale
locale = "ru_RU"


def filterFiles(str):
    if str.endswith(".py"):
        return True
    return False


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
    for file in files:
        if filterFiles(file) and (file not in src):
            src.append(file)
    return src


def updateTranslation():
    print("__update__")
    files = getsubs(os.getcwd())
    myString = ' '.join(files)
    text = "pylupdate5 {0!s} -ts i18n/{1!s}.ts".format(myString, locale)
    os.system(text)


def clearTranslation():
    print("__no_obsolete__")
    files = getsubs(os.getcwd())
    myString = ' '.join(files)
    text = "pylupdate5 {0!s} -ts -noobsolete i18n/{1!s}.ts".format(myString, locale)
    os.system(text)


def fixationTranslation():
    print("__fixation__")
    text = "lrelease i18n/{0!s}.ts".format(locale)
    os.system(text)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "upd":
            updateTranslation()
        if sys.argv[1] == "fix":
            fixationTranslation()
        if sys.argv[1] == "clr":
            clearTranslation()
    else:
        print("Usage: \n params: upd | fix")
        print("upd - Update the specified language translations in the variable 'locale'")
        print("fix - Compilation of translations specified language")
        print("clr - Drop all obsolete strings'")
        print("!!!  don't forget update var locale in script !!!")

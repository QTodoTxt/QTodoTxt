import os
import sys
from PyQt5.QtGui import QIcon


def _getRoot():
    root = ''
    if sys.argv[0].lower().endswith('.exe'):
        root = os.path.dirname(sys.argv[0])
    elif getattr(sys, 'frozen', False):
        root = os.environ['RESOURCEPATH']
    else:
        file = None
        try:
            file = __file__
        except NameError:
            file = sys.argv[0]
        root = os.path.dirname(os.path.abspath(file))
    return root


def __getResourcesRoot():
    return os.path.join(_getRoot(), 'resources')


def getResourcePath(resource_name):
    return os.path.join(__getResourcesRoot(), resource_name)


def getIcon(resource_name):
    return QIcon(getResourcePath(resource_name))

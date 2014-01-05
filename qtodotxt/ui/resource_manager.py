import os
import sys
import platform
from PySide.QtGui import QIcon, QFontDatabase
from PySide.QtCore import QFile, QIODevice
from os import listdir

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

resources_root = __getResourcesRoot()

def getResourcePath(resource_name):
    return os.path.join(resources_root, resource_name)

def getIcon(resource_name):
    return QIcon(getResourcePath(resource_name))

def getFonts():
    font_dir = os.path.join(_getRoot(),'fonts')
    for ttf_filename in listdir(font_dir):
        ttf_path=os.path.join(font_dir,ttf_filename)
        if platform.system() == 'Windows':
            ttf_path = ttf_path.replace("\\","/")
        ttf_file = QFile(ttf_path)
        ttf_file.open(QIODevice.ReadOnly)
        byte_array = ttf_file.readAll()
        QFontDatabase.addApplicationFontFromData(byte_array)
        byte_array = ttf_file.readAll()
import sys
import os
from setuptools import setup

# ======================================
# Py2exe
# use "python setup.py py2exe" to generate a windows package
try:
    import py2exe
except ImportError:
    pass

# ======================================
current_dir = os.getcwd()
os.chdir(os.path.join('..', '..'))
sys.path.append(os.getcwd())

# Data files
icon = os.path.join(os.getcwd(),
                    'qtodotxt', 'ui', 'resources', 'qtodotxt.ico')

def collect_resources(resources_root,resources):					
    for file in os.listdir(resources_root):
        file_path=os.path.join(resources_root, file)
        if os.path.isfile(file_path):
            resources.append(file_path)
		
def collect_packages(path, package_name, packages, excludes=None):
    for dir in os.listdir(path):
        if excludes and dir in excludes:
            continue
        subpath = os.path.join(path, dir)
        if os.path.isdir(subpath):
            if os.path.exists(os.path.join(subpath, '__init__.py')):
                subpackage_name = dir
                if len(package_name) > 0:
                    subpackage_name = package_name + '.' + subpackage_name
                packages.append(subpackage_name)
                collect_packages(subpath, subpackage_name, packages)

packages = []
collect_packages('.', '', packages, excludes=['test'])

resources=[]
resources_root = os.path.join(os.getcwd(), 'qtodotxt', 'ui', 'resources')
collect_resources(resources_root,resources)

css=[]
resources_root = os.path.join(os.getcwd(), 'qtodotxt', 'ui', 'resources','css')
collect_resources(resources_root,css)
# ======================================
# Setup parameters
setup(name='qtodotxt',
      version='1.7',
      author='QTT Development Team',
      author_email='qtodotxt@googlegroups.com',
      url='https://github.com/QTodoTxt/QTodoTxt',
      packages=packages,
      setup_requires=["py2exe"],

      data_files=[
              ('resources', resources), 
# You need to adapt file paths below to fit your development settins/environment
# File paths are for WinPython-32bit-3.4.4.2Qt5 being installed in folder d:\Development\Python\QTodoTxt\WinPython-32bit-3.4.4.2Qt5
			  ('platforms',[r'c:\Qt\Qt5.5.1\5.5\mingw492_32\plugins\platforms\qwindows.dll']),
			  ('platforms',[r'c:\Qt\Qt5.5.1\5.5\mingw492_32\plugins\platforms\qoffscreen.dll']),
			  ('platforms',[r'c:\Qt\Qt5.5.1\5.5\mingw492_32\plugins\platforms\qminimal.dll']),
			  ('resources/css', css)
		  ],

      # py2exe parameters
      windows=[
          {
                "script": "bin/qtodotxt.pyw",
                "icon_resources": [(0, icon)]
          }
        ],
        options={
            "py2exe": {
                "includes": ["argparse", "sip"],
                "dist_dir": os.path.join(current_dir, 'dist')
            },
            "build": {
                "build_base": os.path.join(current_dir, 'build')
            },
        }
    )

import sys
import os
from setuptools import setup

# ======================================
# Py2exe
# use "python setup.py py2app" to generate a windows package
try:
    import py2app
except ImportError:
    pass

# ======================================
current_dir = os.getcwd()
os.chdir(os.path.join('..', '..'))
# Data files
resources = []
resources_root = os.path.join(os.getcwd(), 'qtodotxt', 'ui', 'resources')
for file in os.listdir(resources_root):
    resources.append(os.path.join(resources_root, file))

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

# ======================================
# Setup parameters
setup(name='qtodotxt',
      version='1.5.0',
      author='QTT Development Team',
      author_email='qtodotxt@googlegroups.com',
      url='https://github.com/QTodoTxt/QTodoTxt',
      packages=packages,
      app=["qtodotxt/app.py"],
      setup_requires=["py2app"],

      data_files=[('resources', resources)],

      options={
          "py2app": {
              "iconfile": "artwork/icon/icon.icns",
              "includes": ['PyQt5.QtCore', 'PyQt5.QtGui'],
              "resources": resources,
          },
          "build": {
              "build_base": os.path.join(current_dir, 'build')
          },
      }
    )

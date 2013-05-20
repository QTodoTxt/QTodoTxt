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
# allow py2exe find the required Visual C++ DLLs:
sys.path.append('C:\\Program Files\\Common Files\\Microsoft Shared\\VSTO\\10.0')

# ======================================
# Data files
resources = []
resources_root = os.path.join(os.path.dirname(__file__), 'qtodotxt', 'ui', 'resources')
for file in os.listdir(resources_root):
    resources.append(os.path.join(resources_root, file))

icon = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'qtodotxt', 'ui', 'resources', 'qtodotxt.ico')

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
        version='0.1.0',
        author='David Elentok',
        author_email='3david@gmail.com',
        url='http://www.bitbucket.org/3david/qtodotxt',
        packages=packages,
	app=["qtodotxt/app.py"],
        setup_requires=["py2app"],

        data_files=[
            ('resources', resources)],
        
        # py2exe parameters
        windows=[
            {
                "script": "bin/qtodotxt.pyw",
                "icon_resources": [(0, icon)]
            }
        ],
        options={
            "py2exe": {
                "includes": ["argparse"]
            },
	    "py2app": {
	        "iconfile": "artwork/icon/icon.icns",
		"includes": ['PySide.QtCore', 'PySide.QtGui'],
		"resources": resources,
	    },
        }
    )

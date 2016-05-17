from setuptools import setup, find_packages

import sys


setup(name="qtodotxt", 
      version="1.6.1",
      description="Cross Platform todo.txt GUI",
      author="QTT Development Team",
      author_email="qtodotxt@googlegroups.com",
      url='https://github.com/QTodoTxt/QTodoTxt',
      packages=find_packages(include=("*.png")) + ["qtodotxt.ui.resources", "qtodotxt.ui.resources.css"],
      package_data={"": ["*.png", "*.svg", "*.css"]},
      provides=["qtodotxt"],
      depends=["python-dateutil"],
      license="GNU General Public License v3 or later",
      #install_requires=install_requires,
      classifiers=["Environment :: X11 Applications :: Qt",
                   "Programming Language :: Python :: 3",
                   "Development Status :: 4 - Beta",
                   "Intended Audience :: End Users/Desktop",
                   "Operating System :: OS Independent",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
                   ],
      entry_points={'console_scripts': 
                    [
                        'qtodotxt = qtodotxt.app:run'
                    ]
                    }
      )


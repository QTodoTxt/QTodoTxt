from setuptools import setup, find_packages

import sys


setup(name="qtodotxt", 
      version="0.1.0beta",
      description="Cross Platform todo.txt GUI",
      author="many",
      author_email="olivier.roulet@gmail.com",
      url='https://github.com/QTodoTxt/QTodoTxt',
      packages=find_packages(include=("*.png")) + ["qtodotxt.ui.resources", "qtodotxt.ui.resources.css"],
      package_data={"": ["*.png", "*.svg", "*.css"]},
      provides=["qtodotxt"],
      license="GNU General Public License v3 or later",
      #install_requires=install_requires,
      classifiers=["Environment :: X11 Applications :: Qt",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 2",
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


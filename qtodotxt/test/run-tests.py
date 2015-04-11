#!/usr/bin/env python3

import os
import sys
import unittest

testsdir = os.path.abspath(os.path.dirname(__file__))
root = os.path.join(testsdir, '..', '..')
sys.path.insert(0, os.path.abspath(root))

tests = unittest.defaultTestLoader.discover('.', pattern='test*.py')

if __name__ == "__main__":
    try:
        from flake8 import main as flake8
        sys.argv.append(os.path.dirname(__file__))
        flake8.main()
    except (ImportError, SystemExit):
        pass

    if unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful():
        print("Test passed.")
        sys.exit(0)
    else:
        print("Test failed.")
        sys.exit(1)

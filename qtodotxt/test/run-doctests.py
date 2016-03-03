#!/usr/bin/env python3

import doctest
import os
from os import path
import sys

try:
    import PyQt5  # noqa
except ImportError:
    print("Couldn't import PyQt5. Aborting. These are the PYTHONPATHs:")
    print(sys.path)
    sys.exit(1)


testsdir = path.abspath(path.dirname(__file__))
root = path.abspath(path.join(testsdir, '..', '..'))
sys.path.insert(0, root)


def run_doctests(testsdir):
    exit_code = 0
    for filename in os.listdir(testsdir):
        fullname = path.join(testsdir, filename)
        if filename.endswith('.doctest'):
            print("- Running", fullname)
            result = doctest.testfile(fullname, module_relative=False)
            print("  => ran {0} results, {1} failed".format(result.attempted, result.failed))
            exit_code += result.failed
        elif path.isdir(fullname):
            exit_code += run_doctests(fullname)

    return exit_code

if __name__ == "__main__":
    exit_code = 0

    print("Running Doctests...")
    exit_code = run_doctests(testsdir)
    sys.exit(exit_code)

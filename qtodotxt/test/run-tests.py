import sys
import os
import unittest
import doctest

testsdir = os.path.abspath(os.path.dirname(__file__))
root = os.path.join(testsdir, '..', '..')
sys.path.insert(0, os.path.abspath(root))

tests = unittest.defaultTestLoader.discover('.', pattern='test*.py')

def run_doctests(testsdir):
    exit_code = 0
    for filename in os.listdir(testsdir):
        fullname = os.path.join(testsdir, filename)
        if filename.endswith('.doctest'):
            print "- Running", fullname
            result = doctest.testfile(fullname)
            print "  => ran {0} results, {1} failed".format(result.attempted, result.failed)
        elif os.path.isdir(fullname):
            exit_code = run_doctests(fullname)

    return exit_code

if __name__ == "__main__":
    exit_code = 0

    print "========================================"
    print "Running Unittests"
    print "========================================"
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit_code = 1

    print "========================================"
    print "Running Doctests"
    print "========================================"
    doctests_exit_code = run_doctests(testsdir)
    if exit_code == 0:
        exit_code = doctests_exit_code

    if exit_code == 0:
        print "========================================"
        print "Unit tests passed successfuly"
        print "========================================"
    else:
        print "========================================"
        print "Unit tests failed"
        print "========================================"


    sys.exit(exit_code)


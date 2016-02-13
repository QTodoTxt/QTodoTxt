import logging 
import os
import sys
import unittest

testsdir = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(testsdir, '..', '..'))
sys.path.insert(0, root)

print(sys.path)

from test_tasks import TestTasks

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    unittest.main(verbosity=3)

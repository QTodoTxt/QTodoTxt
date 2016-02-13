import unittest
from qtodotxt.lib.tasklib import Task


class TestTasks(unittest.TestCase):
    def test_completeness(self):
        self.assertEqual(Task('task1').is_complete, Task('task2').is_complete)
        self.assertEqual(Task('x task1').is_complete, Task('x task2').is_complete)
        self.assertNotEqual(Task('task').is_complete, Task('x task').is_complete)
        self.assertNotEqual(Task('x task').is_complete, Task('task').is_complete)
        self.assertGreater(Task('task'), Task('x task'))
        self.assertLess(Task('x task'), Task('task'))

    def test_priority(self):
        self.assertEqual(Task('task1').priority, Task('task2').priority)
        self.assertEqual(Task('(A) task1').priority, Task('(A) task2').priority)
        self.assertNotEqual(Task('(A) task').priority, Task('task').priority)
        self.assertGreater(Task('(A) task').priority, Task('(B) task').priority)
        self.assertGreater(Task('(Z) task').priority, Task('task').priority)
        self.assertLess(Task('(B) task').priority, Task('(A) task').priority)
        self.assertLess(Task('task').priority, Task('(D) task').priority)
        self.assertNotEqual(Task('(A) task1').priority, Task('(AA) task2').priority)
        self.assertEqual(Task('(1) task1').priority, Task('(1) task2').priority)

    def test_comparisons(self):
        self.assertEqual(Task('task'), Task('task'))
        self.assertEqual(Task('(A) task'), Task('(A) task'))

        #self.assertLess(Task('task1'), Task('task2'))
        self.assertLess(Task('x task'), Task('task'))
        self.assertGreater(Task('(A) task'), Task('(B) task'))
        self.assertGreater(Task('(A) task'), Task('task'))
        self.assertGreater(Task('(A) task'), Task('x (A) task'))

        #self.assertGreater(Task('task2'), Task('task1'))
        self.assertLess(Task('x task'), Task('task'))
        self.assertLess(Task('(B) task'), Task('(A) task'))
        self.assertLess(Task('task'), Task('(A) task'))
        self.assertLess(Task('x (A) task'), Task('(A) task'))

import unittest
from qtodotxt.lib.todolib import Task, TaskFeatures

class TestTaskCompletenessComparison(unittest.TestCase):
    @unittest.skip("Necessary methods are not implemented yet.")
    def test(self):
        self.assertEqual(Task('task1').is_complete, Task('task2').is_complete)
        self.assertEqual(Task('x task1').is_complete, Task('x task2').is_complete)
        self.assertNotEqual(Task('task').is_complete, Task('x task').is_complete)
        self.assertNotEqual(Task('x task').is_complete, Task('task').is_complete)
        self.assertGreater(Task('task').is_complete, Task('x task').is_complete)
        self.assertLess(Task('x task').is_complete, Task('task').is_complete)

class TestTaskPriorityComparison(unittest.TestCase):
    @unittest.skip("Necessary methods are not implemented yet.")
    def test(self):
        self.assertEqual(Task('task1').priority, Task('task2').priority)
        self.assertEqual(Task('(A) task1').priority, Task('(A) task2').priority)
        self.assertNotEqual(Task('(A) task').priotity, Task('task'))
        self.assertGreater(Task('(A) task'.priority, Task('(B) task').priority))
        self.assertGreater(Task('(Z) task'.priority), Task('task').priority)
        self.assertLess(Task('(B) task'.priority, Task('(A) task').priority))
        self.assertLess(Task('task').priority, Task('(Z) task'.priority))
        self.assertNotEqual(Task('(A) task1').priority, Task('(AA) task2').priority)
        self.assertNotEqual(Task('(1) task1').priority, Task('(1) task2').priority)

class TestTaskComparison(unittest.TestCase):
    @unittest.skip("Necessary methods are not implemented yet.")
    def test(self):
        self.assertEqual(Task('task'), Task('task'))
        self.assertEqual(Task('(A) task'), Task('(A) task'))

        self.assertLess(Task('task1'), Task('task2'))
        self.assertLess(Task('task'), Task('x task'))
        self.assertLess(Task('(A) task'), Task('(B) task'))
        self.assertLess(Task('(A) task'), Task('task'))
        self.assertLess(Task('(A) task'), Task('x (A) task'))

        self.assertGreater(Task('task2'), Task('task1'))
        self.assertGreater(Task('x task'), Task('task'))
        self.assertGreater(Task('(B) task'), Task('(A) task'))
        self.assertGreater(Task('task'), Task('(A) task'))
        self.assertGreater(Task('x (A) task'), Task('(A) task'))

class TestTaskNewline(unittest.TestCase):
    def test_01(self):
        features = TaskFeatures()
        features.multiline = False
        task = Task(r'this is my task \\ with additional description', features)
        self.assertEqual(task.editText, r'this is my task \\ with additional description')

    def test_02(self):
        features = TaskFeatures()
        features.multiline = True
        task = Task(r'this is my task \\ with additional description',features)
        self.assertEqual(task.editText, 'this is my task\nwith additional description')

    def test_03(self):
        features = TaskFeatures()
        features.multiline = True
        task = Task('this is my task \\ with additional description',features)
        self.assertEqual(task.editText, r'this is my task \ with additional description')

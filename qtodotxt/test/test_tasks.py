from datetime import date
import unittest
from qtodotxt.lib.tasklib import Task


class TestTasks(unittest.TestCase):

    def test_completeness_comparison(self):
        self.assertEqual(Task('task1').is_complete, Task('task2').is_complete)
        self.assertEqual(Task('x task1').is_complete, Task('x task2').is_complete)
        self.assertNotEqual(Task('task').is_complete, Task('x task').is_complete)
        self.assertNotEqual(Task('x task').is_complete, Task('task').is_complete)
        self.assertGreater(Task('task'), Task('x task'))
        self.assertLess(Task('x task'), Task('task'))

    def test_priority_comparison(self):
        # this tests are a bit broken now that priority is only a character
        self.assertEqual(Task('task1').priority, Task('task2').priority)
        self.assertEqual(Task('(A) task1').priority, Task('(A) task2').priority)
        self.assertNotEqual(Task('(A) task').priority, Task('task').priority)
        self.assertLess(Task('(A) task').priority, Task('(B) task').priority)
        self.assertGreater(Task('(B) task').priority, Task('(A) task').priority)
        self.assertNotEqual(Task('(A) task1').priority, Task('(AA) task2').priority)
        self.assertEqual(Task('(1) task1').priority, Task('(1) task2').priority)

    def test_comparisons_comparison(self):
        self.assertEqual(Task('task'), Task('task'))
        self.assertEqual(Task('(A) task'), Task('(A) task'))

        # self.assertLess(Task('task1'), Task('task2'))
        self.assertLess(Task('x task'), Task('task'))
        self.assertGreater(Task('(A) task'), Task('(B) task'))
        self.assertGreater(Task('(A) task'), Task('task'))
        self.assertGreater(Task('(A) task'), Task('x (A) task'))

        # self.assertGreater(Task('task2'), Task('task1'))
        self.assertLess(Task('x task'), Task('task'))
        self.assertLess(Task('(B) task'), Task('(A) task'))
        self.assertLess(Task('task'), Task('(A) task'))
        self.assertLess(Task('x (A) task'), Task('(A) task'))

    def test_task_ordering(self):
        task1 = Task('x task1')
        task2 = Task('task2')
        task3 = Task('abc task2')
        task4 = Task('(D) task2')
        task5 = Task('(C) b task')
        task6 = Task('(C) a task')
        task7 = Task('(B) task2')
        task8 = Task('(A) task2')
        self.assertTrue(task2 < task3)
        self.assertTrue(task1 < task2 < task3 < task4 < task5 < task6 < task7 < task8)
        l = [task1, task2, task3, task4, task5, task6, task7, task8]
        l2 = [task2, task3, task1, task4, task5, task6, task7, task8]
        self.assertFalse(l == l2)
        l2.sort()
        self.assertTrue(l == l2)

    def test_priority(self):
        self.assertEqual(Task("task").priority, "")
        self.assertEqual(Task("(a) task").priority, "")
        self.assertEqual(Task("x (a) task").priority, "")
        self.assertEqual(Task("x 2016-03-12 task").priority, "")
        self.assertEqual(Task("(A) task").priority, "A")
        t = Task("(A) task")
        self.assertEqual(t.priority, "A")
        t.increasePriority()
        self.assertEqual(t.priority, "A")
        t.decreasePriority()
        self.assertEqual(t.priority, "B")
        t.decreasePriority()
        t.decreasePriority()
        self.assertEqual(t.priority, "D")
        self.assertEqual(t.text, "(D) task")
        t.decreasePriority()
        self.assertEqual(t.priority, "")
        self.assertEqual(t.text, "task")

        t.increasePriority()
        t.increasePriority()
        self.assertEqual(t.priority, "C")
        for i in range(20):
            t.increasePriority()
        self.assertEqual(t.priority, "A")
        for i in range(20):
            t.decreasePriority()
        self.assertEqual(t.priority, "")

        # this task i wrongly formated, x should be followed by adate
        # self.assertEqual(Task("x (A) task").priority, Priority("A"))

        # A task with a priority lower than our default minimal priority
        t = Task("(M) task")
        t.increasePriority()
        self.assertEqual(t.priority, "L")
        t.decreasePriority()
        self.assertEqual(t.priority, "")

    def test_basic(self):
        task = Task('do something')
        self.assertEqual(task.text, 'do something')
        self.assertEqual(len(task.contexts), 0)
        self.assertFalse(len(task.projects), 0)
        self.assertFalse(task.is_complete)
        self.assertFalse(task.priority)

        task = Task('do something @context1 @context2')
        self.assertEqual(task.contexts, ['context1', 'context2'])
        self.assertEqual(task.projects, [])
        self.assertFalse(task.is_complete)
        self.assertFalse(task.priority)

        task = Task('do something +project1 +project2')
        self.assertEqual(task.contexts, [])
        self.assertEqual(task.projects, ['project1', 'project2'])
        self.assertFalse(task.is_complete)
        self.assertFalse(task.priority)

        task = Task('(E) do something +project1 @context1 +project2 rest of line @context2')
        self.assertEqual(task.contexts, ['context1', 'context2'])
        self.assertEqual(task.projects, ['project1', 'project2'])
        self.assertFalse(task.is_complete)
        self.assertTrue(task.priority)
        self.assertEqual(task.text, '(E) do something +project1 @context1 +project2 rest of line @context2')

        # task with + alone and complete
        task = Task('x 2016-01-23 do something +project1 @context1 +project2 rest + of line @context2')
        self.assertEqual(task.contexts, ['context1', 'context2'])
        self.assertEqual(task.projects, ['project1', 'project2'])
        self.assertTrue(task.is_complete)
        self.assertFalse(task.priority)
        self.assertEqual(task.completion_date, date(2016, 1, 23))

    def test_completion(self):
        task = Task('(B) something +project1 @context1 pri:C')
        self.assertEqual(task.contexts, ['context1'])
        self.assertEqual(task.projects, ['project1'])
        self.assertFalse(task.is_complete)
        self.assertEqual(task.priority, 'B')
        self.assertEqual(len(task.keywords), 1)

        task.setCompleted()
        self.assertTrue(task.is_complete)
        self.assertEqual(task.completion_date, date.today())
        self.assertTrue(task.text.startswith("x "))

        task.setPending()
        self.assertFalse(task.is_complete)
        self.assertFalse(task.completion_date)

    def test_future(self):
        task = Task('(D) do something +project1 t:2030-10-06')
        self.assertEqual(task.contexts, [])
        self.assertEqual(task.projects, ['project1'])
        self.assertFalse(task.is_complete)
        self.assertTrue(task.priority)
        self.assertTrue(task.is_future)

    def test_custom_keywords(self):
        task = Task('(B) do something +project1 mykey:myval titi:toto @context1 rest + of line pri:C')
        self.assertEqual(task.contexts, ['context1'])
        self.assertEqual(task.projects, ['project1'])
        self.assertFalse(task.is_complete)
        self.assertEqual(task.priority, 'B')
        self.assertEqual(len(task.keywords), 3)
        self.assertIn("titi", task.keywords)
        self.assertEqual(task.keywords['pri'], "C")

    def test_creation_date(self):
        task = Task('(B) 2016-03-15 do something +project1 mykey:myval titi:toto @context1 rest + of line pri:C')
        self.assertTrue(task.creation_date)
        self.assertEqual(task.creation_date, date(2016, 3, 15))
        task = Task('2016-03-15 do something')
        self.assertTrue(task.creation_date)
        self.assertEqual(task.creation_date, date(2016, 3, 15))
        task = Task('do something')
        self.assertFalse(task.creation_date)
        task = Task('(A) do something')
        self.assertFalse(task.creation_date)
        task = Task('x 2017-08-12 2016-03-15 do something')
        self.assertTrue(task.creation_date)
        self.assertEqual(task.creation_date, date(2016, 3, 15))
        task = Task('x 2017-08-12 do something')
        self.assertFalse(task.creation_date)

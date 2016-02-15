import unittest
from qtodotxt.lib.tasklib import Task, Priority


class TestTasks(unittest.TestCase):

    def test_completeness_comparison(self):
        self.assertEqual(Task('task1').is_complete, Task('task2').is_complete)
        self.assertEqual(Task('x task1').is_complete, Task('x task2').is_complete)
        self.assertNotEqual(Task('task').is_complete, Task('x task').is_complete)
        self.assertNotEqual(Task('x task').is_complete, Task('task').is_complete)
        self.assertGreater(Task('task'), Task('x task'))
        self.assertLess(Task('x task'), Task('task'))

    def test_priority_comparison(self):
        self.assertEqual(Task('task1').priority, Task('task2').priority)
        self.assertEqual(Task('(A) task1').priority, Task('(A) task2').priority)
        self.assertNotEqual(Task('(A) task').priority, Task('task').priority)
        self.assertGreater(Task('(A) task').priority, Task('(B) task').priority)
        self.assertGreater(Task('(Z) task').priority, Task('task').priority)
        self.assertLess(Task('(B) task').priority, Task('(A) task').priority)
        self.assertLess(Task('task').priority, Task('(D) task').priority)
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
        self.assertEqual(Task("task").priority, Priority())
        self.assertEqual(Task("(a) task").priority, Priority())
        self.assertEqual(Task("x (a) task").priority, Priority())
        self.assertEqual(Task("(A) task").priority, Priority("A"))
        t = Task("(A) task")
        self.assertEqual(t.priority, Priority("A"))
        t.priority += 1
        self.assertEqual(t.priority, Priority("A"))
        t.priority -= 1
        self.assertEqual(t.priority, Priority("B"))
        t.priority -= 2
        self.assertEqual(t.priority, Priority("D"))
        self.assertEqual(t.text, "(D) task")
        t.priority -= 1
        self.assertEqual(t.priority, Priority())
        self.assertEqual(t.text, "task")

        t.priority += 2
        self.assertEqual(t.priority, Priority("C"))
        t.priority += 5
        self.assertEqual(t.priority, Priority("A"))
        t.priority -= 100
        self.assertEqual(t.priority, Priority(""))

        # this test is controversial, what should be the correct behaviour?
        self.assertEqual(Task("x (A) task").priority, Priority("A"))

        # A task with a priority lower than our default minimal priority
        t = Task("(M) task")
        t.priority += 1
        self.assertEqual(t.priority, Priority("L"))
        t.priority -= 1
        self.assertEqual(t.priority, Priority(""))

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

        # task with + alone and complete
        task = Task('x do something +project1 @context1 +project2 rest + of line @context2')
        self.assertEqual(task.contexts, ['context1', 'context2'])
        self.assertEqual(task.projects, ['project1', 'project2'])
        self.assertTrue(task.is_complete)
        self.assertFalse(task.priority)

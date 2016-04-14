import unittest
from tempfile import mkstemp
from os import remove
from datetime import date, timedelta
from sys import version

from qtodotxt.lib.file import File, ErrorLoadingFile
from qtodotxt.lib.tasklib import Task


PYTHON_VERSION = version[:3]


if PYTHON_VERSION < '3.3':
    FileNotFoundError = BaseException


class TestFile(unittest.TestCase):
    def setUp(self):
        self.file = File()
        self.tmpfile = mkstemp(text=True)[1]

    def tearDown(self):
        try:
            remove(self.tmpfile)
        except FileNotFoundError:
            pass
        except OSError as ex:    # maintain compatibility with Python 3.2
            if ex.errno != 2:
                raise
        except:
            raise

    def saveAndReload(self):
        self.file.save(self.tmpfile)
        self.file = File()
        self.file.load(self.tmpfile)

    def test_single_task(self):
        text = 'due:1999-10-10 do something +project1 @context1'
        self.file.tasks.append(Task(text))
        self.saveAndReload()
        self.assertEqual(self.file.tasks[0].text, text)
        self.assertEqual(self.file.tasks[0].contexts, ['context1'])
        self.assertEqual(self.file.tasks[0].projects, ['project1'])
        self.assertFalse(self.file.tasks[0].is_complete)
        self.assertFalse(self.file.tasks[0].priority)
        self.assertEqual(self.file.tasks[0].due, date(1999, 10, 10))

    def test_two_tasks(self):
        task1 = 'do something +project1 @context1'
        task2 = '(A) do something else +project1 @context2'
        self.file.tasks.extend([
            Task(task1),
            Task(task2)
        ])
        self.saveAndReload()
        self.assertEqual(self.file.tasks[0].text, task2)
        self.assertEqual(self.file.tasks[1].text, task1)

    def test_five_tasks(self):
        task1 = Task('do something +project1 @context1')
        task2 = Task('(A) do something else +project1 @context2')
        task3 = Task('do something else +project1 @context2')
        task4 = Task('something else +project1 @context2')
        task5 = Task('abc +project1 @context2')
        self.file.tasks.extend([task1, task2, task3, task4, task5])
        self.saveAndReload()
        self.assertEqual(self.file.tasks[0].text, task2.text)
        self.assertEqual(self.file.tasks[1].text, task5.text)
        self.assertEqual(self.file.tasks[2].text, task1.text)
        self.assertEqual(self.file.tasks[3].text, task3.text)
        self.assertEqual(self.file.tasks[4].text, task4.text)

    def test_get_all_contexts(self):
        self.file.tasks.extend([
            Task('x task with @context1'),
            Task('task with @context2'),
            Task('task with @context1 and @context2'),
            Task('task with @context1 and @context2 and @context3')
        ])
        self.saveAndReload()
        self.assertEqual(self.file.getAllContexts(), {'context1': 2, 'context2': 3, 'context3': 1})

    def test_get_all_incl_completed_contexts(self):
        self.file.tasks.extend([
            Task('x task with @context1'),
            Task('task with @context2'),
            Task('task with @context1 and @context2'),
            Task('x task with @context1 and @context2 and @context3')
        ])
        self.saveAndReload()
        self.assertEqual(self.file.getAllContexts(True), {'context1': 1, 'context2': 2, 'context3': 0})

    def test_get_all_projects(self):
        self.file.tasks.extend([
            Task('x task with +project1'),
            Task('task with +project2'),
            Task('task with +project1 and +project2'),
            Task('task with +project1 and +project2 and +project3')
        ])
        self.saveAndReload()
        self.assertEqual(self.file.getAllProjects(), {'project1': 2, 'project2': 3, 'project3': 1})

    def test_get_all_due_ranges(self):
        today = date.today().strftime('%Y-%m-%d')
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        self.file.tasks.extend([
            Task('x due:' + today + ' completed task of today'),
            Task('due:' + today + ' first task of today'),
            Task('due:' + today + ' second task of today'),
            Task('due:' + yesterday + ' task of yesterday'),
        ])
        self.saveAndReload()
        self.assertEqual(self.file.getAllDueRanges()[0], {'Today': 2, 'This week': 2, 'This month': 2, 'Overdue': 1})
        self.assertIsInstance(self.file.getAllDueRanges()[1], dict)

    def test_get_all_projects_incl_completed(self):
        self.file.tasks.extend([
            Task('x task with +project1'),
            Task('task with +project2'),
            Task('task with +project1 and +project2'),
            Task('x task with +project1 and +project2 and +project3')
        ])
        self.saveAndReload()
        self.assertEqual(self.file.getAllProjects(True), {'project1': 1, 'project2': 2, 'project3': 0})

    def test_load_empty_filename(self):
        self.assertRaises(ErrorLoadingFile, self.file.load, '')

    def test_load_nonexisting_file(self):
        remove(self.tmpfile)
        self.assertRaises(ErrorLoadingFile, self.file.load, self.tmpfile)

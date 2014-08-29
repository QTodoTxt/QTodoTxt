import unittest
from tempfile import mkstemp
from os import remove
from qtodotxt.lib.file import File, ErrorLoadingFile
from qtodotxt.lib.todolib import Task
from sys import version


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

    def saveAndReaload(self):
        self.file.save(self.tmpfile)
        self.file = File()
        self.file.load(self.tmpfile)

    def test_single_task(self):
        text = 'do something +project1 @context1'
        self.file.tasks.append(Task(text))
        self.saveAndReaload()
        self.assertEqual(self.file.tasks[0].text, text)
        self.assertEqual(self.file.tasks[0].contexts, ['context1'])
        self.assertEqual(self.file.tasks[0].projects, ['project1'])
        self.assertEqual(self.file.tasks[0].is_complete, False)
        self.assertEqual(self.file.tasks[0].priority, None)

    def test_two_tasks(self):
        task1 = 'do something +project1 @context1'
        task2 = '(A) do something else +project1 @context2'
        self.file.tasks.extend([
            Task(task1),
            Task(task2)
        ])
        self.saveAndReaload()
        self.assertEqual(self.file.tasks[0].text, task2)
        self.assertEqual(self.file.tasks[1].text, task1)

    def test_five_tasks(self):
        task1 = Task('do something +project1 @context1')
        task2 = Task('(A) do something else +project1 @context2')
        task3 = Task('do something else +project1 @context2')
        task4 = Task('something else +project1 @context2')
        task5 = Task('abc +project1 @context2')
        self.file.tasks.extend([task1, task2, task3, task4, task5])
        self.saveAndReaload()
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
        self.saveAndReaload()
        self.assertEqual(self.file.getAllContexts(), {'context1': 2, 'context2': 3, 'context3': 1})

    def test_get_all_completed_contexts(self):
        self.file.tasks.extend([
            Task('x task with @context1'),
            Task('task with @context2'),
            Task('task with @context1 and @context2'),
            Task('x task with @context1 and @context2 and @context3')
        ])
        self.saveAndReaload()
        self.assertEqual(self.file.getAllCompletedContexts(), {'context1': 2, 'context2': 1, 'context3': 1})

    def test_get_all_projects(self):
        self.file.tasks.extend([
            Task('x task with +project1'),
            Task('task with +project2'),
            Task('task with +project1 and +project2'),
            Task('task with +project1 and +project2 and +project3')
        ])
        self.saveAndReaload()
        self.assertEqual(self.file.getAllProjects(), {'project1': 2, 'project2': 3, 'project3': 1})

    def test_get_all_completed_projects(self):
        self.file.tasks.extend([
            Task('x task with +project1'),
            Task('task with +project2'),
            Task('task with +project1 and +project2'),
            Task('x task with +project1 and +project2 and +project3')
        ])
        self.saveAndReaload()
        self.assertEqual(self.file.getAllCompletedProjects(), {'project1': 2, 'project2': 1, 'project3': 1})

    def test_load_empty_filename(self):
        self.assertRaises(ErrorLoadingFile, self.file.load, '')

    def test_load_nonexisting_file(self):
        remove(self.tmpfile)
        self.assertRaises(ErrorLoadingFile, self.file.load, self.tmpfile)

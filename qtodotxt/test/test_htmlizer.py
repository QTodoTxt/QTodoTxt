from qtodotxt.lib import task_htmlizer, tasklib
import unittest


class TestHtmlizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.htmlizer = task_htmlizer.TaskHtmlizer()

    def test_01(self):
        # Simple task should return simple html
        task = tasklib.Task('this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task')

    def test_02(self):
        # Test task with a single context at the end
        task = tasklib.Task('this is my task @context')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <font color="green">@context</font>')

    def test_03(self):
        # Test task with a single context at the center
        task = tasklib.Task('this is my task @context and some more words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font color="green">@context</font> and some more words')

    def test_04(self):
        # Test task with a single project at the end
        task = tasklib.Task('this is my task +project')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:#64AAD0">+project</font>')

    def test_05(self):
        # Test task with a single project at the center
        task = tasklib.Task('this is my task +project and some more words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:#64AAD0">+project</font> and '
                         'some more words')

    def test_06(self):
        # Test task with a single context and a single project
        task = tasklib.Task('this is my task @context and +project and some more words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font color="green">@context</font> and '
                         '<font style="color:#64AAD0">+project</font> and some more words')

    def test_07(self):
        # Test task with a two contexts and a three projects
        task = tasklib.Task('this is my task @context1 and @context2 and '
                            '+project1 +project2 and +project3 some more '
                            'words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font color="green">@context1</font> and '
                         '<font color="green">@context2</font> and '
                         '<font style="color:#64AAD0">+project1</font> '
                         '<font style="color:#64AAD0">+project2</font> and '
                         '<font style="color:#64AAD0">+project3</font>'
                         ' some more words')

    def test_08(self):
        # Test task with priority A
        task = tasklib.Task('(A) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font color="red"><tt>(A)</tt>&nbsp;</font>this is my task')

    def test_09(self):
        # Test task with priority B
        task = tasklib.Task('(B) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font color="green"><tt>(B)</tt>&nbsp;</font>this is my task')

    def test_10(self):
        # Test task with priority C
        task = tasklib.Task('(C) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font color="navy"><tt>(C)</tt>&nbsp;</font>this is my task')

    def test_11(self):
        # Test task with priority D
        task = tasklib.Task('(D) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>(D)</tt>&nbsp;this is my task')

    def test_12(self):
        # Test task with an invalid due date
        task = tasklib.Task('this is my task due:abc')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:abc Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_13(self):
        # Test task with an invalid due date
        task = tasklib.Task('this is my task due:2014-04')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-04 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_14(self):
        # Test task with an invalid due month
        task = tasklib.Task('this is my task due:2014-13-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-13-01 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_15(self):
        # Test task with an invalid due day
        task = tasklib.Task('this is my task due:2014-04-31')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-04-31 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_16(self):
        # Test task with an invalid threshold date
        task = tasklib.Task('this is my task t:abc')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:abc Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_17(self):
        # Test task with an invalid threshold date
        task = tasklib.Task('this is my task t:2014-04')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_18(self):
        # Test task with an invalid threshold month
        task = tasklib.Task('this is my task t:2014-13-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-13-01 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_19(self):
        # Test task with an invalid threshold day
        task = tasklib.Task('this is my task t:2014-04-31')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04-31 Invalid date format, '
                         'expected YYYY-MM-DD. ***</font></b>')

    def test_20(self):
        # Test task with an URL
        task = tasklib.Task('Download https://github.com/mNantern/QTodoTxt/archive/master.zip and extract')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;Download '
                         '<a href="https://github.com/mNantern/QTodoTxt/archive/master.zip">'
                         'https://github.com/mNantern/QTodoTxt/archive/master.zip</a> and extract')

    def test_21(self):
        # Test task with solely an URL
        task = tasklib.Task('https://github.com/mNantern/QTodoTxt/archive/master.zip')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;'
                         '<a href="https://github.com/mNantern/QTodoTxt/archive/master.zip">'
                         'https://github.com/mNantern/QTodoTxt/archive/master.zip</a>')

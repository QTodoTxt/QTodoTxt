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
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <font style="color:green">@context</font>')

    def test_03(self):
        # Test task with a single context at the center
        task = tasklib.Task('this is my task @context and some more words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:green">@context</font> and some more words')

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
                         '<font style="color:green">@context</font> and '
                         '<font style="color:#64AAD0">+project</font> and some more words')

    def test_07(self):
        # Test task with a two contexts and a three projects
        task = tasklib.Task('this is my task @context1 and @context2 and '
                            '+project1 +project2 and +project3 some more '
                            'words')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:green">@context1</font> and '
                         '<font style="color:green">@context2</font> and '
                         '<font style="color:#64AAD0">+project1</font> '
                         '<font style="color:#64AAD0">+project2</font> and '
                         '<font style="color:#64AAD0">+project3</font>'
                         ' some more words')

    def test_08(self):
        # Test task with priority A
        task = tasklib.Task('(A) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font style="color:red"><tt>(A)</tt>&nbsp;</font>this is my task')

    def test_09(self):
        # Test task with priority B
        task = tasklib.Task('(B) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font style="color:green"><tt>(B)</tt>&nbsp;</font>this is my task')

    def test_10(self):
        # Test task with priority C
        task = tasklib.Task('(C) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<font style="color:navy"><tt>(C)</tt>&nbsp;</font>this is my task')

    def test_11(self):
        # Test task with priority D
        task = tasklib.Task('(D) this is my task')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>(D)</tt>&nbsp;this is my task')

    def test_12(self):
        # Test task with a valid due date
        task = tasklib.Task('this is my task due:2014-04-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01</font></b>')

    def test_13(self):
        # Test task with a valid due date and time
        task = tasklib.Task('this is my task due:2014-04-01T12:34')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01 12:34</font></b>')

    def test_14(self):
        # Test task with an invalid due date
        task = tasklib.Task('this is my task due:abc')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:abc Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_15(self):
        # Test task with an invalid due date
        task = tasklib.Task('this is my task due:2014-04')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-04 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_16(self):
        # Test task with an invalid due month
        task = tasklib.Task('this is my task due:2014-13-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-13-01 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_17(self):
        # Test task with an invalid due day
        task = tasklib.Task('this is my task due:2014-04-31')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-04-31 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_18(self):
        # Test task with space in due time instead of T. This is valid, but gives an unexpected result
        task = tasklib.Task('this is my task due:2014-04-01 12:34')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01</font></b> 12:34')

    def test_19(self):
        # Test task with a valid due time corner case
        task = tasklib.Task('this is my task due:2014-04-01T00:00')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01</font></b>')

    def test_20(self):
        # Test task with a valid due time corner case
        task = tasklib.Task('this is my task due:2014-04-01T00:01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01 00:01</font></b>')

    def test_21(self):
        # Test task with a valid due time corner case
        task = tasklib.Task('this is my task due:2014-04-01T23:59')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">due:2014-04-01 23:59</font></b>')

    def test_22(self):
        # Test task with an invalid due time corner case
        task = tasklib.Task('this is my task due:2014-04-01T24:00')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** due:2014-04-01T24:00 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_23(self):
        # Test task with a valid threshold date
        task = tasklib.Task('this is my task t:2014-04-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:orange">t:2014-04-01</font>')

    def test_24(self):
        # Test task with a valid threshold date and time
        task = tasklib.Task('this is my task t:2014-04-01T12:34')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task '
                         '<font style="color:orange">t:2014-04-01 12:34</font>')

    def test_25(self):
        # Test task with an invalid threshold date
        task = tasklib.Task('this is my task t:abc')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:abc Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_26(self):
        # Test task with an invalid threshold date
        task = tasklib.Task('this is my task t:2014-04')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_27(self):
        # Test task with an invalid threshold month
        task = tasklib.Task('this is my task t:2014-13-01')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-13-01 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_28(self):
        # Test task with an invalid threshold day
        task = tasklib.Task('this is my task t:2014-04-31')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04-31 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_29(self):
        # Test task with an invalid threshold hour
        task = tasklib.Task('this is my task t:2014-04-31T99:34')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04-31T99:34 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_30(self):
        # Test task with an invalid threshold minute
        task = tasklib.Task('this is my task t:2014-04-31T12:99')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;this is my task <b>'
                         '<font style="color:red">*** t:2014-04-31T12:99 Invalid date format, '
                         'expected yyyy-mm-dd or yyyy-mm-ddThh:mm. ***</font></b>')

    def test_31(self):
        # Test task with an URL
        task = tasklib.Task('Download https://github.com/mNantern/QTodoTxt/archive/master.zip and extract')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;Download '
                         '<a style="color:none;" href="https://github.com/mNantern/QTodoTxt/archive/master.zip">'
                         'https://github.com/...</a> and extract')

    def test_32(self):
        # Test task with solely an URL
        task = tasklib.Task('https://github.com/mNantern/QTodoTxt/archive/master.zip')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;'
                         '<a style="color:none;" href="https://github.com/mNantern/QTodoTxt/archive/master.zip">'
                         'https://github.com/...</a>')

    def test_33(self):
        # Test task with an URL in context
        task = tasklib.Task('Test @https://github.com/mNantern/QTodoTxt/')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;Test <font style="color:green">'
                         '@<a style="color:green;" href="https://github.com/mNantern/QTodoTxt/">'
                         'https://github.com/...</a></font>')

    def test_34(self):
        # Test task with an URL in project
        task = tasklib.Task('Test +https://github.com/mNantern/QTodoTxt/')
        self.assertEqual(self.htmlizer.task2html(task),
                         '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;Test <font style="color:#64AAD0">'
                         '+<a style="color:#64AAD0;" href="https://github.com/mNantern/QTodoTxt/">'
                         'https://github.com/...</a></font>')

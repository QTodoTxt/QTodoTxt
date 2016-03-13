import re
from datetime import datetime, timedelta


class BaseFilter(object):
    """
    The abstract base class for different kind of task-list filters.

    """
    def __init__(self, text):
        """
        Initialize a new BaseFilter objects.

        The required text argument (str) becomes the "text" instance attribute
        of the object.

        """
        self.text = text

    def __str__(self):
        return "Filter:{}".format(self.__class__.__name__)
    __repr__ = __str__

    def isMatch(self, task):
        """
        Determine whether the supplied task (arg 'task') satisfies the filter.

        In this base class, the test always returns True.

        """
        return True

    def __eq__(self, other):
        """
        Evaluates objects as equal if their type and self.text attr are the same.

        """
        if not other:
            return False
        if type(other) == type(self):
            return self.text == other.text
        return False


class AllTasksFilter(BaseFilter):
    """
    Task list filter that returns all tasks.

    """
    def __init__(self):
        BaseFilter.__init__(self, 'All')


class IncompleteTasksFilter(BaseFilter):
    """
    Task list filter that removes any completed tasks.

    """
    def __init__(self):
        BaseFilter.__init__(self, 'Incomplete')

    def isMatch(self, task):
        return not task.is_complete


class UncategorizedTasksFilter(BaseFilter):
    """
    Task list filter permitting incomplete tasks without project or context.

    """
    def __init__(self):
        BaseFilter.__init__(self, 'Uncategorized')

    def isMatch(self, task):
        return (not task.contexts) and (not task.projects)


class CompleteTasksFilter(BaseFilter):
    """
    Task list filter that removes any uncompleted tasks from the list.

    """
    def __init__(self):
        BaseFilter.__init__(self, 'Complete')

    def isMatch(self, task):
        return task.is_complete


class ContextFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected context.

    """

    def __init__(self, context):
        BaseFilter.__init__(self, context)

    def isMatch(self, task):
        return self.text in task.contexts

    def __str__(self):
        return "ContextFilter(%s)" % self.text


class ProjectFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected project.

    """
    def __init__(self, project):
        BaseFilter.__init__(self, project)

    def isMatch(self, task):
        return self.text in task.projects

    def __str__(self):
        return "ProjectFilter(%s)" % self.text


class DueFilter(BaseFilter):
    """
    Due list filter for ranges

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        return self.text in task.dueRanges

    def __str__(self):
        return "DueFilter(%s)" % self.text


class DueTodayFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks that are due today.

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        if (not task.due):
            return False
        else:
            self.due_date = task.due
            today = datetime.today().date()
            return self.due_date == today

    def __str__(self):
        return "DueTodayFilter(%s)" % self.text


class DueTomorrowFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks that are due tomorrow.

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        if not task.due:
            return False
        else:
            due_date = task.due
            today = datetime.today().date()
            return today < due_date <= today + timedelta(days=1)

    def __str__(self):
        return "DueTomorrowFilter(%s)" % self.text


class DueThisWeekFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks that are due this week.

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        if not task.due:
            return False
        else:
            due_date = task.due
            today = datetime.today().date()
            return today <= due_date <= today + timedelta((6 - today.weekday()) % 7)

    def __str__(self):
        return "DueThisWeekFilter(%s)" % self.text


class DueThisMonthFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks that are due this month.

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        if not task.due:
            return False
        else:
            due_date = task.due
            today = datetime.today().date()
            if today.month == 12:
                last_day_of_month = today.replace(day=31)
            else:
                last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            return today <= due_date <= last_day_of_month

    def __str__(self):
        return "DueThisMonthFilter(%s)" % self.text


class DueOverdueFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks that are overdue.

    """
    def __init__(self, dueRange):
        BaseFilter.__init__(self, dueRange)

    def isMatch(self, task):
        if not task.due:
            return False
        else:
            if not task.due:
                return False
            else:
                due_date = task.due
                today = datetime.today().date()
                return due_date < today

    def __str__(self):
        return "DueOverdueFilter(%s)" % self.text


class HasProjectsFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected project.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'Projects')

    def isMatch(self, task):
        return task.projects

    def __str__(self):
        return "HasProjectsFilter" % self.text


class HasContextsFilter(BaseFilter):
    """
    Task list filter allowing only tasks tagged with some project.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'Contexts')

    def isMatch(self, task):
        return task.contexts

    def __str__(self):
        return "HasContextsFilter" % self.text


class HasDueDateFilter(BaseFilter):
    """
    Task list filter allowing only complete tasks with due date in due ranges.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'DueRange')

    def isMatch(self, task):
        return task.due

    def __str__(self):
        return "HasDueDateFilter" % self.text


class HasDueRangesFilter(BaseFilter):
    """
    Task list filter allowing only complete tasks with due date in due ranges.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'DueRange')

    def isMatch(self, task):
        return task.dueRanges

    def __str__(self):
        return "HasDueRangesFilter" % self.text


def simpleTextFilterRepl(matchObj):
    """
    Return a search string based on the matchObj

    Replace function used in SimpleTextFilter isMatch, needed to allow for inverted(not) searching

    """
    if(matchObj.group(1)):
        return "^(?!.*" + matchObj.group(2) + ")"
    else:
        return "^(?=.*" + matchObj.group(2) + ")"


class SimpleTextFilter(BaseFilter):
    """
    Task list filter allowing only tasks whose string matches a filter string.

    This filter allows for basic and/or/not conditions in the filter string.
    For the syntax see SimpleTextFilter.isMatch.

    """

    def __init__(self, text):
        BaseFilter.__init__(self, text)

    def isMatch(self, task):
        """
        Return a boolean based on whether the supplied task satisfies self.text.

        This filter can handle basic and/or/not conditions. The syntax is as
        follows:

        :AND   :   ',' or whitespace (' ')
        :OR    :   '|'
        :NOT   :   prefixed '~' or '!'

        These operators follow the following order of precedence: OR, AND, NOT.
        So, for example:

        :'work job1 | home':                Either  (matches 'work'
                                                     AND 'job1')
                                            OR      (matches 'home')

        :'norweigan blue ~dead | !parrot':  Either  (matches 'norweigan'
                                                     AND 'blue'
                                                     AND does NOT match 'dead')
                                            OR      (does NOT match 'parrot')

        Since the python re module is used, most of the escaped regex
        characters will also work when attached to one of the (comma- or space-
        delimited) strings. E.g.:
        - \bcleese\b will match 'cleese' but not 'johncleese'
        - 2014-\d\d-07 will match '2014-03-07' but not '2014-ja-07'

        The method can handle parentheses in the search strings. Unlike most
        regex characters, these don't need to be escaped since they are escaped
        automatically. So the search string '(B)' will match '(B) nail its
        feet to the perch'.
        """
        mymatch = False
        comp = re.compile(r'\s*([\!~])?([\(\)\w\\\-]+)[\s,]*', re.U)
        restring = comp.sub(simpleTextFilterRepl, self.text, re.U)
        try:
            if ')' in restring:
                raise re.error('')  # otherwise adding closing parenth avoids error here
            mymatch = re.search(restring, task.text, re.I | re.U)
        except re.error:
            comp2 = re.compile(r'\s*\((?=[^?])', re.U)
            restring2 = comp2.sub(r'\\(', restring, re.U)
            comp3 = re.compile(r'(?<!\))\)(?=\))', re.U)
            restring3 = comp3.sub(r'\\)', restring2, re.U)
            mymatch = re.search(restring3, task.text, re.I | re.U)

        return mymatch

    def __str__(self):
        return "SimpleTextFilter({})".format(self.text)


class FutureFilter(BaseFilter):

    def __init__(self):
        BaseFilter.__init__(self, 'Future')

    def isMatch(self, task):
        return not task.is_future

    def __str__(self):
        return "FutureFilter " % self.text

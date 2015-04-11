from datetime import datetime, timedelta
from qtodotxt.lib.task import Task
import re
from weakref import WeakSet


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

    def __eq__(self, other):
        """
        Evaluates objects as equal if their type and self.text attr are the same.

        """
        if not other:
            return False
        if type(other) == type(self):
            return self.text == other.text
        return False

    def isMatch(self, task):
        """
        Determine whether the supplied task (arg 'task') satisfies the filter.
        """
        raise NotImplementedError('A filter-class must implement an isMatch- or a matches-method.')

    def matches(self, tasks=Task.all_tasks):
        """
        Returns a set of all matching items from a given iterable.
        Should be overridden in subclasses to make use of indexes and set operations.
        :param: A set containing Task-instances.
        :return: WeakSet
        """
        return WeakSet([x for x in tasks if self.isMatch(x)])

    def __str__(self):
        return '{filtername}(filterparameter)'.format(self.__class__.__name__, self.text)


class CompleteTasksFilter(BaseFilter):
    """
    Task list filter that removes any uncompleted tasks.

    """
    def __init__(self):
        super().__init__('Complete')

    def isMatch(self, task):
        return task.is_complete

    def matches(self, tasks=Task.all_tasks):
        return tasks & Task.completed_tasks


class IncompleteTasksFilter(BaseFilter):
    """
    Task list filter that removes any completed tasks.

    """
    def __init__(self):
        super().__init__('Incomplete')

    def isMatch(self, task):
        return not task.is_complete

    def matches(self, tasks=Task.all_tasks):
        return tasks - Task.completed_tasks


class IncompleteUncategorizedTasksFilter(BaseFilter):
    """
    Task list filter permitting incomplete tasks without project or context.

    """
    def __init__(self):
        super().__init__('Uncategorized')

    def isMatch(self, task):
        return (not task.is_complete) and (not task.contexts) and (not task.projects)

    def matches(self, tasks=Task.all_tasks):
        return WeakSet([x for x in tasks - Task.completed_tasks if not x.contexts and not x.projects])


class IncompleteTasksWithContextsFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected contexts.

    """

    def __init__(self, *contexts):
        self.contexts = set(contexts)
        super().__init__(contexts)

    def isMatch(self, task):
        return (not task.is_complete) and self.contexts <= set(task.contexts)

    def matches(self, tasks=Task.all_tasks):
        tasks = WeakSet(tasks)
        return WeakSet([x for x in (tasks - Task.completed_tasks) if self.contexts <= set(x.contexts)])


class IncompleteTasksWithProjectsFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with certain projects.

    """

    def __init__(self, *projects):
        self.projects = set(projects)
        super().__init__(projects)

    def isMatch(self, task):
        return (not task.is_complete) and self.projects <= set(task.projects)

    def matches(self, tasks=Task.all_tasks):
        tasks = WeakSet(tasks)
        return WeakSet([x for x in (tasks - Task.completed_tasks) if self.projects <= set(x.projects)])


class FutureFilter(BaseFilter):

    def __init__(self):
        super().__init__('Future')

    def isMatch(self, task):
        return task not in Task.future_tasks

    def matches(self, tasks=Task.all_tasks):
        return tasks & Task.future_tasks


class BaseDueFilter(BaseFilter):
    """
    Due list filter for ranges

    """
    def isMatch(self, task):
        return (not task.is_complete) and (self.text in task.dueRanges)


class DueTodayFilter(BaseDueFilter):
    """
    Task list filter allowing only incomplete tasks that are due today.

    """
    def isMatch(self, task):
        if (not task.due_date) or (task.is_complete):
            return False
        else:
            self.due_date = task.due_date.value
            today = datetime.today().date()
            return self.due_date == today


class DueTomorrowFilter(BaseDueFilter):
    """
    Task list filter allowing only incomplete tasks that are due tomorrow.

    """
    def isMatch(self, task):
        if (not task.due_date) or (task.is_complete):
            return False
        else:
            due_date = task.due_date.value
            today = datetime.today().date()
            return today < due_date <= today + timedelta(days=1)


class DueThisWeekFilter(BaseDueFilter):
    """
    Task list filter allowing only incomplete tasks that are due this week.

    """
    def isMatch(self, task):
        if (not task.due_date) or (task.is_complete):
            return False
        else:
            due_date = task.due_date.value
            today = datetime.today().date()
            return today <= due_date <= today + timedelta((6-today.weekday()) % 7)


class DueThisMonthFilter(BaseDueFilter):
    """
    Task list filter allowing only incomplete tasks that are due this month.

    """
    def isMatch(self, task):
        if (not task.due_date) or (task.is_complete):
            return False
        else:
            due_date = task.due_date.value
            today = datetime.today().date()
            if today.month == 12:
                last_day_of_month = today.replace(day=31)
            else:
                last_day_of_month = today.replace(month=today.month+1, day=1) - timedelta(days=1)
            return today <= due_date <= last_day_of_month


class DueOverdueFilter(BaseDueFilter):
    """
    Task list filter allowing only incomplete tasks that are overdue.

    """
    def isMatch(self, task):
        if (not task.due_date) or (task.is_complete):
            return False
        else:
            due_date = task.due_date.value
            today = datetime.today().date()
            return due_date < today


# TODO make use of IncompleteTasksWithContextsFilter!?
class HasProjectsFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected project.

    """

    def __init__(self):
        super().__init__('Projects')

    def isMatch(self, task):
        return (not task.is_complete) and task.projects


# TODO make use of IncompleteTasksWithProjextsFilter!?
class HasContextsFilter(BaseFilter):
    """
    Task list filter allowing only tasks tagged with some project.

    """

    def __init__(self):
        super().__init__('Contexts')

    def isMatch(self, task):
        return (not task.is_complete) and task.contexts


class HasDueDateFilter(BaseFilter):
    """
    Task list filter allowing only complete tasks with due date in due ranges.

    """

    def __init__(self):
        super().__init__('DueRange')

    def isMatch(self, task):
        return (not task.is_complete) and task.due


class HasDueRangesFilter(BaseFilter):
    """
    Task list filter allowing only complete tasks with due date in due ranges.

    """

    def __init__(self):
        super().__init__('DueRange')

    def isMatch(self, task):
        return (not task.is_complete) and task.dueRanges


class SimpleTextFilter(BaseFilter):
    """
    Task list filter allowing only tasks whose string matches a filter string.

    This filter allows for basic and/or/not conditions in the filter string.
    For the syntax see SimpleTextFilter.isMatch.

    """

    def __init__(self, text):
        super().__init__(text)

    def isMatch(self, task):
        """
        Return a boolean based on whether the supplied task satisfies self.text.
        TODO: the NOT syntax described below isn't yet implemented

        This filter can handle basic and/or/not conditions. The syntax is as
        follows:

        :AND   :   ',' or whitespace (' ')
        :OR    :   '|'
        :NOT   :   prefixed '~' or '!'  {not yet implemented}

        These operators follow the following order of precedence: OR, AND, NOT.
        So, for example:

        :'work job1 | home':                Either  (matches 'work'
                                                     AND 'job1')
                                            OR      (matches 'home')

        :'norwegian blue ~dead | !parrot':  Either  (matches 'norwegian'
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
        # TODO: implement NOT conditions
        comp = re.compile(r'\s*([\(\)\w\\\-]+)[\s,]*', re.U)
        restring = comp.sub(r'^(?=.*\1)', self.text, re.U)
        try:
            if ')' in restring:
                raise re.error  # otherwise adding closing parenthesis avoids error here
            mymatch = re.search(restring, str(task), re.I | re.U)
        except re.error:
            comp2 = re.compile(r'\s*\((?=[^?])', re.U)
            restring2 = comp2.sub(r'\\(', restring, re.U)
            comp3 = re.compile(r'(?<!\))\)(?=\))', re.U)
            restring3 = comp3.sub(r'\\)', restring2, re.U)
            mymatch = re.search(restring3, str(task), re.I | re.U)

        return mymatch

    def matches(self, tasks=Task.all_tasks):
        return WeakSet([x for x in tasks if self.isMatch(x)])

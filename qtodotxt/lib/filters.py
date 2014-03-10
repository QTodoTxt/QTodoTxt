import re


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
        return (not task.is_complete) and (not task.contexts) and (not task.projects)


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
        return (not task.is_complete) and (self.text in task.contexts)

    def __str__(self):
        return "ContextFilter(%s)" % self.text


class ProjectFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected project.

    """
    def __init__(self, project):
        BaseFilter.__init__(self, project)

    def isMatch(self, task):
        return (not task.is_complete) and (self.text in task.projects)

    def __str__(self):
        return "ProjectFilter(%s)" % self.text


class HasProjectsFilter(BaseFilter):
    """
    Task list filter allowing only incomplete tasks with the selected project.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'Projects')

    def isMatch(self, task):
        return (not task.is_complete) and task.projects

    def __str__(self):
        return "HasProjectsFilter" % self.text


class HasContextsFilter(BaseFilter):
    """
    Task list filter allowing only tasks tagged with some project.

    """

    def __init__(self):
        BaseFilter.__init__(self, 'Contexts')

    def isMatch(self, task):
        return (not task.is_complete) and task.contexts

    def __str__(self):
        return "HasContextsFilter" % self.text


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
        TODO: the NOT syntax described below isn't yet implemented

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

        """
        mymatch = False
        comp = re.compile(r'\s*([\w\\-]+)[\s,]*', re.I)
        restring = comp.sub(r'^(?=.*\1)',
                            self.text)
        mymatch = re.search(restring, task.text, re.I|re.U)
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

import re
from datetime import datetime, date

from PySide import QtCore

from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.lib import deprecated


HIGHEST_PRIORITY = 'A'


class Priority(object):

    def __init__(self, val="", lowest_priority="D"):
        self.priority = val
        self._lowest_priority = lowest_priority

    def __add__(self, inc):
        if inc <= 0:
            raise RuntimeError("Increment to priority must be positiv")
        newp = self.priority
        if not self.priority:
            newp = self._lowest_priority
            inc -= 1
        if newp != HIGHEST_PRIORITY:
            o = ord(newp) - inc
            if o < ord(HIGHEST_PRIORITY):
                o = ord(HIGHEST_PRIORITY)
            newp = chr(o)
        return Priority(newp)

    def __sub__(self, inc):
        if inc <= 0:
            raise RuntimeError("Increment to priority must be positiv")
        newp = self.priority
        if newp:
            o = ord(newp) + inc
            if o > ord(self._lowest_priority):
                return Priority("")
            newp = chr(o)
        return Priority(newp)

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        if not other.priority:
            return False
        if other.priority and not self.priority:
            return True
        return self.priority > other.priority

    def __str__(self):
        return self.priority

    def __repr__(self):
        return "Priority({})".format(self.priority)

    def __hash__(self):
        return hash(self.priority)

    def __bool__(self):
        if self.priority:
            return True
        return False


class Task(object):
    """
    Represent a task as defined in todo.txt format
    Take a line in todo.txt format as argument
    priority and complete argument are editable
    other arguments are read-only (this might change), reparse string to modify them
    """

    def __init__(self, line):
        settings = QtCore.QSettings()
        self._lowest_priority = settings.value("user_lowest_priority", "D").upper()
        # force update so option appear in config file
        # FIXME: move it somewhere else where it is only called once for app!!
        settings.setValue("user_lowest_priority", self._lowest_priority)

        self.parseString(line)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Task({})".format(self.text)

    def _reset(self):
        self.contexts = []
        self.projects = []
        self.priority = Priority()
        self.is_complete = False
        self.is_future = False
        self._text = ''
        self.due = None
        self.threshold = None

    def parseString(self, line):
        """
        parse a task formated as string in todo.txt format
        """
        self._reset()
        words = line.split(' ')
        if words[0] == "x":
            self.is_complete = True
            words = words[1:]
        if re.search('^\([A-Z]\)$', words[0]):
            self.priority = Priority(words[0][1:-1], self._lowest_priority)
            words = words[1:]
        text = []
        for word in words:
            w = self._parseWord(word)
            if w:
                text.append(w)
        self._text = ' '.join(text)

    def _parseWord(self, word):
        if len(word) > 1:
            if word.startswith('@'):
                self.contexts.append(word[1:])
            elif word.startswith('+'):
                self.projects.append(word[1:])
            elif word.startswith('due:'):
                self.due = word[4:]
            elif word.startswith('t:'):
                self.threshold = word[2:]
                try:
                    self.is_future = datetime.strptime(self.threshold, '%Y-%m-%d').date() > date.today()
                except ValueError:
                    self.is_future = False
        return word  # Currently we return all, but we should take out keyword

    @staticmethod
    def fromString(self, string):
        """
        Create a new task from a string in todo.txt format
        """
        return Task(string)

    def toString(self):
        """
        return a task as a string following todo.txt format
        """
        priority = ""
        if self.priority:
            priority = "({}) ".format(self.priority)
        complete = ""
        if self.is_complete:
            complete = "x "
        return "{}{}{}".format(complete, priority, self._text)

    def toHtml(self):
        """
        return a task as an html block which is a pretty display of a line in todo.txt format
        """
        htmlizer = TaskHtmlizer()
        return htmlizer.task2html(self)

    def _getText(self):
        return self.toString()

    def _setText(self, line):
        if line:
            self.parseLine(line)

    text = property(_getText, _setText)

    def increasePriority(self):
        self.priority += 1

    def decreasePriority(self):
        self.priority -= 1

    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        if self.is_complete != other.is_complete:
            return self._lowerCompleteness(other)
        if self.priority != other.priority:
            return self.priority < other.priority
        # order the other tasks alphabetically
        return self._text > other._text

    def _lowerCompleteness(self, other):
        if self.is_complete and not other.is_complete:
            return True
        if not self.is_complete and other.is_complete:
            return False
        raise RuntimeError("Could not compare completeness of 2 tasks, please report")


def filterTasks(filters, tasks):
    if None in filters:
        return tasks

    filteredTasks = []
    for task in tasks:
        for filter in filters:
            if filter.isMatch(task):
                filteredTasks.append(task)
                break
    return filteredTasks

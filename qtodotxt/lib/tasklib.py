from datetime import datetime, date, time
import re

from PyQt5 import QtCore
from enum import Enum
from qtodotxt.lib.task_htmlizer import TaskHtmlizer


class recursiveMode(Enum):
    completitionDate = 0  # Original due date mode: Task recurs from original due date
    originalDueDate = 1  # Completion date mode: Task recurs from completion date


class recursion:
    mode = None
    increment = None
    interval = None

    def __init__(self, arg_mode, arg_increment, arg_interval):
        self.mode = arg_mode
        self.increment = arg_increment
        self.interval = arg_interval


class Task(QtCore.QObject):
    """
    Represent a task as defined in todo.txt format
    Take a line in todo.txt format as argument
    Arguments are read-only, reparse string to modify them or
    use one the modification methods such as setCompleted()
    """

    modified = QtCore.pyqtSignal(object)

    def __init__(self, line):
        QtCore.QObject.__init__(self)
        settings = QtCore.QSettings()
        self._highest_priority = 'A'
        self._lowest_priority = settings.value("lowest_priority", "D")

        # all other class attributes are defined in _reset method
        # which is called in _parse
        self._parse(line)

    def __str__(self):
        return self._text

    def __repr__(self):
        return "Task({})".format(self._text)

    def _reset(self):
        self.contexts = []
        self.projects = []
        self.priority = ""
        self.is_complete = False
        self.completion_date = None
        self.creation_date = None
        self.is_future = False
        self.threshold_error = ""
        self._text = ''
        self.description = ''
        self.due = None
        self.due_error = ""
        self.threshold = None
        self.keywords = {}
        self.recursion = None

    def _parse(self, line):
        """
        parse a task formated as string in todo.txt format
        """
        self._reset()
        words = line.split(' ')
        if words[0] == "x":
            self.is_complete = True
            words = words[1:]
            # parse next word as a completion date
            # required by todotxt but often not here
            self.completion_date = self._parseDate(words[0])
            if self.completion_date:
                words = words[1:]
        elif re.search(r'^\([A-Z]\)$', words[0]):
            self.priority = words[0][1:-1]
            words = words[1:]

        dato = self._parseDate(words[0])
        if dato:
            self.creation_date = dato
            words = words[1:]

        self.description = " ".join(words)
        for word in words:
            self._parseWord(word)
        self._text = line

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, txt):
        self._parse(txt)
        self.modified.emit(self)

    def _parseWord(self, word):
        if len(word) > 1:
            if word.startswith('@'):
                self.contexts.append(word[1:])
            elif word.startswith('+'):
                self.projects.append(word[1:])
            elif ":" in word:
                key, val = word.split(":", 1)
                self.keywords[key] = val
                if word.startswith('due:'):
                    self.due = self._parseDateTime(word[4:])
                    if not self.due:
                        print("Error parsing due date '{}'".format(word))
                        self.due_error = word[4:]
                elif word.startswith('t:'):
                    self.threshold = self._parseDateTime(word[2:])
                    if not self.threshold:
                        print("Error parsing threshold '{}'".format(word))
                        self.threshold_error = word[2:]
                    else:
                        if self.threshold > datetime.today():
                            self.is_future = True
                elif word.startswith('rec:'):
                    self._parseRecurrence(word)

    def _parseRecurrence(self, word):
        # Original due date mode
        if word[4] == '+':
            # Test if chracters have the right format
            if re.match('^[1-9][bdwmy]', word[5:7]):
                self.recursion = recursion(recursiveMode.originalDueDate, word[5], word[6])
            else:
                print("Error parsing recurrence '{}'".format(word))
        # Completion mode
        else:
            # Test if chracters have the right format
            if re.match('^[1-9][bdwmy]', word[4:6]):
                self.recursion = recursion(recursiveMode.completitionDate, word[4], word[5])
            else:
                print("Error parsing recurrence '{}'".format(word))

    def _parseDate(self, string):
        try:
            return datetime.strptime(string, '%Y-%m-%d').date()
        except ValueError:
            return None

    def _parseDateTime(self, string):
        try:
            return datetime.strptime(string, '%Y-%m-%d')
        except ValueError:
            try:
                return datetime.strptime(string, '%Y-%m-%dT%H:%M')
            except ValueError:
                return None

    @property
    def dueString(self):
        return dateString(self.due)

    @staticmethod
    def updateDateInTask(text, newDate):
        # FIXME: This method has nothing to do in this class, move womewhere else
        # (A) 2016-12-08 Feed Schrodinger's Cat rec:9w due:2016-11-23
        text = re.sub('\sdue\:[0-9]{4}\-[0-9]{2}\-[0-9]{2}', ' due:' + str(newDate)[0:10], text)
        return text

    @property
    def thresholdString(self):
        return dateString(self.threshold)

    def setCompleted(self):
        """
        Set a task as completed by inserting a x and current date at the begynning of line
        """
        if self.is_complete:
            return
        self.completion_date = date.today()
        date_string = self.completion_date.strftime('%Y-%m-%d')
        self._text = 'x %s %s' % (date_string, self._text)
        self.is_complete = True
        self.modified.emit(self)

    def setPending(self):
        """
        Unset completed flag from task
        """
        if not self.is_complete:
            return
        words = self._text.split(" ")
        d = self._parseDate(words[1])
        if d:
            self._text = " ".join(words[2:])
        else:
            self._text = " ".join(words[1:])
        self.is_complete = False
        self.completion_date = None
        self.modified.emit(self)

    def toHtml(self):
        """
        return a task as an html block which is a pretty display of a line in todo.txt format
        """
        htmlizer = TaskHtmlizer()
        return htmlizer.task2html(self)

    def increasePriority(self):
        if self.is_complete:
            return
        if not self.priority:
            self.priority = self._lowest_priority
            self._text = "({}) {}".format(self.priority, self._text)
        elif self.priority != self._highest_priority:
            self.priority = chr(ord(self.priority) - 1)
            self._text = "({}) {}".format(self.priority, self._text[4:])
        self.modified.emit(self)

    def decreasePriority(self):
        if self.is_complete:
            return
        if self.priority >= self._lowest_priority:
            self.priority = ""
            self._text = self._text[4:]
            self._text = self._text.replace("({})".format(self.priority), "", 1)
        elif self.priority:
            oldpriority = self.priority
            self.priority = chr(ord(self.priority) + 1)
            self._text = self._text.replace("({})".format(oldpriority), "({})".format(self.priority), 1)
        self.modified.emit(self)

    def __eq__(self, other):
        return self._text == other.text

    def __lt__(self, other):
        if self.is_complete != other.is_complete:
            return self._lowerCompleteness(other)
        if self.priority != other.priority:
            if not self.priority:
                return True
            if not other.priority:
                return False
            return self.priority > other.priority
        # order the other tasks alphabetically
        return self._text > other.text

    def _lowerCompleteness(self, other):
        if self.is_complete and not other.is_complete:
            return True
        if not self.is_complete and other.is_complete:
            return False
        raise RuntimeError("Could not compare completeness of 2 tasks, please report")


def dateString(date):
    """
    Return a datetime as a nicely formatted string
    """
    if date.time() == time.min:
        return date.strftime('%Y-%m-%d')
    else:
        return date.strftime('%Y-%m-%d %H:%M')


def filterTasks(filters, tasks):
    if None in filters:  # FIXME: why??? if a filter is None we can just ignore it
        return tasks

    filteredTasks = []
    for task in tasks:
        for myfilter in filters:
            if myfilter.isMatch(task):
                filteredTasks.append(task)
                break
    return filteredTasks

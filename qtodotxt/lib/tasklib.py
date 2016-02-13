import re
from datetime import datetime, date

from PySide import QtCore

from qtodotxt.lib.task_htmlizer import TaskHtmlizer


class Task(object):
    """
    Represent a task as defined in todo.txt format
    Take a line in todo.txt format as argument
    Arguments are read-only, reparse string to modify them or
    use one the modification methods such as setCompleted()
    """

    def __init__(self, line):
        settings = QtCore.QSettings()
        self._highest_priority = 'A'
        self._lowest_priority = settings.value("lowest_priority", "D")

        # define all class attributes here to avoid pylint warnings
        self.contexts = []
        self.projects = []
        self.priority = ""
        self.is_complete = False
        self.completion_date = ""
        self.is_future = False
        self.text = ''
        self.due = None
        self.threshold = None
        self.keywords = {}

        self.parseString(line)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Task({})".format(self.text)

    def _reset(self):
        self.contexts = []
        self.projects = []
        self.priority = ""
        self.is_complete = False
        self.completion_date = ""
        self.is_future = False
        self.text = ''
        self.due = None
        self.threshold = None
        self.keywords = {}

    def parseString(self, line):
        """
        parse a task formated as string in todo.txt format
        """
        self._reset()
        words = line.split(' ')
        if words[0] == "x":
            self.is_complete = True
            words = words[1:]
            # FIXME: parse next word as a completion date if format matches.
            # It is required by format
            # self.complete_date
        elif re.search(r'^\([A-Z]\)$', words[0]):
            self.priority = words[0][1:-1]
            words = words[1:]
        for word in words:
            self._parseWord(word)
        self.text = line

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
                    self.due = word[4:]
                elif word.startswith('t:'):
                    self.threshold = word[2:]
                    try:
                        self.is_future = datetime.strptime(self.threshold, '%Y-%m-%d').date() > date.today()
                    except ValueError:
                        self.is_future = False

    def setCompleted(self):
        """
        """
        if self.is_complete:
            return
        self.completion_date = date.today()
        date_string = self.completion_date.strftime('%Y-%m-%d')
        self.text = 'x %s %s' % (date_string, self.text)
        self.is_complete = True

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
            self.text = "({}) {}".format(self.priority, self.text)
        elif self.priority != self._highest_priority:
            self.priority = chr(ord(self.priority) - 1)
            self.text = "({}) {}".format(self.priority, self.text[4:])

    def decreasePriority(self):
        if self.is_complete:
            return
        if self.priority >= self._lowest_priority:
            self.priority = ""
            self.text = self.text[4:]
        elif self.priority:
            self.priority = chr(ord(self.priority) + 1)
            self.text = "({}) {}".format(self.priority, self.text[4:])

    def __eq__(self, other):
        return self.text == other.text

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
        return self.text > other.text

    def _lowerCompleteness(self, other):
        if self.is_complete and not other.is_complete:
            return True
        if not self.is_complete and other.is_complete:
            return False
        raise RuntimeError("Could not compare completeness of 2 tasks, please report")


def filterTasks(filters, tasks):
    if None in filters:  # FIXME: why??? if a filter is None we can just ignore it
        return tasks

    filteredTasks = []
    for task in tasks:
        for filter in filters:
            if filter.isMatch(task):
                filteredTasks.append(task)
                break
    return filteredTasks

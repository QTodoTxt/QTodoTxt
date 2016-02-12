import re
from datetime import datetime, date

from PySide import QtCore


HIGHEST_PRIORITY = 'A'
LOWEST_PRIORITY = 'Z'


class Task(object):

    def __init__(self, line):
        self.reset()

        # read and validate user_lowest_priority
        # TODO: make user_lowest_priority changeable from gui
        default_lowest_priority = "D"
        settings = QtCore.QSettings()
        user_lowest_priority = settings.value("user_lowest_priority", default_lowest_priority)
        if str(user_lowest_priority).isupper():
            self._user_lowest_priority = user_lowest_priority
        else:
            self._user_lowest_priority = default_lowest_priority
            # make sure other parts of the application using this value
            # always get a valid value
            settings.setValue("user_lowest_priority", self._user_lowest_priority)

        if line:
            self.parseLine(line)

    def __str__(self):
        return "Task({})".format(self.text)
    __repr__ = __str__

    def reset(self):
        self.contexts = []
        self.projects = []
        self.priority = None
        self.is_complete = False
        self.is_future = False
        self._text = ''
        self.due = None
        self.threshold = None

    def parseLine(self, line):
        words = line.split(' ')
        i = 0
        while i < len(words):
            self.parseWord(words[i], i)
            i += 1

        self._text = ' '.join(words)

    def parseWord(self, word, index):
        if index == 0:
            if word == 'x':
                self.is_complete = True
            elif re.search('^\([A-Z]\)$', word):
                self.priority = word[1]
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

    def _getText(self):
        return self._text

    def _setText(self, line):
        self.reset()
        if line:
            self.parseLine(line)

    text = property(_getText, _setText)

    def increasePriority(self):
        if self.priority != HIGHEST_PRIORITY:
            if (self.priority is None):
                self.priority = self._user_lowest_priority
                self.text = '(%s) %s' % (self.priority, self.text)
            else:
                oldPriority = self.priority
                self.priority = chr(ord(self.priority) - 1)
                self.text = re.sub('^\(%s\) ' % oldPriority, '(%s) ' % self.priority, self.text)

    def decreasePriority(self):
        if self.priority is not None:
            if (self.priority == self._user_lowest_priority) or (self.priority == LOWEST_PRIORITY):
                self.priority = None
                self.text = self.text[4:]
            else:
                oldPriority = self.priority
                self.priority = chr(ord(self.priority) + 1)
                self.text = re.sub('^\(%s\) ' % oldPriority, '(%s) ' % self.priority, self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        if self.is_complete != other.is_complete:
            return self._lowerCompleteness(other)
        if self.priority != other.priority:
            return self._lowerPriority(other)
        # order the other tasks alphabetically
        return self.text > other.text

    def _lowerPriority(self, other):
        if not other.priority:
            return False
        if other.priority and not self.priority:
            return True
        return self.priority > other.priority

    def _lowerCompleteness(self, other):
        if self.is_complete and not other.is_complete:
            return True
        if not self.is_complete and other.is_complete:
            return False
        raise RuntimeError("Could not comapre completeness, report")


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

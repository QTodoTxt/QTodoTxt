import re
from datetime import datetime, date

from PySide import QtCore


HIGHEST_PRIORITY = 'A'


class Priority(object):
    def __init__(self, val="", lowest_priority="D"):
        self.priority = val
        self._lowest_priority = lowest_priority

    def __add__(self, inc):
        newp = self.priority
        if newp != HIGHEST_PRIORITY:
            if not newp:
                newp = self._lowest_priority
            else:
                newp = chr(ord(newp) - inc)
        return Priority(newp)

    def __sub__(self, inc):
        newp = self.priority
        if newp:
            if newp == self._lowest_priority:
                newp = ""
            else:
                newp = chr(ord(newp) + inc)
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

    def __init__(self, line):
        settings = QtCore.QSettings()
        self._lowest_priority = settings.value("user_lowest_priority", "D")
        settings.setValue("user_lowest_priority", self._lowest_priority)  #force update, FIXME: why????

        self.parseLine(line)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Task({})".format(self.text)

    def reset(self):
        self.contexts = []
        self.projects = []
        self.priority = Priority()
        self.is_complete = False
        self.is_future = False
        self._text = ''
        self.due = None
        self.threshold = None

    def parseLine(self, line):
        self.reset()
        words = line.split(' ')
        if words[0] == "x":
            self.is_complete = True
            words = words[1:]
        if re.search('^\([A-Z]\)$', words[0]):
            self.priority = Priority(words[0][1:-1], self._lowest_priority)
            words = words[1:]
        text = []
        for word in words:
            w = self.parseWord(word)
            if w:
                text.append(w)
        self._text = ' '.join(text)

    def parseWord(self, word):
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

    def _getText(self):
        priority = ""
        if self.priority:
            priority = "({}) ".format(self.priority)
        complete = ""
        if self.is_complete:
            complete = "x "
        return "{}{}{}".format(complete, priority, self._text)

    def _setText(self, line):
        self.reset()
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
        return self.text > other.text

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

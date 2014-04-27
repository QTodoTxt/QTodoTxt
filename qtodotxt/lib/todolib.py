import re
import os
import codecs
from datetime import datetime,date
from functools import cmp_to_key

USE_LAST_FILENAME = 1
HIGHER_PRIORITY = 'A'
LOWER_PRIORITY = 'C'

class Error(Exception):
    pass

class ErrorLoadingFile(Error):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ErrorSavingFile(Error):

    def __init__(self, message, innerException=None):
        self.message = message
        self.innerException = innerException

    def __str__(self):
        lines = [repr(self.message)]
        if self.innerException:
            lines.append(repr(self.innerException))
        return '\n'.join(lines)

class File(object):
    def __init__(self):
        self.NEWLINE = '\n'
        self.tasks = []
        self.filename = None

    def load(self, filename):
        if filename.strip() == '':
            raise Error("Trying to load a file with an empty filename.")
        self.filename = filename
        lines = self._loadLinesFromFile(filename)
        self._createTasksFromLines(lines)

    def _createTasksFromLines(self, lines):
        self.tasks = []
        for line in lines:
            task_text = line.strip()
            if task_text:
                task = Task(task_text)
                self.tasks.append(task)

    def _loadLinesFromFile(self, filename):
        lines = []
        fd = None
        try:
            fd = codecs.open(filename, 'r', 'utf-8')
            lines = fd.readlines()
            fd.close()
        except IOError as e:
            raise ErrorLoadingFile(str(e))
        finally:
            if fd:
                fd.close()
        return lines

    def save(self, filename=USE_LAST_FILENAME):
        if filename == USE_LAST_FILENAME:
            filename = self.filename
        if not filename:
            raise ErrorSavingFile("Filename is None")
        self.filename = filename
        self.tasks.sort(key=cmp_to_key(compareTasks))
        self._saveTasks()

    def _saveTasks(self):
        fd = None
        try:
            fd = open(self.filename, 'w')
            lines = [(task.text + self.NEWLINE) for task in self.tasks]
            fd.writelines(lines)
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '%s'" % self.filename, e)
        finally:
            if fd:
                fd.close()

    def saveDoneTask(self, task):
        fdDone = None
        doneFilename = os.path.join(os.path.dirname(self.filename), 'done.txt')
        try:
            fdDone = open(doneFilename, 'a')
            fdDone.write(task.text + self.NEWLINE)
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '%s'" % doneFilename, e)
        finally:
            if fdDone:
                fdDone.close()

    def getAllCompletedContexts(self):
        contexts = dict()
        for task in self.tasks:
            if task.is_complete:
                for context in task.contexts:
                    if context in contexts:
                        contexts[context] += 1
                    else:
                        contexts[context] = 1
        return contexts

    def getAllCompletedProjects(self):
        projects = dict()
        for task in self.tasks:
            if task.is_complete:
                for project in task.projects:
                    if project in projects:
                        projects[project] += 1
                    else:
                        projects[project] = 1
        return projects

    def getAllContexts(self):
        contexts = dict()
        for task in self.tasks:
            if not task.is_complete:
                for context in task.contexts:
                    if context in contexts:
                        contexts[context] += 1
                    else:
                        contexts[context] = 1
        return contexts

    def getAllProjects(self):
        projects = dict()
        for task in self.tasks:
            if not task.is_complete:
                for project in task.projects:
                    if project in projects:
                        projects[project] += 1
                    else:
                        projects[project] = 1
        return projects

    def getTasksCounters(self):
        counters = dict({'Pending': 0,
                         'Uncategorized': 0,
                         'Contexts': 0,
                         'Projects': 0,
                         'Complete': 0})
        for task in self.tasks:
            if not task.is_complete:
                counters['Pending'] += 1
                nbProjects = len(task.projects)
                nbContexts = len(task.contexts)
                if nbProjects > 0:
                    counters['Projects'] += 1
                if nbContexts > 0:
                    counters['Contexts'] += 1
                if nbContexts == 0 and nbProjects == 0:
                    counters['Uncategorized'] += 1
            else:
                counters['Complete'] += 1
        return counters    


class Task(object):

    def __init__(self, line):
        self.reset()
        if line:
            self.parseLine(line)

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

    def increasePriority(self):
        if self.priority is None:
            self.priority = LOWER_PRIORITY
            self.text = '(%s) %s' % (LOWER_PRIORITY, self.text)
        elif self.priority == HIGHER_PRIORITY:
            self.priority = None
            self.text = self.text[4:]
        else:
            newPriority = chr(ord(self.priority)-1)
            self.text = re.sub('^\(%s\) ' % self.priority, '(%s) ' % newPriority, self.text)
            self.priority = newPriority

    def decreasePriority(self):
        if self.priority is None:
            self.priority = HIGHER_PRIORITY
            self.text = '(%s) %s' % (HIGHER_PRIORITY, self.text)
        elif self.priority == LOWER_PRIORITY:
            self.text = self.text[4:]
            self.priority = None
        else:
            newPriority = chr(ord(self.priority)+1)
            self.text = re.sub('^\(%s\) ' % self.priority, '(%s) ' % newPriority, self.text)
            self.priority = newPriority
    text = property(_getText, _setText)



def compareTasks(task1, task2):
    comparison = compareTasksByCompleteness(task1, task2)
    if comparison:
        return comparison
    comparison = compareTasksByPriority(task1, task2)
    if comparison:
        return comparison
    if task1.text < task2.text:
        return -1
    elif task1.text > task2.text:
        return 1
    else:
        return 0

def compareTasksByPriority(task1, task2):
    if (not task1.priority and not task2.priority) \
        or \
        (task1.priority == task2.priority):
            return 0
    if not task1.priority:
        return 1
    if not task2.priority:
        return -1
    if task1.priority > task2.priority:
        return 1
    if task2.priority < task2.priority:
        return -1

def compareTasksByCompleteness(task1, task2):
    if task1.is_complete == task2.is_complete:
        return 0
    if task1.is_complete:
        return 1
    if task2.is_complete:
        return -1
    else:
        return 1
    
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

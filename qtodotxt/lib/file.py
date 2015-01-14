from functools import cmp_to_key
import logging
import os
from PySide import QtCore
from qtodotxt.lib.filters import DueTodayFilter, DueTomorrowFilter, DueThisWeekFilter, DueThisMonthFilter, DueOverdueFilter
from qtodotxt.lib.todolib import Task, compareTasks
from sys import version
import time

logger = logging.getLogger(__name__)

PYTHON_VERSION = version[:3]

if PYTHON_VERSION < '3.3':
    FileNotFoundError = OSError


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
        self.filename = ''

    def load(self, filename):

        try:
            with open(filename, 'rt', encoding='utf-8') as fd:
                lines = fd.readlines()
        except FileNotFoundError:
            raise ErrorLoadingFile("Trying to load a non-existing file: '{}".format(filename))
        except IOError as ex:                # deprecated since Python 3.3, it would be OSError for =>3.3-support
            raise ErrorLoadingFile(str(ex))
        self.filename = filename
        self._createTasksFromLines(lines)

    def _createTasksFromLines(self, lines):
        self.tasks = []
        for line in lines:
            task_text = line.strip()
            if task_text:
                task = Task(task_text)
                self.tasks.append(task)

    def save(self, filename=''):
        logger.debug('File.save called with filename="{}"'.format(filename))
        if not filename and not self.filename:
            self.filename = self._createNewFilename()
        elif filename:
            self.filename = filename
        self.tasks.sort(key=cmp_to_key(compareTasks))
        self._saveTasks()

    @staticmethod
    def _createNewFilename():
        newFileName = os.path.expanduser('~/todo.txt')
        if not os.path.isfile(newFileName):
            return newFileName
        for counter in range(0, 100):
            newFileName = os.path.expanduser('~/todo.{}.txt.'.format(counter))
            if not os.path.isfile(newFileName):
                return newFileName
        return os.path.expanduser('~/todo.0.txt')

    def _saveTasks(self):
        try:
            with open(self.filename, 'wt', encoding='utf-8') as fd:
                fd.writelines([(task.text + self.NEWLINE) for task in self.tasks])
            logger.debug('{} was saved to disk.'.format(self.filename))
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '{}'".format(self.filename), e)

    def saveDoneTask(self, task):
        doneFilename = os.path.join(os.path.dirname(self.filename), 'done.txt')
        try:
            with open(doneFilename, 'at', encoding='utf-8') as fd:
                fd.write(task.text + self.NEWLINE)
            logger.debug('"{}" was appended to "{}"'.format(task.text, doneFilename))
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '%s'" % doneFilename, e)

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

    def getAllDueRanges(self):
        dueRanges = dict()
        for task in self.tasks:
            if DueTodayFilter('Today').isMatch(task):
                if not ('Today' in dueRanges):
                    dueRanges['Today'] = 1
                else:
                    dueRanges['Today'] += 1

            if DueTomorrowFilter('Tomorrow').isMatch(task):
                if not ('Tomorrow' in dueRanges):
                    dueRanges['Tomorrow'] = 1
                else:
                    dueRanges['Tomorrow'] += 1

            if DueThisWeekFilter('This week').isMatch(task):
                if not ('This week' in dueRanges):
                    dueRanges['This week'] = 1
                else:
                    dueRanges['This week'] += 1

            if DueThisMonthFilter('This month').isMatch(task):
                if not ('This month' in dueRanges):
                    dueRanges['This month'] = 1
                else:
                    dueRanges['This month'] += 1

            if DueOverdueFilter('Overdue').isMatch(task):
                if not ('Overdue' in dueRanges):
                    dueRanges['Overdue'] = 1
                else:
                    dueRanges['Overdue'] += 1

        return dueRanges

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
                         'Complete': 0,
                         'Due' : 0})
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
                if task.due:
                    counters['Due'] += 1
            else:
                counters['Complete'] += 1
        return counters


class FileObserver(QtCore.QFileSystemWatcher):
   def __init__(self, parent, file):
       logger.debug('Setting up FileObserver instance.')
       super().__init__(parent)
       self._file = file
       self.fileChanged.connect(self.fileChangedHandler)

   @QtCore.Slot(str)
   def fileChangedHandler(self, path):
       logger.debug('Detected change on {}\nremoving it from watchlist'.format(path))
       self.removePath(path)
       debug_counter = 0
       if path == self._file.filename:
           max_time = time.time() + 1
           while time.time() < max_time:
               try:
                   self.parent().openFileByName(self._file.filename)  # TODO make that emit a signal
               except ErrorLoadingFile:
                   time.sleep(0.01)
                   debug_counter += 1
               else:
                   logger.debug('It took {} additional attempts until the file could be read.'.format(debug_counter))
                   break

   def clear(self):
       if self.files():
           logger.debug('Clearing watchlist.')
           self.removePaths(self.files())

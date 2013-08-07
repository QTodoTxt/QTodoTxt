import re
import os
import codecs
from argparse import ArgumentError

USE_LAST_FILENAME = 1

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
        self.newline = '\n'
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
            fd = codecs.open(filename,'r','utf-8')
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
        self.tasks.sort(compareTasks)
        self._saveTasks()
        
    def _saveTasks(self):
        fd = None
        try:
            fd = open(self.filename, 'w')
            lines = [(task.text.encode('utf8') + self.newline) for task in self.tasks]
            fd.writelines(lines)
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '%s'" % self.filename, e)
        finally:
            if fd:
                fd.close()
                
    def saveDoneTask(self,task):
        fdDone = None
        doneFilename = os.path.join(os.path.dirname(self.filename),'done.txt')
        try:
            fdDone = open(doneFilename,'a')
            fdDone.write(task.text.encode('utf8') + self.newline)
        except IOError as e:
            raise ErrorSavingFile("Error saving to file '%s'" % doneFilename, e)
        finally:
            if fdDone:
                fdDone.close()
        
        
    def getAllContexts(self):
        contexts = []
        for task in self.tasks:
            if not task.is_complete:
                for context in task.contexts:
                    if context not in contexts:
                        contexts.append(context)
        return contexts

    def getAllProjects(self):
        projects = []
        for task in self.tasks:
            if not task.is_complete:
                for project in task.projects:
                    if project not in projects:
                        projects.append(project)
        return projects

    
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
        self._text = ''
        self.due = None
    
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

    def _getText(self):
        return self._text
    
    def _setText(self, line):
        self.reset()
        if line:
            self.parseLine(line)
    
    text = property(_getText, _setText)

def compareTasks(task1, task2):
    comparison = compareTasksByCompleteness(task1, task2)
    if comparison != 0:
        return comparison
    comparison = compareTasksByPriority(task1, task2)
    if comparison != 0:
        return comparison
    return cmp(task1.text, task2.text)
    
def compareTasksByPriority(task1, task2):
    if task1.priority is None:
        if task2.priority is None:
            return 0
        else:
            return 1
    else:
        if task2.priority is None:
            return -1
        else:
            return cmp(task1.priority, task2.priority)

def compareTasksByCompleteness(task1, task2):
    if task1.is_complete == task2.is_complete:
        return 0
    elif task2.is_complete:
        return -1
    else:
        return 1
        

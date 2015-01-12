import re
from datetime import datetime,date,timedelta


HIGHER_PRIORITY = 'A'
LOWER_PRIORITY = 'Z'


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
        self.dueRanges = []
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
                try:
                    today = datetime.today().date()
                    due_date = datetime.strptime(self.due, '%Y-%m-%d').date()

                    # Tasks due today
                    if  due_date == date.today():
                        self.dueRanges.append('today')

                    # Tasks due tomorrow
                    if today < due_date <= today + timedelta(days=1):
                        self.dueRanges.append('tomorrow')

                    # Tasks due this week (assuming monday as start of week)
                    if today <= due_date <= today + timedelta((6-today.weekday()) % 7):
                        self.dueRanges.append('this week')

                    # Tasks due this month
                    if today.month == 12:
                        last_day_of_month = today.replace(day=31)
                    else:
                        last_day_of_month = today.replace(month=today.month+1, day=1) - timedelta(days=1)
                    if today <= due_date <= last_day_of_month:
                        self.dueRanges.append('this month')

                    # Overdue tasks
                    if due_date < today:
                        self.dueRanges.append('overdue')

                except ValueError:
                    self.dueRanges.append('ValueError')

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

from datetime import date, timedelta
import collections
import calendar
from collections import OrderedDict
import string

from dateutil.relativedelta import relativedelta

from PyQt5 import QtCore, QtGui, QtWidgets


def end_of_month(today=None, month=None):
    if today is None:
        today = date.today()
    if month is None:
        month = today.month
    year = today.year
    if month < today.month:
        year += 1
    eom = date(year=year, month=month, day=calendar.monthrange(year, month)[1])
    return eom.isoformat()


def end_of_next_month(today=None):
    if today is None:
        today = date.today()
    today += relativedelta(months=1)
    eom = date(year=today.year, month=today.month, day=calendar.monthrange(today.year, today.month)[1])
    return eom.isoformat()


def end_of_week(day=None):
    if day is None:
        day = date.today()
    return (day + timedelta((6 - day.weekday()) % 7)).isoformat()


def end_of_next_week(day=None):
    if day is None:
        day = date.today()
    return (day + timedelta((13 - day.weekday()) % 14)).isoformat()


def end_of_work_week(day=None):
    if day is None:
        day = date.today()
    if day.weekday() > 4:
        return end_of_next_work_week()
    return (day + timedelta((4 - day.weekday()) % 7)).isoformat()


def end_of_next_work_week(day=None):
    if day is None:
        day = date.today()
    return (day + timedelta((11 - day.weekday()) % 14)).isoformat()


def end_of_year(day=None):
    if day is None:
        day = date.today()
    return (date(year=day.year + 1, month=1, day=1) - timedelta(days=1)).isoformat()




class CompleterSetup(object):
    autocomplete_pairs = collections.OrderedDict([
        ('due:Today', ''),
        ('due:Tomorrow', ''),
        ('due:EndOfWorkWeek', ''),
        ('due:EndOfNextWorkWeek', ''),
        ('due:EndOfWeek', ''),
        ('due:EndOfNextWeek', ''),
        ('due:EndOfMonth', ''),
        ('due:EndOfNextMonth', ''),
        ('due:EndOfYear', ''),
        ('due:January', ''),
        ('due:February', ''),
        ('due:March', ''),
        ('due:April', ''),
        ('due:May', ''),
        ('due:June', ''),
        ('due:July', ''),
        ('due:August', ''),
        ('due:September', ''),
        ('due:October', ''),
        ('due:November', ''),
        ('t:Today', ''),
        ('t:Tomorrow', ''),
        ('t:EndOfWeek', ''),
        ('t:EndOfNextWeek', ''),
        ('t:EndOfMonth', ''),
        ('t:EndOfNextMonth', ''),
        ('t:EndOfYear', ''),
        ('due:December', '')
    ])

    def __init__(self, editor):

        self._populateKeys(self.autocomplete_pairs)

    def _populateKeys(self, keys):
        self._populateDues(keys)
        self._populateThresholds(keys)

    def _populateThresholds(self, keys):
        keys['t:Today'] = 't:' + date.today().isoformat()
        keys['t:Tomorrow'] = 't:' + (date.today() + timedelta(days=1)).isoformat()
        keys['t:EndOfWorkWeek'] = 't:' + end_of_work_week()
        keys['t:EndOfNextWorkWeek'] = 't:' + end_of_next_work_week()
        keys['t:EndOfWeek'] = 't:' + end_of_week()
        keys['t:EndOfNextWeek'] = 't:' + end_of_next_week()
        keys['t:EndOfMonth'] = 't:' + end_of_month()
        keys['t:EndOfNextMonth'] = 't:' + end_of_next_month()
        keys['t:EndOfYear'] = 't:' + end_of_year()

    def _populateDues(self, keys):
        keys['due:Today'] = 'due:' + date.today().isoformat()
        keys['due:Tomorrow'] = 'due:' + (date.today() + timedelta(days=1)).isoformat()
        keys['due:EndOfWorkWeek'] = 'due:' + end_of_work_week()
        keys['due:EndOfNextWorkWeek'] = 'due:' + end_of_next_work_week()
        keys['due:EndOfWeek'] = 'due:' + end_of_week()
        keys['due:EndOfNextWeek'] = 'due:' + end_of_next_week()
        keys['due:EndOfMonth'] = 'due:' + end_of_month()
        keys['due:EndOfNextMonth'] = 'due:' + end_of_next_month()
        keys['due:EndOfYear'] = 'due:' + end_of_year()
        keys['due:January'] = "due:" + end_of_month(month=1)
        keys['due:February'] = "due:" + end_of_month(month=2)
        keys['due:March'] = "due:" + end_of_month(month=3)
        keys['due:April'] = "due:" + end_of_month(month=4)
        keys['due:May'] = "due:" + end_of_month(month=5)
        keys['due:June'] = "due:" + end_of_month(month=6)
        keys['due:July'] = "due:" + end_of_month(month=7)
        keys['due:August'] = "due:" + end_of_month(month=8)
        keys['due:September'] = "due:" + end_of_month(month=9)
        keys['due:October'] = "due:" + end_of_month(month=10)
        keys['due:November'] = "due:" + end_of_month(month=11)
        keys['due:December'] = "due:" + end_of_month(month=12)


class ValuesGenerator(object):
    def __init__(self, mfile, keys):
        self._mfile = mfile
        self._dates = keys
        self._priorities = ["(" + i + ")" for i in string.ascii_uppercase]
        self._values = []
        self._completedValues = []
        self._values.extend(self._priorities)
        self.updateValues()

    def updateTodoValues(self):
        contexts = self._mfile.getAllContexts()
        projects = self._mfile.getAllProjects()
        for context in contexts:
            self._values.append('@' + context)
        for project in projects:
            self._values.append('+' + project)

    def updateCompletedValues(self):
        contexts = self._mfile.getAllContexts(True)
        projects = self._mfile.getAllProjects(True)
        for context in contexts:
            self._completedValues.append('@' + context)
        for project in projects:
            self._completedValues.append('+' + project)

    def updateValues(self):
        self.updateTodoValues()
        self.updateCompletedValues()

    def get_values(self):
        return sorted(list(OrderedDict.fromkeys(self._completedValues + self._values))) + self._dates


class TaskEditorLineEdit(QtWidgets.QLineEdit):
    def __init__(self, mfile):
        super(TaskEditorLineEdit, self).__init__()
        self.mfile = mfile
        self._values_generator = ValuesGenerator(mfile, list(CompleterSetup.autocomplete_pairs.keys()))
        model = self._values_generator.get_values()
        self._completerSetup = CompleterSetup(self)
        self._completer = QtWidgets.QCompleter(model)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._completer.activated.connect(self._insertCompletion)
        self._keysToIgnore = [QtCore.Qt.Key_Enter,
                              QtCore.Qt.Key_Return,
                              QtCore.Qt.Key_Escape,
                              QtCore.Qt.Key_Tab]

    def updateValues(self):
        self._values_generator.updateValues()

    def _insertCompletion(self, completion):
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        currentText = self.text()
        completionPrefixSize = len(self._completer.completionPrefix())
        textFirstPart = self.cursorPosition() - completionPrefixSize
        textLastPart = textFirstPart + completionPrefixSize

        if completion in self._completerSetup.autocomplete_pairs:
            completion = self.replaceAutocompleteKeys(completion)

        newtext = currentText[:textFirstPart] + completion + " " + currentText[textLastPart:]
        newCursorPos = self.cursorPosition() + (len(completion) - completionPrefixSize) + 1

        self.setText(newtext)
        self.setCursorPosition(newCursorPos)

    def replaceAutocompleteKeys(self, completion):
        if completion in self._completerSetup.autocomplete_pairs.keys():
            return self._completerSetup.autocomplete_pairs[completion]

    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1
        while i >= 0 and text[i] != " ":
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(TaskEditorLineEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()
        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)
        if len(event.text()) > 0 and len(completionPrefix) > 0:
            if event.key() not in self._keysToIgnore:
                self._completer.complete()
        if len(completionPrefix) == 0:
            self._completer.popup().hide()

    def _updateCompleterPopupItems(self, completionPrefix):
        """
        Filters the completer's popup items to only show items
        with the given prefix.
        """
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0))


if __name__ == '__main__':
    def demo():
        import sys
        app = QtGui.QApplication(sys.argv)
        values = ['@call', '@bug', '+qtodotxt', '+sqlvisualizer']
        editor = TaskEditorLineEdit(values)
        window = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(editor)
        window.setLayout(hbox)
        window.show()

        sys.exit(app.exec_())

    demo()

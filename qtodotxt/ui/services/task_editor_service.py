import string
from qtodotxt.ui.controls.autocomplete_inputdialog import AutoCompleteInputDialog
from collections import OrderedDict


class TaskEditorService(object):
    def __init__(self, parent_window):
        self._parent_window = parent_window
        self._priorities = ["("+i+")" for i in string.ascii_uppercase ]
        self._resetValues()

    def _resetValues(self):
        self._values = []
        self._completedValues = []
        self._values.extend(self._priorities)

    def updateTodoValues(self, file):
        contexts = file.getAllContexts()
        projects = file.getAllProjects()
        for context in contexts:
            self._values.append('@' + context)
        for project in projects:
            self._values.append('+' + project)

    def updateCompletedValues(self, file):
        contexts = file.getAllCompletedContexts()
        projects = file.getAllCompletedProjects()
        for context in contexts:
            self._completedValues.append('@' + context)
        for project in projects:
            self._completedValues.append('+' + project)

    def updateValues(self, file):
        self._resetValues()
        self.updateTodoValues(file)
        self.updateCompletedValues(file)

    def createTask(self):
        (text, ok) = self._openTaskEditor("Create Task")
        return text, ok

    def editTask(self, task):
        (text, ok) = self._openTaskEditor('Edit Task', task)
        return text, ok

    def _openTaskEditor(self, title, task=None):
        uniqlist = sorted(list(OrderedDict.fromkeys(self._completedValues+self._values)))
        dialog = AutoCompleteInputDialog(uniqlist, self._parent_window)
        dialog.setWindowTitle(title)
        dialog.setLabelText('Task:')
        dialog.resize(500, 100)
        if task:
            dialog.setTextValue(task.text)
        dialog.setModal(True)
        if dialog.exec_():
            return dialog.textValue(), True
        return None, False


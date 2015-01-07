import string
from qtodotxt.ui.controls.autocomplete_inputdialog import AutoCompleteInputDialog
from collections import OrderedDict
from qtodotxt.lib import settings

class TaskEditorService(object):
    def __init__(self, parent_window, settings):
        self._parent_window = parent_window
        self._priorities = ["("+i+")" for i in string.ascii_uppercase ]
        self._resetValues()
        self._multilineTasks = False
        self._settings = settings

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

    def setMultilineTasks(self,multilineTasks):
        self._multilineTasks = multilineTasks

    def createTask(self):
        (text, ok) = self._openTaskEditor("Create Task")
        return text, ok

    def editTask(self, task):
        (text, ok) = self._openTaskEditor('Edit Task', task)
        return text, ok

    def _openTaskEditor(self, title, task=None):
        uniqlist = sorted(list(OrderedDict.fromkeys(self._completedValues+self._values)))
        dialog = AutoCompleteInputDialog(uniqlist, self._parent_window, self._settings.getSupportMultilineTasks())
        dialog.setWindowTitle(title)
        dialog.setLabelText('Task:')
        
        self._restoreMultilineDialogDimensions(dialog)

        if task:
            dialog.setTextValue(task.text)
        dialog.setModal(True)
        
        dlgReturn = dialog.exec_()
        
        self._saveMultilineDialogDimensions(dialog)
        
        if dlgReturn:
            return dialog.textValue(), True
        return None, False

    def _restoreMultilineDialogDimensions(self,dialog):
        if self._settings.getSupportMultilineTasks():
            height = self._settings.getEditViewHeight()
            width = self._settings.getEditViewWidth()
            if height and width:
                dialog.resize(width, height)
        else:
            dialog.resize(500,100)

    def _saveMultilineDialogDimensions(self,dialog):
        if self._settings.getSupportMultilineTasks():
            height = dialog.size().height()
            width = dialog.size().width()
            self._settings.setEditViewHeight(height)
            self._settings.setEditViewWidth(width)

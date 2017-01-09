import string
from qtodotxt.ui.dialogs.taskeditor_dialog import TaskEditorDialog
from PyQt5 import QtCore


class TaskEditor(object):

    def __init__(self, parent_window, mfile):
        self._parent_window = parent_window
        self._mfile = mfile
        self.priorities = ["(" + i + ")" for i in string.ascii_uppercase]

    def createTask(self, task=None):
        _tr = QtCore.QCoreApplication.translate
        (text, ok) = self._openTaskEditor(_tr("taskEditor", "Create Task"), task)
        return text, ok

    def editTask(self, task):
        _tr = QtCore.QCoreApplication.translate
        (text, ok) = self._openTaskEditor(_tr("taskEditor", 'Edit Task'), task)
        return text, ok

    def _openTaskEditor(self, title, task=None):
        dialog = TaskEditorDialog(self._parent_window, self._mfile)
        dialog.setWindowTitle(title)
        dialog.setLabelText('Task:')
        dialog.resize(500, 100)
        if task:
            dialog.setTextValue(task.text)
        #dialog.setModal(True)
        if dialog.exec_():
            return dialog.textValue(), True
        return None, False

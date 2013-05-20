from qtodotxt.ui.controls.autocomplete_inputdialog import AutoCompleteInputDialog

class TaskEditorService(object):
    def __init__(self, parent_window):
        self._parent_window = parent_window
        self._priorities = ['(A)', '(B)', '(C)']
        self._resetValues()

    def _resetValues(self):
        self._values = []
        self._values.extend(self._priorities)

    def updateValues(self, file):
        self._resetValues()
        contexts = file.getAllContexts()
        projects = file.getAllProjects()
        for context in contexts:
            self._values.append('@' + context)
        for project in projects:
            self._values.append('+' + project)

    def createTask(self):
        (text, ok) = self._openTaskEditor("Create Task")
        return (text, ok)
    
    def editTask(self, task):
        (text, ok) = self._openTaskEditor('Edit Task', task)
        return (text, ok)

    def _openTaskEditor(self, title, task=None):
        dialog = AutoCompleteInputDialog(self._values, self._parent_window)
        dialog.setWindowTitle(title)
        dialog.setLabelText('Task:')
        dialog.resize(500, 100)
        if task:
            dialog.setTextValue(task.text)
        dialog.setModal(True)
        if dialog.exec_():
            return (dialog.textValue(), True)
        return (None, False)


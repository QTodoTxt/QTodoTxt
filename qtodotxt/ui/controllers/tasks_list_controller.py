from PyQt5 import QtCore
from PyQt5 import QtWidgets

from qtodotxt.lib import tasklib
from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.ui.resource_manager import getIcon

from datetime import date


class TasksListController(QtCore.QObject):

    taskModified = QtCore.pyqtSignal(tasklib.Task)
    taskCreated = QtCore.pyqtSignal(tasklib.Task)
    taskArchived = QtCore.pyqtSignal(tasklib.Task)
    taskDeleted = QtCore.pyqtSignal(tasklib.Task)

    def __init__(self, view, task_editor_service):
        QtCore.QObject.__init__(self)
        self.view = view
        self._task_editor_service = task_editor_service
        self._task_htmlizer = TaskHtmlizer()
        self.view.taskActivated.connect(self.editTask)
        self._initCreateTaskAction()
        self._initEditTaskAction()
        if int(QtCore.QSettings().value("show_delete", 0)):
            self._initDeleteSelectedTasksAction()
        self._initCompleteSelectedTasksAction()
        self._initDecreasePrioritySelectedTasksAction()
        self._initIncreasePrioritySelectedTasksAction()

    def _initEditTaskAction(self):
        action = QtWidgets.QAction(getIcon('TaskEdit.png'), '&Edit Task', self)
        action.setShortcuts(['Ctrl+E'])
        action.triggered.connect(self.editTask)
        self.view.addListAction(action)
        self.editTaskAction = action

    def _initCreateTaskAction(self):
        action = QtWidgets.QAction(getIcon('TaskCreate.png'), '&Create New Task', self)
        action.setShortcuts(['Insert', 'Ctrl+I', 'Ctrl+N'])
        action.triggered.connect(self.createTask)
        self.view.addListAction(action)
        self.createTaskAction = action

    def _initDeleteSelectedTasksAction(self):
        action = QtWidgets.QAction(getIcon('TaskDelete.png'), '&Delete Selected Tasks', self)
        action.setShortcut('Delete')
        action.triggered.connect(self._deleteSelectedTasks)
        self.view.addListAction(action)
        self.deleteSelectedTasksAction = action

    def _initCompleteSelectedTasksAction(self):
        action = QtWidgets.QAction(getIcon('TaskComplete.png'), 'C&omplete Selected Tasks', self)
        action.setShortcuts(['x', 'c'])
        action.triggered.connect(self._completeSelectedTasks)
        self.view.addListAction(action)
        self.completeSelectedTasksAction = action

    def _initDecreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(getIcon('TaskPriorityDecrease.png'), 'Decrease Priority', self)
        action.setShortcuts(['-', '<'])
        action.triggered.connect(self._decreasePriority)
        self.view.addListAction(action)
        self.decreasePrioritySelectedTasksAction = action

    def _initIncreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(getIcon('TaskPriorityIncrease.png'), 'Increase Priority', self)
        action.setShortcuts(['+', '>'])
        action.triggered.connect(self._increasePriority)
        self.view.addListAction(action)
        self.increasePrioritySelectedTasksAction = action

    def completeTask(self, task):
        if not task.is_complete:
            task.setCompleted()
        else:
            task.setPending()
        if int(QtCore.QSettings().value("auto_archive", 0)):
            self.taskArchived.emit(task)
        else:
            self.taskModified.emit(task)

    def _completeSelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            confirm = int(QtCore.QSettings().value("confirm_complete", 1))
            if not confirm or self._confirmTasksAction(tasks, 'Toggle Completeness of'):
                for task in tasks:
                    self.completeTask(task)

    def _deleteSelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            if self._confirmTasksAction(tasks, 'Delete'):
                for task in tasks:
                    self.view.removeTask(task)
                    self.taskDeleted.emit(task)

    def _confirmTasksAction(self, tasks, messagePrefix):
        if len(tasks) == 1:
            message = '<b>%s the following task?</b><ul>' % messagePrefix
        else:
            message = '<b>%s the following tasks?</b><ul>' % messagePrefix
        for task in tasks:
            message += '<li>%s</li>' % self._task_htmlizer.task2html(task)
        message += '</ul>'
        result = QtWidgets.QMessageBox.question(self.view,
                                                'Confirm',
                                                message,
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                defaultButton=QtWidgets.QMessageBox.Yes
                                                )
        return result == QtWidgets.QMessageBox.Yes

    def _decreasePriority(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.decreasePriority()
                self.view.updateTask(task)
                self.taskModified.emit(task)

    def _increasePriority(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.increasePriority()
                self.view.updateTask(task)
                self.taskModified.emit(task)

    def showTasks(self, tasks):
        previouslySelectedTasks = self.view.getSelectedTasks()
        self.view.clear()
        self._sortTasks(tasks)
        for task in tasks:
            self.view.addTask(task)
        self._reselect(previouslySelectedTasks)

    def _reselect(self, tasks):
        for task in tasks:
            self.view.selectTaskByText(task.text)

    def _sortTasks(self, tasks):
        tasks.sort(reverse=True)

    def _addCreationDate(self, text):
        date_string = date.today().strftime('%Y-%m-%d')
        if text[:3] in self._task_editor_service._priorities:
            text = '%s %s %s' % (text[:3], date_string, text[4:])
        else:
            text = '%s %s' % (date_string, text)
        return text

    def createTask(self):
        (text, ok) = self._task_editor_service.createTask()
        if ok and text:
            if int(QtCore.QSettings().value("add_created_date", 0)):
                text = self._addCreationDate(text)
            task = tasklib.Task(text)
            self.view.addTask(task)
            self.view.clearSelection()
            self.view.selectTask(task)
            self.taskCreated.emit(task)

    def editTask(self, task=None):
        if not task:
            tasks = self.view.getSelectedTasks()
            # FIXME: instead of this we should disable icon when no task or serveral tasks are selected
            if len(tasks) == 0:
                print("No task selected")
                return
            elif len(tasks) > 1:
                print("More than one task selected")
                return
            task = tasks[0]
        (text, ok) = self._task_editor_service.editTask(task)
        if ok and text:
            if text != task.text:
                task.parseLine(text)
                self.view.updateTask(task)
                self.taskModified.emit(task)

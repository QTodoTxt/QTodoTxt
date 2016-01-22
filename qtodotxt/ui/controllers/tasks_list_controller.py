from PySide import QtCore
from PySide import QtGui
from qtodotxt.lib import task_parser
from qtodotxt.ui.resource_manager import getIcon
from datetime import date
from functools import cmp_to_key


class TasksListController(QtCore.QObject):

    taskModified = QtCore.Signal(task_parser.Task)
    taskCreated = QtCore.Signal(task_parser.Task)
    taskArchived = QtCore.Signal(task_parser.Task)
    taskDeleted = QtCore.Signal(task_parser.Task)

    def __init__(self, view, task_editor_service):
        QtCore.QObject.__init__(self)
        self._view = view
        self._task_editor_service = task_editor_service
        self._view.taskActivated.connect(self.editTask)
        self._initCreateTaskAction()
        self._initDeleteSelectedTasksAction()
        self._initCompleteSelectedTasksAction()
        self._initDecreasePrioritySelectedTasksAction()
        self._initIncreasePrioritySelectedTasksAction()

    def _initCreateTaskAction(self):
        action = QtGui.QAction(getIcon('add.svg'), '&Create New Task', self)
        action.setShortcuts(['Insert', 'Ctrl+I', 'Ctrl+N'])
        action.triggered.connect(self.createTask)
        self._view.addListAction(action)
        self.createTaskAction = action

    def _initDeleteSelectedTasksAction(self):
        action = QtGui.QAction(getIcon('delete.svg'), '&Delete Selected Tasks', self)
        action.setShortcut('Delete')
        action.triggered.connect(self._deleteSelectedTasks)
        self._view.addListAction(action)
        self.deleteSelectedTasksAction = action

    def _initCompleteSelectedTasksAction(self):
        action = QtGui.QAction(getIcon('checked.svg'), 'C&omplete Selected Tasks', self)
        action.setShortcuts(['x', 'c'])
        action.triggered.connect(self._completeSelectedTasks)
        self._view.addListAction(action)
        self.completeSelectedTasksAction = action

    def _initDecreasePrioritySelectedTasksAction(self):
        action = QtGui.QAction(getIcon('decrease.svg'), 'Decrease Priority', self)
        action.setShortcuts(['-', '<'])
        action.triggered.connect(self._decreasePriority)
        self._view.addListAction(action)
        self.decreasePrioritySelectedTasksAction = action

    def _initIncreasePrioritySelectedTasksAction(self):
        action = QtGui.QAction(getIcon('increase.svg'), 'Increase Priority', self)
        action.setShortcuts(['+', '>'])
        action.triggered.connect(self._increasePriority)
        self._view.addListAction(action)
        self.increasePrioritySelectedTasksAction = action

    def completeTask(self, task):
        date_string = date.today().strftime('%Y-%m-%d')
        if not task.is_complete:
            task.text = 'x %s %s' % (date_string, task.text)
            if int(QtCore.QSettings().value("auto_archive", 1)):
                self.taskArchived.emit(task)
            else:
                self.taskModified.emit(task)

    def _completeSelectedTasks(self):
        tasks = self._view.getSelectedTasks()
        if tasks:
            if self._confirmTasksAction(tasks, 'Complete'):
                for task in tasks:
                    self.completeTask(task)

    def _deleteSelectedTasks(self):
        tasks = self._view.getSelectedTasks()
        if tasks:
            if self._confirmTasksAction(tasks, 'Delete'):
                for task in tasks:
                    self._view.removeTask(task)
                    self.taskDeleted.emit(task)

    def _confirmTasksAction(self, tasks, messagePrefix):
        if len(tasks) == 1:
            message = '%s "%s"?' % (messagePrefix, tasks[0].text)
        else:
            message = '%s %d tasks?' % (messagePrefix, len(tasks))

        result = QtGui.QMessageBox.question(self._view, 'Confirm', message,
                                            buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            defaultButton=QtGui.QMessageBox.Yes)

        return result == QtGui.QMessageBox.Yes

    def _decreasePriority(self):
        tasks = self._view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.decreasePriority()
                self._view.updateTask(task)
                self.taskModified.emit(task)

    def _increasePriority(self):
        tasks = self._view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.increasePriority()
                self._view.updateTask(task)
                self.taskModified.emit(task)

    def showTasks(self, tasks):
        previouslySelectedTasks = self._view.getSelectedTasks()
        self._view.clear()
        self._sortTasks(tasks)
        for task in tasks:
            self._view.addTask(task)
        self._reselect(previouslySelectedTasks)

    def _reselect(self, tasks):
        for task in tasks:
            self._view.selectTaskByText(task.text)

    def _sortTasks(self, tasks):
        tasks.sort(key=cmp_to_key(task_parser.compareTasks))

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
            if int(QtCore.QSettings().value("add_created_date", 1)):
                text = self._addCreationDate(text)
            task = task_parser.Task(text)
            self._view.addTask(task)
            self._view.clearSelection()
            self._view.selectTask(task)
            self.taskCreated.emit(task)

    def editTask(self, task):
        (text, ok) = self._task_editor_service.editTask(task)
        if ok and text:
            if text != task.text:
                task.text = text
                self._view.updateTask(task)
                self.taskModified.emit(task)

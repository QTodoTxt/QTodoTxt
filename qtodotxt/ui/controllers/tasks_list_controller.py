from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from qtodotxt.lib import tasklib
from qtodotxt.lib.task_htmlizer import TaskHtmlizer

from datetime import date

import os


class TasksListController(QtCore.QObject):

    taskModified = QtCore.pyqtSignal(tasklib.Task)
    taskCreated = QtCore.pyqtSignal(tasklib.Task)
    taskArchived = QtCore.pyqtSignal(tasklib.Task)
    taskDeleted = QtCore.pyqtSignal(tasklib.Task)

    def __init__(self, view, task_editor_service):
        QtCore.QObject.__init__(self)
        self.style = ":/white_icons"
        if str(QtCore.QSettings().value("color_schem", "")).find("dark") >= 0:
            self.style = ":/dark_icons"
        self.view = view
        self._task_editor_service = task_editor_service
        self._task_htmlizer = TaskHtmlizer()
        self.view.taskActivated.connect(self.editTask)
        self.view.itemSelectionChanged.connect(self.updateActions)
        self._initCreateTaskAction()
        self._initEditTaskAction()
        self._initCopySelectedTasksAction()
        if int(QtCore.QSettings().value("show_delete", 1)):
            self._initDeleteSelectedTasksAction()
        self._initCompleteSelectedTasksAction()
        self._initDecreasePrioritySelectedTasksAction()
        self._initIncreasePrioritySelectedTasksAction()
        self._initCreateTaskActionOnTemplate()
        self.disableTaskActions()

    def _initEditTaskAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style +
                                               '/resources/TaskEdit.png'), self.tr('&Edit Task'), self)
        action.setShortcuts(['Ctrl+E', 'Enter'])
        action.setDisabled(True)
        action.triggered.connect(self.editTask)
        self.view.addListAction(action)
        self.editTaskAction = action

    def _initCreateTaskAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskCreate.png'),
                                   self.tr('&Create New Task'), self)
        action.setShortcuts(['Insert', 'Ctrl+I', 'Ctrl+N'])
        action.triggered.connect(self.createTask)
        self.view.addListAction(action)
        self.createTaskAction = action

    def _initCreateTaskActionOnTemplate(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskAddOnTem.png'),
                                   self.tr('&Create a new Task based on a template'), self)
        action.setShortcuts(['Shift+Insert', 'Ctrl+Shift+I'])
        action.triggered.connect(self.createTaskOnTemplate)
        self.view.addListAction(action)
        self.createTaskActionOnTemplate = action

    def _initCopySelectedTasksAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskCopy.png'),
                                   self.tr('Copy Selected Tasks'), self)
        action.setShortcuts([QtGui.QKeySequence.Copy])
        action.triggered.connect(self._copySelectedTasks)
        self.view.addListAction(action)
        self.copySelectedTasksAction = action

    def _initDeleteSelectedTasksAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskDelete.png'),
                                   self.tr('&Delete Selected Tasks'), self)
        action.setShortcut('Delete')
        action.triggered.connect(self._deleteSelectedTasks)
        self.view.addListAction(action)
        self.deleteSelectedTasksAction = action

    def _initCompleteSelectedTasksAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskComplete.png'),
                                   self.tr('C&omplete Selected Tasks'), self)
        action.setShortcuts(['x', 'c'])
        action.triggered.connect(self._completeSelectedTasks)
        self.view.addListAction(action)
        self.completeSelectedTasksAction = action

    def _initDecreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskPriorityDecrease.png'),
                                   self.tr('Decrease Priority'), self)
        action.setShortcuts(['-', '<'])
        action.triggered.connect(self._decreasePriority)
        self.view.addListAction(action)
        self.decreasePrioritySelectedTasksAction = action

    def _initIncreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskPriorityIncrease.png'),
                                   self.tr('Increase Priority'), self)
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
            if not confirm or self._confirmTasksAction(tasks, self.tr('Toggle Completeness of')):
                for task in tasks:
                    self.completeTask(task)

    def _deleteSelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            if self._confirmTasksAction(tasks, self.tr('Delete')):
                for task in tasks:
                    self.view.removeTask(task)
                    self.taskDeleted.emit(task)

    def _confirmTasksAction(self, tasks, messagePrefix):
        if len(tasks) == 1:
            message = self.tr('<b>%s the following task?</b><ul>') % messagePrefix
        else:
            message = self.tr('<b>%s the following tasks?</b><ul>') % messagePrefix
        for task in tasks:
            message += '<li>%s</li>' % self._task_htmlizer.task2html(task)
        message += '</ul>'
        result = QtWidgets.QMessageBox.question(self.view,
                                                self.tr('Confirm'),
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

    def createTaskOnTemplate(self):
        tasks = self.view.getSelectedTasks()
        if len(tasks) != 1:
            return
        task = tasks[0]
        (text, ok) = self._task_editor_service.createTask(task)
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
            task = tasks[0]
        (text, ok) = self._task_editor_service.editTask(task)
        if ok and text:
            if text != task.text:
                task.parseLine(text)
                self.view.updateTask(task)
                self.taskModified.emit(task)

    def _copySelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            text = "".join(str(task) + os.linesep for task in tasks)
            app = QtWidgets.QApplication.instance()
            app.clipboard().setText(text)

    def updateActions(self):
        if len(self.view.getSelectedTasks()) > 0:
            self.enableTaskActions()
            if len(self.view.getSelectedTasks()) > 1:
                self.editTaskAction.setEnabled(False)
                self.createTaskActionOnTemplate.setEnabled(False)
        else:
            self.disableTaskActions()

    def enableTaskActions(self):
        self.editTaskAction.setEnabled(True)
        self.createTaskActionOnTemplate.setEnabled(True)
        self.deleteSelectedTasksAction.setEnabled(True)
        self.completeSelectedTasksAction.setEnabled(True)
        self.copySelectedTasksAction.setEnabled(True)
        self.increasePrioritySelectedTasksAction.setEnabled(True)
        self.decreasePrioritySelectedTasksAction.setEnabled(True)

    def disableTaskActions(self):
        self.editTaskAction.setEnabled(False)
        self.createTaskActionOnTemplate.setEnabled(False)
        self.deleteSelectedTasksAction.setEnabled(False)
        self.completeSelectedTasksAction.setEnabled(False)
        self.copySelectedTasksAction.setEnabled(False)
        self.increasePrioritySelectedTasksAction.setEnabled(False)
        self.decreasePrioritySelectedTasksAction.setEnabled(False)

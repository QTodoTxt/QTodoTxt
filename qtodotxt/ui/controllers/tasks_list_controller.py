import os
import string
from datetime import date
from datetime import timedelta
import re

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from qtodotxt.lib import tasklib
from qtodotxt.lib.task_htmlizer import TaskHtmlizer

from qtodotxt.lib.tasklib import recursiveMode


class LinkDialog(QtWidgets.QFileDialog):
    def __init__(self, parent, directory):
        QtWidgets.QFileDialog.__init__(self, parent, caption="Select file", directory=directory)
        self.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.setViewMode(QtWidgets.QFileDialog.Detail)

    @staticmethod
    def getLink(parent, directory):
        dia = LinkDialog(parent, directory=directory)
        if dia.exec_():
            return [uri.toString() for uri in dia.selectedUrls()]


class TasksListController(QtCore.QObject):

    taskModified = QtCore.pyqtSignal(tasklib.Task)
    taskCreated = QtCore.pyqtSignal(tasklib.Task)
    taskArchived = QtCore.pyqtSignal(tasklib.Task)
    taskDeleted = QtCore.pyqtSignal(tasklib.Task)

    def __init__(self, view, mfile):
        QtCore.QObject.__init__(self)
        self.style = ":/white_icons"
        if str(QtCore.QSettings().value("color_schem", "")).find("dark") >= 0:
            self.style = ":/dark_icons"
        self._settings = QtCore.QSettings()
        self.view = view
        self.view.setFileObject(mfile)
        self._task_htmlizer = TaskHtmlizer()
        self._priorities = ["(" + i + ")" for i in string.ascii_uppercase]  # FIXME: why do we have this?
        self.view.taskActivated.connect(self.view.editCurrentTask)
        self.view.currentTaskChanged.connect(self.updateActions)
        self.view.taskDeleted.connect(self.taskDeleted.emit)
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
        self._initAddLinkAction()
        self.view.taskCreated.connect(self._task_created)
        self.view.taskModified.connect(self._task_modified)
        self.disableTaskActions()

    def _task_created(self, task):
        self.view.clearSelection()
        self.view.selectTask(task)
        self.taskCreated.emit(task)

    def _task_modified(self, task):
        self.taskModified.emit(task)

    def _initEditTaskAction(self):
        action = QtWidgets.QAction(QtGui.QIcon(self.style + '/resources/TaskEdit.png'), self.tr('&Edit Task'), self)
        action.setShortcuts(['Ctrl+E', 'Enter'])
        action.setDisabled(True)
        action.triggered.connect(self.view.editCurrentTask)
        self.view.addAction(action)
        self.editTaskAction = action

    def _initCreateTaskAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskCreate.png'), self.tr('&Create new task'), self)
        action.setShortcuts(['Insert', 'Ctrl+I', 'Ctrl+N'])
        action.triggered.connect(self.view.createTask)
        self.view.addAction(action)
        self.createTaskAction = action

    def _initCreateTaskActionOnTemplate(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskAddOnTem.png'),
            self.tr('&Create a new task based on current task'), self)
        action.setShortcuts(['Shift+Insert', 'Ctrl+Shift+I'])
        action.triggered.connect(self.createTaskOnTemplate)
        self.view.addAction(action)
        self.createTaskActionOnTemplate = action

    def _initCopySelectedTasksAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskCopy.png'), self.tr('Copy selected tasks'), self)
        action.setShortcuts([QtGui.QKeySequence.Copy])
        action.triggered.connect(self._copySelectedTasks)
        self.view.addAction(action)
        self.copySelectedTasksAction = action

    def _initDeleteSelectedTasksAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskDelete.png'), self.tr('&Delete selected tasks'), self)
        action.setShortcut('Delete')
        action.triggered.connect(self._deleteSelectedTasks)
        self.view.addAction(action)
        self.deleteSelectedTasksAction = action

    def _initCompleteSelectedTasksAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskComplete.png'), self.tr('C&omplete selected tasks'), self)
        action.setShortcuts(['x', 'c'])
        action.triggered.connect(self._completeSelectedTasks)
        self.view.addAction(action)
        self.completeSelectedTasksAction = action

    def _initDecreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskPriorityDecrease.png'), self.tr('Decrease priority'), self)
        action.setShortcuts(['-', '<'])
        action.triggered.connect(self._decreasePriority)
        self.view.addAction(action)
        self.decreasePrioritySelectedTasksAction = action

    def _initIncreasePrioritySelectedTasksAction(self):
        action = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/TaskPriorityIncrease.png'), self.tr('Increase priority'), self)
        action.setShortcuts(['+', '>'])
        action.triggered.connect(self._increasePriority)
        self.view.addAction(action)
        self.increasePrioritySelectedTasksAction = action

    def _initAddLinkAction(self):
        self.addLinkAction = QtWidgets.QAction(
            QtGui.QIcon(self.style + '/resources/link.png'), self.tr('Add &Link to file'), self)
        self.addLinkAction.setShortcuts(['Ctrl+Shift+L'])
        self.view.addAction(self.addLinkAction)
        self.addLinkAction.triggered.connect(self._addLink)

    def _addLink(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            uris = LinkDialog.getLink(self.view, directory=".")
            if uris:
                for uri in uris:
                    for task in tasks:
                        task.text = task.text + " " + uri
                        self.taskModified.emit(task)

    def completeTask(self, task):
        if not task.is_complete:
            # Check if task is recurrent and has a due date
            if task.recursion is not None and task.due is not None:
                self._recurTask(task)
            task.setCompleted()  # maybe we should not do that is show_completed is True....
            self.view.selectNext()
        else:
            task.setPending()
        if int(QtCore.QSettings().value("auto_archive", 0)):
            self.taskArchived.emit(task)
        else:
            self.taskModified.emit(task)

    def _recurTask(self, task):
        if task.recursion.interval == 'd':
            if task.recursion.mode == recursiveMode.originalDueDate:
                next_due_date = task.due + timedelta(days=int(task.recursion.increment))
            else:
                next_due_date = date.today() + timedelta(days=int(task.recursion.increment))
        elif task.recursion.interval == 'b':
            if task.recursion.mode == recursiveMode.originalDueDate:
                next_due_date = self._incrWorkDays(task.due, int(task.recursion.increment))
            else:
                next_due_date = self._incrWorkDays(date.today(), int(task.recursion.increment))
        elif task.recursion.interval == 'w':
            if task.recursion.mode == recursiveMode.originalDueDate:
                next_due_date = task.due + timedelta(weeks=int(task.recursion.increment))
            else:
                next_due_date = date.today() + timedelta(weeks=int(task.recursion.increment))
        elif task.recursion.interval == 'm':
            if task.recursion.mode == recursiveMode.originalDueDate:
                next_due_date = task.due + timedelta(weeks=int(task.recursion.increment) * 4)  # 4 weeks in a month
            else:
                next_due_date = date.today() + timedelta(weeks=int(task.recursion.increment) * 4)  # 4 weeks in a month
        elif task.recursion.interval == 'y':
            if task.recursion.mode == recursiveMode.originalDueDate:
                next_due_date = task.due + timedelta(weeks=int(task.recursion.increment) * 52)  # 52 weeks in a year
            else:
                next_due_date = date.today() + timedelta(weeks=int(task.recursion.increment) * 52)  # 52 weeks in a year
        else:
            # Test already made during line parsing - shouldn't be a problem here
            pass
        # Set new due date in old task text
        rec_text = task.updateDateInTask(task.text, next_due_date)
        # create a new task duplicate
        self._createTask(rec_text)
        return

    def _incrWorkDays(self, startDate, daysToIncrement):
        while daysToIncrement > 0:
            if startDate.weekday() == 4:  # Friday
                startDate = startDate + timedelta(days=3)
            elif startDate.weekday() == 5:  # Saturday
                startDate = startDate + timedelta(days=2)
            else:
                startDate = startDate + timedelta(days=1)
            daysToIncrement -= 1
        return startDate

    def _completeSelectedTasks(self):

        tasks = self.view.getSelectedTasks()
        if tasks:
            confirm = int(QtCore.QSettings().value("confirm_complete", 1))
            if not confirm or self._confirmTasksAction(tasks, self.tr('Toggle completeness of')):
                for task in tasks:
                    self.completeTask(task)

    def _deleteSelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            if self._confirmTasksAction(tasks, self.tr('Delete')):
                for task in tasks:
                    self.view.removeTask(task)
                    self.taskDeleted.emit(task)
                    self.view.selectNext()

    def _confirmTasksAction(self, tasks, messagePrefix):
        if len(tasks) == 1:
            message = self.tr('<b>%s the following task?</b><ul>') % messagePrefix
        else:
            message = self.tr('<b>%s the following tasks?</b><ul>') % messagePrefix
        for task in tasks:
            message += '<li>%s</li>' % self._task_htmlizer.task2html(task)
        message += '</ul>'
        result = QtWidgets.QMessageBox.question(
            self.view,
            self.tr('Confirm'),
            message,
            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            defaultButton=QtWidgets.QMessageBox.Yes)
        return result == QtWidgets.QMessageBox.Yes

    def _decreasePriority(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.decreasePriority()
                self.taskModified.emit(task)

    def _increasePriority(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            for task in tasks:
                task.increasePriority()
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

    def _removeCreationDate(self, text):
        match = re.match(r'^(\([A-Z]\)\s)?[0-9]{4}\-[0-9]{2}\-[0-9]{2}\s(.*)', text)
        if match:
            if match.group(1):
                text = match.group(1) + match.group(2)
            else:
                text = match.group(2)
        return text

    def _addCreationDate(self, text):
        date_string = date.today().strftime('%Y-%m-%d')
        if text[:3] in self._priorities:
            text = '%s %s %s' % (text[:3], date_string, text[4:])
        else:
            text = '%s %s' % (date_string, text)
        return text

    def _createTask(self, text):
        if int(QtCore.QSettings().value("add_created_date", 0)):
            text = self._removeCreationDate(text)
            text = self._addCreationDate(text)
        task = tasklib.Task(text)
        self.view.addTask(task)
        self._task_created(task)
        return task

    def createTaskOnTemplate(self):
        tasks = self.view.getSelectedTasks()
        if len(tasks) != 1:
            return
        task = tasks[0]
        return self.view.createTask(task)

    def _copySelectedTasks(self):
        tasks = self.view.getSelectedTasks()
        if tasks:
            text = "".join(str(task) + os.linesep for task in tasks)
            app = QtWidgets.QApplication.instance()
            app.clipboard().setText(text)

    def updateActions(self):
        tasks = self.view.selectedItems()
        if tasks:
            self.enableTaskActions()
            if len(tasks) > 1:
                self.editTaskAction.setEnabled(False)
                self.addLinkAction.setEnabled(False)
                self.createTaskActionOnTemplate.setEnabled(False)
        else:
            self.disableTaskActions()

    def enableTaskActions(self):
        self.editTaskAction.setEnabled(True)
        self.addLinkAction.setEnabled(True)
        self.createTaskActionOnTemplate.setEnabled(True)
        self.deleteSelectedTasksAction.setEnabled(True)
        self.completeSelectedTasksAction.setEnabled(True)
        self.copySelectedTasksAction.setEnabled(True)
        self.increasePrioritySelectedTasksAction.setEnabled(True)
        self.decreasePrioritySelectedTasksAction.setEnabled(True)

    def disableTaskActions(self):
        self.editTaskAction.setEnabled(False)
        self.addLinkAction.setEnabled(False)
        self.createTaskActionOnTemplate.setEnabled(False)
        self.deleteSelectedTasksAction.setEnabled(False)
        self.completeSelectedTasksAction.setEnabled(False)
        self.copySelectedTasksAction.setEnabled(False)
        self.increasePrioritySelectedTasksAction.setEnabled(False)
        self.decreasePrioritySelectedTasksAction.setEnabled(False)

import logging
from PySide import QtCore
from PySide import QtGui
from qtodotxt.lib.task import Task

logger = logging.getLogger(__name__)


class TasksListView(QtGui.QListWidget):

    taskActivated = QtCore.Signal(Task)

    def __init__(self, parent=None):
        super(TasksListView, self).__init__(parent)
        self.setLayoutMode(self.LayoutMode.Batched)
        self._initUI()
        self._oldSelected = []

    def addTask(self, task):
        item = TaskListWidgetItem(task, self)
        label = self._createLabel(task)
        self.setItemWidget(item, label)
        logger.debug('Added task-item ({}) to {}'.format(item, self))

    def addListAction(self, action):
        self.addAction(action)

    def _initUI(self):
        self.setSelectionMode(
            QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.itemDoubleClicked.connect(self._list_itemActivated)
        self.itemSelectionChanged.connect(self._list_itemPressed)

    def _createLabel(self, task):
        label = QtGui.QLabel()
        label.setTextFormat(QtCore.Qt.RichText)
        label.setOpenExternalLinks(True)
        text = task.html
        label.setText(text)
        logger.debug('Created label with text: {}'.format(text))
        return label

    def _findItemByTask(self, task):
        for index in range(self.count()):
            item = self.item(index)
            if item.task is task:
            # DEBUG below was before / does it count?
            #if item.task == task:
                return item
        return None

    def _findItemByTaskText(self, text):
        for index in range(self.count()):
            item = self.item(index)
            if str(item.task) == text:
                return item
        return None

    def updateTask(self, task):
        item = self._findItemByTask(task)
        label = self.itemWidget(item)
        text = item.task.html
        label.setText(text)
        logger.debug('Set label text of {} to: {}'.format(item, text))

    def _selectItem(self, item):
        if item:
            item.setSelected(True)
            self.setCurrentItem(item)

    def selectTask(self, task):
        item = self._findItemByTask(task)
        self._selectItem(item)

    def selectTaskByText(self, text):
        item = self._findItemByTaskText(text)
        self._selectItem(item)

    def removeTask(self, task):
        item = self._findItemByTask(task)
        if item:
            self._oldSelected.remove(item)
            self.removeItemWidget(item)

    def _list_itemActivated(self, item):
        self.taskActivated.emit(item.task)

    def getSelectedTasks(self):
        items = self.selectedItems()
        return [item.task for item in items]

    def _list_itemPressed(self):
        for oldSelected in self._oldSelected:
            label = self.itemWidget(oldSelected)
            text = oldSelected.task.html
            label.setText(text)
        self._oldSelected = []
        items = self.selectedItems()
        for item in items:
            self._oldSelected.append(item)
            label = self.itemWidget(item)
            text = item.task.html
            label.setText(text)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            items = self.selectedItems()
            if len(items) > 0:
                self._list_itemActivated(items[-1])
        else:
            QtGui.QListWidget.keyPressEvent(self, event)
            return


class TaskListWidgetItem(QtGui.QListWidgetItem):

    def __init__(self, task, list):
        QtGui.QListWidgetItem.__init__(self, '', list)
        self.task = task

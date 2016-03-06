from PyQt5 import QtCore
from PyQt5 import QtWidgets
from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.lib import tasklib


class TasksListView(QtWidgets.QListWidget):

    taskActivated = QtCore.pyqtSignal(tasklib.Task)

    def __init__(self, parent=None):
        super(TasksListView, self).__init__(parent)
        self.setLayoutMode(self.Batched)
        self.setAlternatingRowColors(True)
        self._task_htmlizer = TaskHtmlizer()
        self._initUI()
        self._oldSelected = []

    def addTask(self, task):
        item = TaskListWidgetItem(task, self)
        label = self._createLabel(task)
        label.setWordWrap(True)
        # set minimum width to a reasonable value to get a useful
        # sizeHint _height_ when using word wrap
        label.setMinimumWidth(self.width() - 20)
        # set items size and add some space between items
        item.setSizeHint(QtCore.QSize(label.sizeHint().width(),
                                      label.sizeHint().height() + 5))
        self.setItemWidget(item, label)

    def addListAction(self, action):
        self.addAction(action)

    def _initUI(self):
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.itemDoubleClicked.connect(self._list_itemActivated)
        self.itemSelectionChanged.connect(self._list_itemPressed)

    def _createLabel(self, task):
        label = QtWidgets.QLabel()
        label.setTextFormat(QtCore.Qt.RichText)
        label.setOpenExternalLinks(True)
        text = self._task_htmlizer.task2html(task)
        label.setText(text)
        return label

    def _findItemByTask(self, task):
        for index in range(self.count()):
            item = self.item(index)
            if item.task == task:
                return item
        return None

    def _findItemByTaskText(self, text):
        for index in range(self.count()):
            item = self.item(index)
            if item.task.text == text:
                return item
        return None

    def updateTask(self, task):
        item = self._findItemByTask(task)
        label = self.itemWidget(item)
        text = self._task_htmlizer.task2html(item.task)
        label.setText(text)

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
            text = self._task_htmlizer.task2html(oldSelected.task)
            label.setText(text)
        self._oldSelected = []
        items = self.selectedItems()
        for item in items:
            self._oldSelected.append(item)
            label = self.itemWidget(item)
            text = self._task_htmlizer.task2html(item.task)
            label.setText(text)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Return:
            items = self.selectedItems()
            if len(items) > 0:
                self._list_itemActivated(items[-1])
        else:
            QtWidgets.QListWidget.keyPressEvent(self, event)
            return


class TaskListWidgetItem(QtWidgets.QListWidgetItem):

    def __init__(self, task, list):
        QtWidgets.QListWidgetItem.__init__(self, '', list)
        self.task = task

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QStackedLayout, QListWidget, QLabel, QListView, QListWidgetItem, QSizePolicy,\
     QAbstractItemView

from qtodotxt.lib import tasklib
from qtodotxt.ui.dialogs.taskeditor_lineedit import TaskEditorLineEdit


class TaskWidget(QWidget):

    taskModified = pyqtSignal(tasklib.Task)
    taskDeleted = pyqtSignal(tasklib.Task)
    taskCreated = pyqtSignal(tasklib.Task)

    def __init__(self, parent, task, new=False):
        QWidget.__init__(self, parent)
        self.task = task
        self.new = new
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout = QStackedLayout(self)

        self.label = QLabel(self)
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self._update()
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.editor = TaskEditorLineEdit(self, parent.mfile)
        self.layout.addWidget(self.editor)
        self.setLayout(self.layout)
        self.layout.setCurrentIndex(0)
        self.editor.editingFinished.connect(self.editFinished)
        self.task.modified.connect(self._update)

    def sizeHint(self):
        return self.label.size()

    def edit(self):
        self.editor.setText(self.task.text)
        self.layout.setCurrentIndex(1)
        self.editor.setFocus()

    def editFinished(self):
        # qt bug, this method may be called several times for one edit
        self.layout.setCurrentIndex(0)
        text = self.editor.text()
        if not text:
            self.taskDeleted.emit(self.task)
        elif self.new:
            self.task.text = text
            self.new = False
            self.taskCreated.emit(self.task)
        elif text != self.task.text:
            self.task.text = text
            self.taskModified.emit(self)
        self.parent().setFocus()

    def _update(self):
        self.label.setText(self.task.toHtml())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.editor.setText(self.task.text)
            self.layout.setCurrentIndex(0)
            self.parent().setFocus()


class TasksListView(QListWidget):

    taskActivated = pyqtSignal(tasklib.Task)
    currentTaskChanged = pyqtSignal(list)
    taskModified = pyqtSignal(tasklib.Task)
    taskCreated = pyqtSignal(tasklib.Task)
    taskDeleted = pyqtSignal(tasklib.Task)

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.mfile = None
        self.setAlternatingRowColors(True)
        self.LayoutMode = QListView.Batched
        self.setResizeMode(QListView.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.activated.connect(self._taskActivated)

    def setFileObject(self, mfile):
        self.mfile = mfile

    def _taskActivated(self, idx):
        self.taskActivated.emit(self.taskFromIndex(idx))

    def taskFromIndex(self, idx):
        it = self.itemFromIndex(idx)
        if it:
            return self.itemWidget(it).task

    def currentChanged(self, current, previous):
        it = self.itemFromIndex(current)
        self.scrollTo(current)  # maybe should be in task controller
        widg = self.itemWidget(it)
        if widg:
            self.currentTaskChanged.emit([widg.task])

    def createTask(self, template_task=None):
        """
        Add a task and start editing it with inline editor
        """
        if isinstance(template_task, tasklib.Task):
            task = tasklib.Task(template_task.text)
        else:
            task = tasklib.Task("")
        idxs = self.selectedIndexes()
        item = self.addTask(task, idxs, new=True)
        self.scrollToItem(item)
        self.itemWidget(item).edit()

    def items(self):
        """
        iterate over all items
        """
        for i in range(self.count()):
            yield self.item(i)

    def tasks(self):
        """
        iterate over all tasks
        """
        for i in range(self.count()):
            yield self.indexWidget(i).task

    def addTask(self, task, idxs=None, new=False):
        """
        add a new task to the view
        """
        item = QListWidgetItem()
        twidget = TaskWidget(self, task, new=new)
        # set items size and add some space between items
        item.setSizeHint(twidget.sizeHint())
        if not idxs:
            self.addItem(item)
        else:
            row = idxs[-1].row()
            row += 1
            self.insertItem(row, item)
        self.setItemWidget(item, twidget)
        twidget.taskModified.connect(self.taskModified.emit)
        twidget.taskDeleted.connect(self._taskDeleted)
        twidget.taskCreated.connect(self.taskCreated.emit)
        return item

    def findItemByTask(self, task):
        for it in self.items():
            if task == self.itemWidget(it).task:
                return it
        return None

    def selectTask(self, task):
        for item in self.items():
            if self.itemWidget(item).task == task:
                self.setCurrentItem(item)
                return

    def selectTaskByText(self, text):
        for item in self.items():
            if self.itemWidget(item).task.text == text:
                self.setCurrentItem(item)
                return

    def removeTask(self, task):
        for item in self.items():
            if self.itemWidget(item).task == task:
                self.takeItem(self.indexFromItem(item).row())
                return

    def _taskDeleted(self, task):
        emit = False
        it = self.findItemByTask(task)
        widg = self.itemWidget(it)
        if not widg:  # can happen due to qt bug mentiooned above
            return
        if not self.itemWidget(it).new:
            emit = True
        self.removeTask(task)
        if emit:
            self.taskDeleted.emit(task)

    def getSelectedTasks(self):
        idxs = self.selectedIndexes()
        return [self.indexWidget(idx).task for idx in idxs]

    def editCurrentTask(self):
        it = self.currentItem()
        if it:
            self.itemWidget(it).edit()

from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QWidget, QStackedLayout, QListWidget, QLabel, QListView, QListWidgetItem,\
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
        self.editor.focusOut.connect(self.editFinished)
        self.task.modified.connect(self._update)

    def sizeHint(self):
        new_height = self.label.heightForWidth(self.parent().size().width())
        new_height += 10
        return QSize(self.parent().size().width(), new_height)

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
            return
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.editFinished()
            return
        QWidget.keyPressEvent(self, event)


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
        self.setLayoutMode(QListView.Batched)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.activated.connect(self._taskActivated)
        self.setUniformItemSizes(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def resizeEvent(self, ev):
        """
        Why do we need to do that???
        """
        for i in range(self.count()):
            item = self.item(i)
            widg = self.itemWidget(item)
            if widg:
                item.setSizeHint(widg.sizeHint())

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

    def currentTask(self):
        it = self.currentItem()
        if it:
            return self.itemWidget(it).task
        return None

    def selectNext(self):
        idx = self.currentIndex()
        row = idx.row() + 1
        print("ROW", row, self.count())
        if row >= self.count():
            print("HERE")
            row = self.count() - 2
        idx = idx.sibling(row, 0)
        self.setCurrentIndex(idx)
        print(self.currentTask())

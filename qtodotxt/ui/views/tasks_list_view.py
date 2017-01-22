from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument, QAbstractTextDocumentLayout, QPalette
from PyQt5.QtWidgets import QListView, QStyledItemDelegate, QStyleOptionViewItem, QApplication, QStyle

from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.lib import tasklib


class TasksListView(QListView):

    taskActivated = pyqtSignal(tasklib.Task)
    currentTaskChanged = pyqtSignal(list)
    taskModified = pyqtSignal(tasklib.Task)
    taskCreated = pyqtSignal(tasklib.Task)

    def __init__(self, parent):
        QListView.__init__(self)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setAlternatingRowColors(True)
        self.LayoutMode = QListView.Batched
        self.setResizeMode(QListView.Adjust)
        self._task_htmlizer = TaskHtmlizer()
        self._delegate = MyDelegate(self)
        self.setItemDelegate(self._delegate)
        self.activated.connect(self._taskActivated)
        self._delegate.taskModified.connect(self.taskModified.emit)
        self._delegate.taskCreated.connect(self.taskCreated.emit)

    def _taskActivated(self, idx):
        it = self.model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        self.taskActivated.emit(task)

    def currentChanged(self, current, previous):
        it = self.model.itemFromIndex(current)
        self.scrollTo(current)  # maybe should be in task controller
        if it:
            task = it.data(Qt.UserRole)
            self.currentTaskChanged.emit([task])

    def setEditor(self, editor_type, editor_args):
        self._delegate.editor = editor_type
        self._delegate.editor_args = editor_args

    def createTask(self, template_task=None):
        if template_task is not None:
            task = tasklib.Task(template_task.text)
        else:
            task = tasklib.Task("")
        task.new = True
        item = QStandardItem()
        item.setData(task, Qt.UserRole)
        item.setData(self._task_htmlizer.task2html(task), Qt.DisplayRole)
        idxs = self.selectedIndexes()
        if not idxs:
            self.model.appendRow(item)
            self.edit(self.model.index(self.model.rowCount()-1, 0))
        else:
            idx = idxs[-1].row()
            self.model.insertRow(idx, item)
            self.edit(self.model.index(idx, 0))

    def addTask(self, task):
        item = QStandardItem()
        item.setData(self._task_htmlizer.task2html(task), Qt.DisplayRole)
        item.setData(task, Qt.UserRole)
        self.model.appendRow(item)

    def addListAction(self, action):
        self.addAction(action)

    def findItemByTask(self, task):
        for idx in range(self.model.rowCount()):
            item = self.model.item(idx)
            listtask = item.data(Qt.UserRole)
            if listtask == task:
                return item
        return None

    def updateTask(self, task):
        item = self.findItemByTask(task)
        html = self._task_htmlizer.task2html(task)
        item.setData(html, Qt.DisplayRole)

    def _selectItem(self, item):
        if item:
            item.setSelected(True)
            self.setCurrentItem(item)

    def selectTask(self, task):
        for idx in range(self.model.rowCount()):
            item = self.model.item(idx)
            listtask = item.data(Qt.UserRole)
            if listtask == task:
                self.setCurrentIndex(self.model.index(idx, 0))

    def selectTaskByText(self, text):
        for idx in range(self.model.rowCount()):
            item = self.model.item(idx)
            task = item.data(Qt.UserRole)
            if task.text == text:
                self.setCurrentIndex(self.model.index(idx, 0))

    def removeTask(self, task):
        for idx in range(self.model.rowCount()):
            item = self.model.item(idx)
            listtask = item.data(Qt.UserRole)
            if listtask == task:
                self.model.removeRow(idx)
                return

    def _list_itemActivated(self, item):
        self.taskActivated.emit(item.task)

    def getSelectedTasks(self):
        idxs = self.selectedIndexes()
        return [self.model.itemFromIndex(idx).data(Qt.UserRole) for idx in idxs]

    def getCurrentItem(self):
        idx = self.currentItem()
        it = self.model.itemFromIndex(idx)
        return it

    def editCurrentTask(self):
        self.edit(self.currentIndex())

    def clear(self):
        self.model.clear()


class MyDelegate(QStyledItemDelegate):

    error = pyqtSignal(Exception)
    taskModified = pyqtSignal(tasklib.Task)
    taskCreated = pyqtSignal(tasklib.Task)

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)
        self.parent = parent
        self.editor = None
        self.editor_args = None
        self._task_htmlizer = TaskHtmlizer()

    def createEditor(self, parent, option, idx):
        editor = self.editor(parent, *self.editor_args)
        return editor

    def setEditorData(self, editor, idx):
        it = self.parent.model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        editor.setText(task.text)

    def setModelData(self, editor, model, idx):
        it = model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        task.parseLine(editor.text())
        it.setData(self._task_htmlizer.task2html(task), Qt.DisplayRole)
        if task.new and editor.text():
            self.taskCreated.emit(task)
            task.new = False
        else:
            self.taskModified.emit(task)

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        style = QApplication.style() if options.widget is None else options.widget.style()

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())

        options.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.State_Selected:
            ctx.palette.setColor(QPalette.Text, options.palette.color(QPalette.Active, QPalette.HighlightedText))
        else:
            ctx.palette.setColor(QPalette.Text, options.palette.color(QPalette.Active, QPalette.Text))

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QSize(doc.idealWidth(), doc.size().height())

    def destroyEditor(self, editor, idx):
        it = self.parent.model.item(idx.row())
        if it:
            task = it.data(Qt.UserRole)
            if not task.text:
                self.parent.model.removeRow(idx.row())
        QStyledItemDelegate.destroyEditor(self, editor, idx)

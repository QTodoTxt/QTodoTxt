from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument, QAbstractTextDocumentLayout
from PyQt5.QtWidgets import QListView, QStyledItemDelegate, QWidget, QStyleOptionViewItem, QApplication, QStyle

from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.lib import tasklib


class TasksListView(QListView):

    taskActivated = pyqtSignal(tasklib.Task)
    currentTaskChanged = pyqtSignal(list)

    def __init__(self, parent):
        QListView.__init__(self)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        #self.setLayoutMode(self.Batched)
        self.setAlternatingRowColors(True)
        self._task_htmlizer = TaskHtmlizer()
        self._delegate = MyDelegate(self)
        self.setItemDelegate(self._delegate)
        self.activated.connect(self._taskActivated)

    def _taskActivated(self, idx):
        it = self.model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        self.taskActivated.emit(task)

    def currentChanged(self, current, previous):
        it = self.model.itemFromIndex(current)
        if it:
            task = it.data(Qt.UserRole)
            self.currentTaskChanged.emit([task])

    def setEditor(self, editor_type, editor_args):
        self._delegate.editor = editor_type
        self._delegate.editor_args = editor_args

    def addTask(self, task):
        print("APPEND", task)
        item = QStandardItem()
        item.setData(self._task_htmlizer.task2html(task), Qt.DisplayRole)
        item.setData(task, Qt.UserRole)
        #label.setWordWrap(True)
        # set minimum width to a reasonable value to get a useful
        # sizeHint _height_ when using word wrap
        #label.setMinimumWidth(self.width() - 20)
        # set items size and add some space between items
        #item.setSizeHint(QSize(label.sizeHint().width(),
                                      #label.sizeHint().height() + 5))
        #self.setItemWidget(item, label)
        self.model.appendRow(item)

    def addListAction(self, action):
        self.addAction(action)

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
            self.removeItemWidget(item)

    def _list_itemActivated(self, item):
        self.taskActivated.emit(item.task)

    def getSelectedTasks(self):
        idxs = self.selectedIndexes()
        return [self.model.itemFromIndex(idx).data(Qt.USerRole) for idx in idxs]

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

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)
        self.parent = parent
        self.editor = None
        self.editor_args = None
        self._task_htmlizer = TaskHtmlizer()

    def createEditor(self, parent, option, idx):
        """
        Called when editing starts, here can we override default editor,
        disable editing for some values, etc...
        """
        print("CREATE EDITOR")
        editor =  self.editor(parent, *self.editor_args)
        print(editor, type(editor), isinstance(editor, QWidget))
        return editor

    def setEditorData(self, editor, idx):
        it = self.parent.model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        editor.setText(task.text)

    def setModelData(self, editor, model, idx):
        print("SET MODEL DATA")
        it = model.itemFromIndex(idx)
        task = it.data(Qt.UserRole)
        task.parseLine(editor.text())
        it.setData(self._task_htmlizer.task2html(task), Qt.DisplayRole)

    def paint(self, painter, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options,index)

        style = QApplication.style() if options.widget is None else options.widget.style()

        doc = QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, options, painter);

        ctx = QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        #if (optionV4.state & QStyle::State_Selected)
            #ctx.palette.setColor(QPalette::Text, optionV4.palette.color(QPalette::Active, QPalette::HighlightedText));

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options,index)

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QSize(doc.idealWidth(), doc.size().height())

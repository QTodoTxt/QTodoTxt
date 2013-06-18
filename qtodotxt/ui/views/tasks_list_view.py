from PySide import QtCore
from PySide import QtGui
from qtodotxt.lib.task_htmlizer import TaskHtmlizer
from qtodotxt.lib import todolib

class TasksListView(QtGui.QWidget):
    
    taskActivated = QtCore.Signal(todolib.Task)
    
    def __init__(self,parent=None):
        super(TasksListView, self).__init__(parent)
        self._task_htmlizer = TaskHtmlizer()        
        self._initUI()
        self._oldSelected = []

    def clear(self):
        self._list.clear()
        
    def clearSelection(self):
        self._list.clearSelection()
        
    def addTask(self, task):
        item = TaskListWidgetItem(task, self._list)
        label = self._createLabel(task)
        self._list.setItemWidget(item, label)

    def addListAction(self, action):
        self._list.addAction(action)
        
    def _initUI(self):
        layout = QtGui.QGridLayout()
        
        self._list = QtGui.QListWidget(self)
        self._list.setSelectionMode(
            QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)
        self._list.itemActivated.connect(self._list_itemActivated)
        self._list.itemSelectionChanged.connect(self._list_itemPressed)
        layout.addWidget(self._list)
        
        self.setLayout(layout)
        
    def _createLabel(self, task):
        label = QtGui.QLabel()
        label.setTextFormat(QtCore.Qt.RichText)
        label.setOpenExternalLinks(True)
        text = self._task_htmlizer.task2html(task)
        label.setText(text)
        return label
    
    def _findItemByTask(self, task):
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item.task == task:
                return item
        return None
    
    def _findItemByTaskText(self, text):
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item.task.text == text:
                return item
        return None
    
    def updateTask(self, task):
        item = self._findItemByTask(task)
        label = self._list.itemWidget(item)
        text = self._task_htmlizer.task2html(item.task)
        label.setText(text)
        
    def _selectItem(self, item):
        if item:
            item.setSelected(True)
            self._list.setCurrentItem(item)
        
    def selectTask(self, task):
        item = self._findItemByTask(task)
        self._selectItem(item)

    def selectTaskByText(self, text):
        item = self._findItemByTaskText(text)
        self._selectItem(item)
    
    def removeTask(self, task):
        item = self._findItemByTask(task)
        if item:
            self._list.removeItemWidget(item)
            self._list.takeItem(self._list.row(item))
    
    def _list_itemActivated(self, item):
        self.taskActivated.emit(item.task)
        
    def getSelectedTasks(self):
        items = self._list.selectedItems()
        return [item.task for item in items]

    def _list_itemPressed(self):
        
        for oldSelected in self._oldSelected:
            label = self._list.itemWidget(oldSelected)
            text = self._task_htmlizer.task2html(oldSelected.task,False)
            label.setText(text)
        self._oldSelected = []
        items = self._list.selectedItems()
        for item in items:
            self._oldSelected.append(item)
            label = self._list.itemWidget(item)
            text = self._task_htmlizer.task2html(item.task,True)
            label.setText(text)
            
class TaskListWidgetItem(QtGui.QListWidgetItem):
    
    def __init__(self, task, list):
        QtGui.QListWidgetItem.__init__(self, '', list)
        self.task = task
        
        
            

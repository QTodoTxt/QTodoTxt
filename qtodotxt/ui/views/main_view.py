from PySide import QtCore
from PySide import QtGui

from ..resource_manager import getIcon
from filters_tree_view import FiltersTreeView
from tasks_list_view import TasksListView

class MainView(QtGui.QMainWindow):
    
    closeEventSignal = QtCore.Signal(QtGui.QCloseEvent)
        
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self._initUI()
        
    def show(self):
        super(MainView, self).show()
    
    def _initUI(self):
        
        splitter = QtGui.QSplitter()
        
        self.filters_tree_view = FiltersTreeView(splitter)
        self.tasks_list_view = TasksListView(splitter)
        
        self.setCentralWidget(splitter)

        self.resize(700, 400)
        splitter.setSizes([200, 500])
        self.setWindowIcon(getIcon('qtodotxt.ico'))
                
    def closeEvent(self, closeEvent):
        super(MainView, self).closeEvent(closeEvent)
        self.closeEventSignal.emit(closeEvent)

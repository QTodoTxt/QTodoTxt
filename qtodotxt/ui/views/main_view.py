from PySide import QtCore
from PySide import QtGui

from qtodotxt.ui.resource_manager import getIcon
from qtodotxt.ui.views.filters_tree_view import FiltersTreeView
from qtodotxt.ui.views.tasks_view import TasksView


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
        self.tasks_view = TasksView(splitter)

        self.setCentralWidget(splitter)

        self.resize(800, 400)
        splitter.setSizes([250, 550])
        self.setWindowIcon(getIcon('qtodotxt.ico'))

    def closeEvent(self, closeEvent):
        super(MainView, self).closeEvent(closeEvent)
        self.closeEventSignal.emit(closeEvent)

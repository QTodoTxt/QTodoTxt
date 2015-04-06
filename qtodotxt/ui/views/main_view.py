from PySide import QtCore
from PySide import QtGui

from qtodotxt.ui.resource_manager import getIcon, getResourcePath
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
        splitter.setHandleWidth(1)

        cssPath = getResourcePath("css/default.css")
        css = open(cssPath,'r', encoding='utf-8').read();
        self.setStyleSheet(css);

        self.filters_tree_view = FiltersTreeView(splitter)
        self.tasks_view = TasksView(splitter)

        self.setCentralWidget(splitter)

        self.resize(800, 400)
        splitter.setSizes([250, 550])
        self.setWindowIcon(getIcon('qtodotxt.ico'))

    def closeEvent(self, closeEvent):
        super(MainView, self).closeEvent(closeEvent)
        self.closeEventSignal.emit(closeEvent)


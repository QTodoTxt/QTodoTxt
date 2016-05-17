from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from qtodotxt.ui.resource_manager import getIcon, getResourcePath
from qtodotxt.ui.views.filters_tree_view import FiltersTreeView
from qtodotxt.ui.views.tasks_view import TasksView


class MainView(QtWidgets.QMainWindow):

    closeEventSignal = QtCore.pyqtSignal(QtGui.QCloseEvent)

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self._initUI()

    def show(self):
        super(MainView, self).show()

    def _initUI(self):

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setHandleWidth(1)

        cssPath = getResourcePath("css/default.css")
        css = open(cssPath, 'r', encoding='utf-8').read()
        self.setStyleSheet(css)

        self.filters_tree_view = FiltersTreeView(self.splitter)
        self.tasks_view = TasksView(self.splitter)

        self.setCentralWidget(self.splitter)

        self.resize(800, 400)
        self.splitter.setSizes([250, 550])
        self.setWindowIcon(getIcon('qtodotxt.png'))

    def closeEvent(self, closeEvent):
        super(MainView, self).closeEvent(closeEvent)
        self.closeEventSignal.emit(closeEvent)

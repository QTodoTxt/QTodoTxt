from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import os

from qtodotxt.ui.resource_manager import getResourcePath
from qtodotxt.ui.views.filters_tree_view import FiltersTreeView
from qtodotxt.ui.views.tasks_view import TasksView


class MainView(QtWidgets.QMainWindow):

    closeEventSignal = QtCore.pyqtSignal(QtGui.QCloseEvent)

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.style = ":/white_icons"
        if str(QtCore.QSettings().value("color_schem", "")).find("dark") >= 0:
            self.style = ":/dark_icons"
        self._initUI()

    def show(self):
        super(MainView, self).show()

    def hide(self):
        super(MainView, self).hide()

    def _initUI(self):

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setHandleWidth(1)

        self.filters_tree_view = FiltersTreeView(self.splitter)
        self.tasks_view = TasksView(self.splitter)

        colorSchemName = QtCore.QSettings().value("color_schem", "")
        tFile = "css/{}.css".format(colorSchemName)
        cssPath = getResourcePath(tFile)
        if os.path.isfile(cssPath):
            css = open(cssPath, 'r', encoding='utf-8').read()
            self.setStyleSheet(css)

        self.setCentralWidget(self.splitter)

        self.resize(800, 400)
        self.splitter.setSizes([250, 550])
        self.setWindowIcon(QtGui.QIcon(self.style + '/resources/qtodotxt.png'))

        self.setTabOrder(self.tasks_view.tasks_search_view, self.tasks_view.tasks_list_view)
        self.setTabOrder(self.tasks_view.tasks_list_view, self.filters_tree_view)

    def closeEvent(self, closeEvent):
        super(MainView, self).closeEvent(closeEvent)
        self.closeEventSignal.emit(closeEvent)

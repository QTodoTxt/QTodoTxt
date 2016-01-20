from PySide import QtGui, QtCore
from qtodotxt.ui.views.tasks_filter_view import TasksFilterView
from qtodotxt.ui.views.tasks_list_view import TasksListView
from qtodotxt.ui.resource_manager import getIcon


class TasksView(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TasksView, self).__init__(parent)
        self._initUI()

    def _initUI(self):
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(10)

        self.tasks_filter = TasksFilterView(getIcon("zoom.png"), getIcon("cross.png"), self)
        self.tasks_list_view = TasksListView(self)
        offset = QtCore.QSettings().value("ui_margin_offset", -4)
        self.setContentsMargins(2 * offset, offset, offset, offset)
        layout.addWidget(self.tasks_filter)
        layout.addWidget(self.tasks_list_view)
        self.setLayout(layout)

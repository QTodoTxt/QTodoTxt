from PySide import QtGui
from qtodotxt.lib.settings import UI_MARGINS_OFFSET
from qtodotxt.ui.views.tasks_filter_view import TasksFilterView
from qtodotxt.ui.views.tasks_list_view import TasksListView
from qtodotxt.ui.resource_manager import getIcon


class TasksView(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TasksView, self).__init__(parent)
        self._initUI()

    def _initUI(self):
        layout = QtGui.QGridLayout(self)
        layout.setSpacing(10)

        self.tasks_filter = TasksFilterView(getIcon("zoom.png"), getIcon("cross.png"), self)
        self.tasks_list_view = TasksListView(self)
        self.setContentsMargins(2 * UI_MARGINS_OFFSET, UI_MARGINS_OFFSET,
                                UI_MARGINS_OFFSET, UI_MARGINS_OFFSET)
        layout.addWidget(self.tasks_filter, 1, 0)
        layout.addWidget(self.tasks_list_view, 2, 0)
        self.setLayout(layout)

from PySide import QtGui
from qtodotxt.ui.views.filter_tasks_view import FilterTasksView
from qtodotxt.ui.views.tasks_list_view import TasksListView
from qtodotxt.ui.resource_manager import getIcon

class TasksView(QtGui.QWidget):

    def __init__(self, parent=None):
        super(TasksView, self).__init__(parent)
        self._initUI()

    def _initUI(self):
        layout = QtGui.QGridLayout(self)
        layout.setSpacing(10)

        self.filter_tasks = FilterTasksView(getIcon("zoom.png"),getIcon("cross.png"),self)
        self.tasks_list_view = TasksListView(self)

        layout.addWidget(self.filter_tasks, 1, 0)
        layout.addWidget(self.tasks_list_view, 2, 0)
        self.setLayout(layout)
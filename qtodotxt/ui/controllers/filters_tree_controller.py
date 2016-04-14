from PyQt5 import QtCore
from qtodotxt.lib.filters import ContextFilter, ProjectFilter, DueTodayFilter, DueTomorrowFilter, DueThisWeekFilter, \
    DueThisMonthFilter, DueOverdueFilter

# class IFiltersTreeView(object):
#    def addFilter(self, filter): pass
#    def clear(self): pass
#    def clearSelection(self): pass
#    def selectFilter(self, filter): pass
#    def getSelectedFilters(self): pass
#    filterSelectionChanged = QtCore.pyqtSignal()
#    def selectAllTasksFilter(self): pass


class FiltersTreeController(QtCore.QObject):

    filterSelectionChanged = QtCore.pyqtSignal(list)

    def __init__(self, view):
        QtCore.QObject.__init__(self)
        self.view = view
        self.view.filterSelectionChanged.connect(self.view_filterSelectionChanged)
        self._is_showing_filters = False

    def view_filterSelectionChanged(self, filters):
        if not self._is_showing_filters:
            self.filterSelectionChanged.emit(filters)

    def showFilters(self, file, show_completed=False):
        self._is_showing_filters = True
        previouslySelectedFilters = self.view.getSelectedFilters()
        self.view.clearSelection()
        self.view.clear()
        self._addAllContexts(file, show_completed)
        self._addAllProjects(file, show_completed)
        self._addAllDueRanges(file, show_completed)
        self._updateCounter(file)
        self._is_showing_filters = False
        self._reselect(previouslySelectedFilters)

    def _updateCounter(self, file):
        rootCounters = file.getTasksCounters()
        self.view.updateTopLevelTitles(rootCounters)

    def _addAllContexts(self, file, show_completed):
        contexts = file.getAllContexts(show_completed)
        for context, number in contexts.items():
            filter = ContextFilter(context)
            self.view.addFilter(filter, number)

    def _addAllProjects(self, file, show_completed):
        projects = file.getAllProjects(show_completed)
        for project, number in projects.items():
            filter = ProjectFilter(project)
            self.view.addFilter(filter, number)

    def _addAllDueRanges(self, file, show_completed):

        dueRanges, rangeSorting = file.getAllDueRanges(show_completed)

        for range, number in dueRanges.items():
            if range == 'Today':
                filter = DueTodayFilter(range)
                sortKey = rangeSorting['Today']
            elif range == 'Tomorrow':
                filter = DueTomorrowFilter(range)
                sortKey = rangeSorting['Tomorrow']
            elif range == 'This week':
                filter = DueThisWeekFilter(range)
                sortKey = rangeSorting['This week']
            elif range == 'This month':
                filter = DueThisMonthFilter(range)
                sortKey = rangeSorting['This month']
            elif range == 'Overdue':
                filter = DueOverdueFilter(range)
                sortKey = rangeSorting['Overdue']

            self.view.addDueRangeFilter(filter, number, sortKey)

    def _reselect(self, previouslySelectedFilters):
        for filter in previouslySelectedFilters:
            self.view.selectFilter(filter)
        if not self.view.getSelectedFilters():
            self.view.selectAllTasksFilter()

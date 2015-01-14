from PySide import QtCore
from qtodotxt.lib.filters import ContextFilter, ProjectFilter, DueFilter, DueTodayFilter, DueTomorrowFilter, DueThisWeekFilter, DueThisMonthFilter, DueOverdueFilter

# class IFiltersTreeView(object):
#    def addFilter(self, filter): pass
#    def clear(self): pass
#    def clearSelection(self): pass
#    def selectFilter(self, filter): pass
#    def getSelectedFilters(self): pass
#    filterSelectionChanged = QtCore.Signal()
#    def selectAllTasksFilter(self): pass    


class FiltersTreeController(QtCore.QObject):
    
    filterSelectionChanged = QtCore.Signal(list)
    
    def __init__(self, view):
        QtCore.QObject.__init__(self)
        self._view = view
        self._view.filterSelectionChanged.connect(self._view_filterSelectionChanged)
        self._is_showing_filters = False
        
    def _view_filterSelectionChanged(self, filters):
        if not self._is_showing_filters:
            self.filterSelectionChanged.emit(filters)
        
    def showFilters(self, file):
        self._is_showing_filters = True
        previouslySelectedFilters = self._view.getSelectedFilters()
        self._view.clearSelection()
        self._view.clear()
        self._addAllContexts(file)
        self._addAllProjects(file)
        self._addAllDueRanges(file)
        self._updateCounter(file)
        self._is_showing_filters = False
        self._reselect(previouslySelectedFilters)

    def _updateCounter(self, file):
        rootCounters = file.getTasksCounters()
        self._view.updateTopLevelTitles(rootCounters)

    def _addAllContexts(self, file):
        contexts = file.getAllContexts()
        for context, number in contexts.items():
            filter = ContextFilter(context)
            self._view.addFilter(filter, number)

    def _addAllProjects(self, file):
        projects = file.getAllProjects()
        for project, number in projects.items():
            filter = ProjectFilter(project)
            self._view.addFilter(filter, number)

    def _addAllDueRanges(self, file):

        dueRanges = file.getAllDueRanges()

        for range, number in dueRanges.items():
            if range == 'Today':
                filter = DueTodayFilter(range)
            elif range == 'Tomorrow':
                filter = DueTomorrowFilter(range)
            elif range == 'This week':
                filter = DueThisWeekFilter(range)
            elif range == 'This month':
                filter = DueThisMonthFilter(range)
            elif range == 'Overdue':
                filter = DueOverdueFilter(range)

            self._view.addDueRangeFilter(filter, number)
        
    def _reselect(self, previouslySelectedFilters):
        for filter in previouslySelectedFilters:
            self._view.selectFilter(filter)
        if not self._view.getSelectedFilters():
            self._view.selectAllTasksFilter()

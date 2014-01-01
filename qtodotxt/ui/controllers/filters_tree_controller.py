from PySide import QtCore
from qtodotxt.lib.filters import ContextFilter, ProjectFilter

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
        self._updateCounter(file)
        self._is_showing_filters = False
        self._reselect(previouslySelectedFilters)

    def _updateCounter(self, file):
        rootCounters = file.getTasksCounters()
        self._view.updateTopLevelTitles(rootCounters)
        

    def _addAllContexts(self, file):
        contexts = file.getAllContexts()
        for context, number in contexts.iteritems():
            filter = ContextFilter(context)
            self._view.addFilter(filter, number)

    def _addAllProjects(self, file):
        projects = file.getAllProjects()
        for project, number in projects.iteritems():
            filter = ProjectFilter(project)
            self._view.addFilter(filter, number)
        
    def _reselect(self, previouslySelectedFilters):
        for filter in previouslySelectedFilters:
            self._view.selectFilter(filter)
        if not self._view.getSelectedFilters():
            self._view.selectAllTasksFilter()
        

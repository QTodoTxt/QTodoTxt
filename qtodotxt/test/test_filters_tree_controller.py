import unittest
from PySide import QtCore

from qtodotxt.lib import todolib
from qtodotxt.lib.filters import IncompleteTasksFilter, ContextFilter, ProjectFilter
from qtodotxt.ui.controllers import FiltersTreeController

class FakeTreeView(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.filters = []
        self.selectedFilters = []
        
    def addFilter(self, filter, number=0):
        filter.text = "%s (%d)" % (filter.text, number)
        self.filters.append(filter)
        
    def clear(self):
        self.filters = []
        
    def clearSelection(self):
        self.selectedFilters = []
        
    def selectFilter(self, filter):
        if filter not in self.selectedFilters:
            self.selectedFilters.append(filter)
            
    def getSelectedFilters(self):
        return self.selectedFilters
    
    filterSelectionChanged = QtCore.Signal()
    
    def selectAllTasksFilter(self):
        self.selectedFilters = [IncompleteTasksFilter()]
        
    def updateTopLevelTitles(self, counters):
        return
        
        
class Test(unittest.TestCase):
    
    def _createMockFile(self):
        file = todolib.File()
        file.tasks.append(todolib.Task('my task1 @context1'))
        file.tasks.append(todolib.Task('my task2 @context1 @context2'))
        file.tasks.append(todolib.Task('my task3 +project1 @context2'))
        return file
        
    def test_showFilters(self):
        # arrange
        view = FakeTreeView()
        controller = FiltersTreeController(view)
        file = self._createMockFile()
        
        # act
        controller.showFilters(file)
        
        sortedFilter = sorted(view.filters, key=lambda filter: filter.text)
        
        # assert
        self.assertEqual(1, len(view.selectedFilters),
            'There should be only 1 selected filter (actual: %s)' % view.selectedFilters)
        self.assertIsInstance(view.selectedFilters[0], IncompleteTasksFilter,
            'selected filter #1 should be instance of IncompleteTasksFilter (actual: %s)' % view.selectedFilters[0])
        
        self.assertEqual(3, len(view.filters),
            'There should be 3 filters (actual: %d)' % len(view.filters))
        filter = sortedFilter[0]
        self.assertIsInstance(filter, ContextFilter,
            'Filter #1 should be instance of ContextFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'context1 (2)',
            'Filter #1 text should be "context1" (actual: "%s")' % filter.text)

        filter = sortedFilter[1]
        self.assertIsInstance(filter, ContextFilter,
            'Filter #2 should be instance of ContextFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'context2 (2)',
            'Filter #2 text should be "%s" (actual: context2)' % filter.text)
        
        filter = sortedFilter[2]
        self.assertIsInstance(filter, ProjectFilter,
            'Filter #2 should be instance of ProjectFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'project1 (1)',
            'Filter #2 text should be "%s" (actual: project1)' % filter.text)
        
    def test_showFilters_afterAddingNewContext(self):
        # arrange
        view = FakeTreeView()
        controller = FiltersTreeController(view)
        file = self._createMockFile()
        controller.showFilters(file)
        original_filter0 = view.filters[0]
        view.clearSelection()
        view.selectFilter(view.filters[0])
        file.tasks[2].text += " @context3"
        
        # act
        controller.showFilters(file)
        
        # assert
        self.assertNotEqual(view.filters[0], original_filter0,
            'A new filter was not created (expected: %s, actual: %s)' % 
                (view.filters[0], original_filter0))

        # self.assertNotEqual(view.selectedFilters[0], original_filter0, 
        #    'The old selected filter is still selected (expected: %s, actual: %s)' % 
        #        (view.selectedFilters[0], original_filter0))
        
        self.assertEquals(
            4, len(view.filters),
            'There should be 4 filters (actual: %s)' % view.selectedFilters)

        sortedFilter = sorted(view.filters, key=lambda filter: filter.text)

        filter1_text = sortedFilter[0].text
        self.assertEqual("context1 (2)", filter1_text,
            'Filter #1 context should be "context1 (2)" (actual: "%s")' % filter1_text)

        self.assertEquals(
            1, len(view.selectedFilters),
            'There should be 1 selected filters (actual: %s)' % view.selectedFilters)
        
        expectedSelectedFilters = [sortedFilter[1]]
        self.assertSequenceEqual(
            expectedSelectedFilters,
            view.selectedFilters,
            'Wrong selected filters (expected: %s, actual: %s)' % 
                (str(expectedSelectedFilters), view.selectedFilters))
        
        

import unittest
from PyQt5 import QtCore
from datetime import date

from qtodotxt.lib import tasklib
from qtodotxt.lib.file import File
from qtodotxt.lib.filters import IncompleteTasksFilter, ContextFilter, ProjectFilter, DueThisMonthFilter, \
    DueThisWeekFilter, DueTodayFilter
from qtodotxt.ui.controllers.filters_tree_controller import FiltersTreeController


class FakeTreeView(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.filters = []
        self.selectedFilters = []

    def addFilter(self, filter, number=0):
        filter.text = "%s (%d)" % (filter.text, number)
        self.filters.append(filter)

    def addDueRangeFilter(self, filter, number=0, sortKey=0):
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

    filterSelectionChanged = QtCore.pyqtSignal()

    def selectAllTasksFilter(self):
        self.selectedFilters = [IncompleteTasksFilter()]

    def updateTopLevelTitles(self, counters):
        return


class Test(unittest.TestCase):

    def _createMockFile(self):
        today = today = date.today().strftime('%Y-%m-%d')
        file = File()
        file.tasks.append(tasklib.Task('my task1 @context1'))
        file.tasks.append(tasklib.Task('my task2 @context1 @context2'))
        file.tasks.append(tasklib.Task('due:' + today + ' my task3 +project1 @context2'))
        file.tasks.append(tasklib.Task('due:' + today + ' my task4'))
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
                              'selected filter #1 should be instance of IncompleteTasksFilter (actual: %s)'
                              % view.selectedFilters[0])

        self.assertEqual(6, len(view.filters), 'There should be 6 filters (actual: %d)' % len(view.filters))

        filter = sortedFilter[0]
        self.assertIsInstance(filter, DueThisMonthFilter,
                              'Filter #1 should be instance of DueThisMonthFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'This month (2)',
                         'Filter #1 text should be "This month" (actual: "%s")' % filter.text)

        filter = sortedFilter[1]
        self.assertIsInstance(filter, DueThisWeekFilter,
                              'Filter #2 should be instance of DueThisWeekFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'This week (2)',
                         'Filter #2 text should be "This week" (actual: "%s")' % filter.text)

        filter = sortedFilter[2]
        self.assertIsInstance(filter, DueTodayFilter,
                              'Filter #3 should be instance of DueTodayFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'Today (2)',
                         'Filter #3 text should be "Today" (actual: "%s")' % filter.text)

        filter = sortedFilter[3]
        self.assertIsInstance(filter, ContextFilter,
                              'Filter #4 should be instance of ContextFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'context1 (2)',
                         'Filter #4 text should be "context1" (actual: "%s")' % filter.text)

        filter = sortedFilter[4]
        self.assertIsInstance(filter, ContextFilter,
                              'Filter #5 should be instance of ContextFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'context2 (2)',
                         'Filter #5 text should be "%s" (actual: context2)' % filter.text)

        filter = sortedFilter[5]
        self.assertIsInstance(filter, ProjectFilter,
                              'Filter #6 should be instance of ProjectFilter (actual: %s)' % str(type(filter)))
        self.assertEqual(filter.text, 'project1 (1)',
                         'Filter #6 text should be "%s" (actual: project1)' % filter.text)

    def test_showFilters_afterAddingNewContext(self):
        # arrange
        view = FakeTreeView()
        controller = FiltersTreeController(view)
        file = self._createMockFile()
        controller.showFilters(file)
        original_filter0 = view.filters[0]
        view.clearSelection()
        view.selectFilter(view.filters[0])
        file.tasks[2] = tasklib.Task(file.tasks[2].text + " @context3")

        # act
        controller.showFilters(file)

        # assert
        self.assertEquals(
            7,
            len(view.filters),
            'There should be 7 filters (actual: %s)' % view.selectedFilters)

        sortedFilter = sorted(view.filters, key=lambda filter: filter.text)
        print(sortedFilter)

        self.assertEquals(
            1, len(view.selectedFilters),
            'There should be 1 selected filters (actual: %s)' % view.selectedFilters)

        # Due filters are not sorted
        filter1_text = sortedFilter[3].text
        self.assertEqual("context1 (2)", filter1_text,
                         'Filter #1 context should be "context1 (2)" (actual: "%s")' % filter1_text)

        expectedselectedfilter = original_filter0.text
        self.assertSequenceEqual(
            expectedselectedfilter,
            view.selectedFilters[0].text,
            'Wrong selected filters (expected: %s, actual: %s)' %
            (expectedselectedfilter, view.selectedFilters))

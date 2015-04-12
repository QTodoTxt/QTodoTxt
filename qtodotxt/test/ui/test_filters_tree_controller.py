from datetime import date
from PySide import QtCore
import unittest

from qtodotxt.lib.task import Task
from qtodotxt.lib.file import File
from qtodotxt.lib.filters import IncompleteTasksFilter, IncompleteTasksWithContextsFilter, \
    IncompleteTasksWithProjectsFilter, DueThisMonthFilter, DueThisWeekFilter, DueTodayFilter
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

    filterSelectionChanged = QtCore.Signal()

    def selectAllTasksFilter(self):
        self.selectedFilters = [IncompleteTasksFilter()]

    def updateTopLevelTitles(self, counters):
        return


class Test(unittest.TestCase):

    def _createMockFile(self):
        today = today = date.today().strftime('%Y-%m-%d')
        file = File()
        file.tasks.append(Task('my task1 @context1'))
        file.tasks.append(Task('my task2 @context1 @context2'))
        file.tasks.append(Task('due:' + today + ' my task3 +project1 @context2'))
        file.tasks.append(Task('due:' + today + ' my task4'))
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
        self.assertEqual(1, len(view.selectedFilters))
        self.assertIsInstance(view.selectedFilters[0], IncompleteTasksFilter)

        self.assertEqual(6, len(view.filters))
        filter = sortedFilter[0]
        self.assertIsInstance(filter, DueThisMonthFilter)
        self.assertEqual(filter.text, 'This month (2)')

        filter = sortedFilter[1]
        self.assertIsInstance(filter, DueThisWeekFilter)
        self.assertEqual(filter.text, 'This week (2)')

        filter = sortedFilter[2]
        self.assertIsInstance(filter, DueTodayFilter)
        self.assertEqual(filter.text, 'Today (2)')

        filter = sortedFilter[3]
        self.assertIsInstance(filter, IncompleteTasksWithContextsFilter)
        self.assertEqual(filter.text, 'context1 (2)')

        filter = sortedFilter[4]
        self.assertIsInstance(filter, IncompleteTasksWithContextsFilter)
        self.assertEqual(filter.text, 'context2 (2)')

        filter = sortedFilter[5]
        self.assertIsInstance(filter, IncompleteTasksWithProjectsFilter)
        self.assertEqual(filter.text, 'project1 (1)')

    def test_showFilters_afterAddingNewContext(self):
        # arrange
        view = FakeTreeView()
        controller = FiltersTreeController(view)
        file = self._createMockFile()
        controller.showFilters(file)
        original_filter0 = view.filters[0]
        view.clearSelection()
        view.selectFilter(view.filters[0])
        file.tasks[2] += "@context3"

        # act
        controller.showFilters(file)

        # assert
        self.assertEquals(7, len(view.filters))

        sortedFilter = sorted(view.filters, key=lambda filter: filter.text)
        print(sortedFilter)

        self.assertEquals(1, len(view.selectedFilters))

        # Due filters are not sorted
        filter1_text = sortedFilter[3].text
        self.assertEqual("context1 (2)", filter1_text)

        expectedselectedfilter = original_filter0.text
        self.assertSequenceEqual(expectedselectedfilter, view.selectedFilters[0].text)

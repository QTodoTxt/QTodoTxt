from PySide import QtCore
from PySide import QtGui
from qtodotxt.lib.filters import *  #FIXME
from qtodotxt.lib.settings import UI_MARGINS_OFFSET
from qtodotxt.ui.resource_manager import getIcon


class FiltersTreeView(QtGui.QWidget):

    filterSelectionChanged = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(FiltersTreeView, self).__init__(parent)
        self._filterItemByFilterType = dict()
        self._filterIconByFilterType = dict()
        self._treeItemByFilterType = dict()
        self._initUI()

    def getSelectedFilters(self):
        items = self._tree.selectedItems()
        filters = [item.filter for item in items]
        return filters

    def clear(self):
        self._tree.clear()
        self._addDefaultTreeItems(self._tree)
        self._initFilterTypeMappings()

    def clearSelection(self):
        self._tree.clearSelection()

    def addFilter(self, filter, number=0):
        parentItem = self._filterItemByFilterType[type(filter)]
        icon = self._filterIconByFilterType[type(filter)]
        FilterTreeWidgetItem(parentItem, ["%s (%d)" % (filter.text, number)], filter=filter, icon=icon)
        parentItem.setExpanded(True)
        parentItem.sortChildren(0, QtCore.Qt.AscendingOrder)

    # Predefined sorting for due ranges
    def addDueRangeFilter(self, filter, number=0, sortKey=0):
        parentItem = self._dueItem
        icon = self._filterIconByFilterType[type(filter)]
        FilterTreeWidgetItem(parentItem, ["%s (%d)" % (filter.text, number)], filter=filter, icon=icon, order=sortKey)
        parentItem.setExpanded(True)
        parentItem.sortChildren(1, QtCore.Qt.AscendingOrder)

    def updateTopLevelTitles(self, counters):
        nbPending = counters['Pending']
        nbDue = counters['Due']
        nbUncategorized = counters['Uncategorized']
        nbContexts = counters['Contexts']
        nbProjects = counters['Projects']
        nbComplete = counters['Complete']
        self._incompleteTasksItem.setText(0, "Pending (%d)" % nbPending)
        self._dueItem.setText(0, "Due (%d)" % nbDue)
        self._uncategorizedTasksItem.setText(0, "Uncategorized (%d)" % nbUncategorized)
        self._contextsItem.setText(0, "Contexts (%d)" % nbContexts)
        self._projectsItem.setText(0, "Projects (%d)" % nbProjects)
        self._completeTasksItem.setText(0, "Complete (%d)" % nbComplete)

    def selectAllTasksFilter(self):
        self._incompleteTasksItem.setSelected(True)

    def _selectItem(self, item):
        if item:
            item.setSelected(True)
            self._tree.setCurrentItem(item)

    def _selectContext(self, context):
        item = self._findItem(context, self._contextsItem)
        self._selectItem(item)

    def _selectProject(self, project):
        item = self._findItem(project, self._projectsItem)
        self._selectItem(item)

    def _selectDueRange(self, due):
        item = self._findItem(due, self._dueItem)
        self._selectItem(item)

    def _findItem(self, text, parentItem):
        for index in range(parentItem.childCount()):
            child = parentItem.child(index)
            #Remove counter on the tree: context (3) for example
            childText = child.text(0).rpartition(' ')[0]
            if childText == text:
                return child
        return None

    def _initUI(self):
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        self.setContentsMargins(UI_MARGINS_OFFSET, UI_MARGINS_OFFSET,
                                2*UI_MARGINS_OFFSET, UI_MARGINS_OFFSET)
        self._tree = self._createTreeWidget()
        layout.addWidget(self._tree)

    def _createTreeWidget(self):
        tree = QtGui.QTreeWidget()
        tree.header().hide()
        tree.setSelectionMode(
            QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)
        tree.itemSelectionChanged.connect(self._tree_itemSelectionChanged)
        self._addDefaultTreeItems(tree)
        self._initFilterTypeMappings()
        return tree

    def _addDefaultTreeItems(self, tree):
        self._incompleteTasksItem = \
            FilterTreeWidgetItem(None, ['Pending'], IncompleteTasksFilter(), getIcon('time.png'))
        self._dueItem = \
            FilterTreeWidgetItem(None, ['Due'], HasDueDateFilter(), getIcon('due.png'))
        self._uncategorizedTasksItem = \
            FilterTreeWidgetItem(None, ['Uncategorized'], UncategorizedTasksFilter(), getIcon('help.png'))
        self._contextsItem = \
            FilterTreeWidgetItem(None, ['Contexts'], HasContextsFilter(), getIcon('at.png'))
        self._projectsItem = \
            FilterTreeWidgetItem(None, ['Projects'], HasProjectsFilter(), getIcon('plus.png'))
        self._completeTasksItem = \
            FilterTreeWidgetItem(None, ['Complete'], CompleteTasksFilter(), getIcon('x.png'))
        tree.addTopLevelItems([
            self._incompleteTasksItem,
            self._uncategorizedTasksItem,
            self._dueItem,
            self._contextsItem,
            self._projectsItem,
            self._completeTasksItem])

    def _initFilterTypeMappings(self):
        self._filterItemByFilterType[ContextFilter] = self._contextsItem
        self._filterItemByFilterType[ProjectFilter] = self._projectsItem
        self._filterItemByFilterType[DueFilter] = self._dueItem

        self._filterIconByFilterType[ContextFilter] = getIcon('at.png')
        self._filterIconByFilterType[ProjectFilter] = getIcon('plus.png')

        self._filterIconByFilterType[DueTodayFilter] = getIcon('due_today.png')
        self._filterIconByFilterType[DueTomorrowFilter] = getIcon('due_tomorrow.png')
        self._filterIconByFilterType[DueThisWeekFilter] = getIcon('due.png')
        self._filterIconByFilterType[DueThisMonthFilter] = getIcon('due_this_month.png')
        self._filterIconByFilterType[DueOverdueFilter] = getIcon('due_overdue.png')

        self._treeItemByFilterType[IncompleteTasksFilter] = self._incompleteTasksItem
        self._treeItemByFilterType[UncategorizedTasksFilter] = self._uncategorizedTasksItem
        self._treeItemByFilterType[CompleteTasksFilter] = self._completeTasksItem
        self._treeItemByFilterType[HasProjectsFilter] = self._projectsItem
        self._treeItemByFilterType[HasDueDateFilter] = self._dueItem
        self._treeItemByFilterType[HasContextsFilter] = self._contextsItem

    def _tree_itemSelectionChanged(self):
        self.filterSelectionChanged.emit(self.getSelectedFilters())

    def selectFilter(self, filter):
        if isinstance(filter, ContextFilter):
            self._selectContext(filter.text)
        elif isinstance(filter, ProjectFilter):
            self._selectProject(filter.text)
        elif isinstance(filter, DueFilter):
            self._selectDueRange(filter.text)
        elif isinstance(filter, DueTodayFilter):
            self._selectDueRange(filter.text)
        elif isinstance(filter, DueTomorrowFilter):
            self._selectDueRange(filter.text)
        elif isinstance(filter, DueThisWeekFilter):
            self._selectDueRange(filter.text)
        elif isinstance(filter, DueThisMonthFilter):
            self._selectDueRange(filter.text)
        elif isinstance(filter, DueOverdueFilter):
            self._selectDueRange(filter.text)
        else:
            item = self._treeItemByFilterType[type(filter)]
            self._selectItem(item)


class FilterTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, strings, filter=None, icon=None, order=None):
        QtGui.QTreeWidgetItem.__init__(self, parent, strings)
        self.filter = filter
        if order:
            self.setText(1,str(order))
        if icon:
            self.setIcon(0, icon)

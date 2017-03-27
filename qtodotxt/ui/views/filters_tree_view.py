from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from qtodotxt.lib.filters import ContextFilter, CompleteTasksFilter, DueFilter, DueOverdueFilter, DueThisMonthFilter, \
    DueThisWeekFilter, DueTodayFilter, DueTomorrowFilter, HasContextsFilter, HasDueDateFilter, HasProjectsFilter, \
    ProjectFilter, UncategorizedTasksFilter, AllTasksFilter, PriorityFilter, HasPriorityFilter


class FiltersTreeView(QtWidgets.QWidget):

    filterSelectionChanged = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(FiltersTreeView, self).__init__(parent)
        self.style = ":/white_icons"
        if str(QtCore.QSettings().value("color_schem", "")).find("dark") >= 0:
            self.style = ":/dark_icons"
        self._filterItemByFilterType = dict()
        self._filterIconByFilterType = dict()
        self._treeItemByFilterType = dict()
        self._initUI()

    def getSelectedFilters(self):
        items = self._tree.selectedItems()
        filters = [item.filter for item in items]
        return filters

    def getSelectedFilterNames(self):
        return [f.text for f in self.getSelectedFilters()]

    def setSelectedFiltersByNames(self, names):
        # FIXME: seems selecting an item deselect previous item....
        # we could also support reselecting dynamic filters....
        if not isinstance(names, (list, tuple)):
            names = [names]
        for name in names:
            if name == "All":
                self.selectAllTasksFilter()
            elif name == "Incomplete":
                self.selectIncompleteTasksFilter()
            elif name == "Complete":
                self._completeTasksItem.setSelected(True)
            elif name == "Uncategorized":
                self._uncategorizedTasksItem.setSelected(True)

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

    def updateTopLevelTitles(self, counters, show_completed=False):
        nbPending = counters['Pending']
        nbDue = counters['Due']
        nbUncategorized = counters['Uncategorized']
        nbContexts = counters['Contexts']
        nbProjects = counters['Projects']
        nbComplete = counters['Complete']
        nbContCompl = counters['ContCompl']
        nbProjCompl = counters['ProjCompl']
        nbDueCompl = counters['DueCompl']
        nbUncatCompl = counters['UncatCompl']
        nbPriority = counters['Priority']
        nbPrioCompl = counters['PrioCompl']

        self._completeTasksItem.setText(0, "Complete (%d)" % nbComplete)
        if (show_completed is True):
            self._allTasksItem.setText(0, "All ({0}; {1})".format(nbPending, nbComplete))
            self._dueItem.setText(0, "Due ({0}; {1})".format(nbDue, nbDueCompl))
            self._contextsItem.setText(0, "Contexts ({0}; {1})".format(nbContexts, nbContCompl))
            self._projectsItem.setText(0, "Projects ({0}; {1})".format(nbProjects, nbProjCompl))
            self._priorityItem.setText(0, "Priority ({0}; {1})".format(nbPriority, nbPrioCompl))
            self._uncategorizedTasksItem.setText(0, "Uncategorized ({0}; {1})".format(nbUncategorized, nbUncatCompl))
        else:
            self._allTasksItem.setText(0, "All (%d)" % nbPending)
            self._contextsItem.setText(0, "Contexts (%d)" % nbContexts)
            self._projectsItem.setText(0, "Projects (%d)" % nbProjects)
            self._dueItem.setText(0, "Due (%d)" % nbDue)
            self._priorityItem.setText(0, "Priority (%d)" % nbPriority)
            self._uncategorizedTasksItem.setText(0, "Uncategorized (%d)" % nbUncategorized)

    def selectAllTasksFilter(self):
        self._allTasksItem.setSelected(True)

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

    def _selectPriority(self, priority):
        item = self._findItem(priority, self._priorityItem)
        self._selectItem(item)

    def _findItem(self, text, parentItem):
        for index in range(parentItem.childCount()):
            child = parentItem.child(index)
            # Remove counter on the tree: context (3) for example
            childText = child.text(0).rpartition(' ')[0]
            if childText == text:
                return child
        return None

    def _initUI(self):
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        offset = QtCore.QSettings().value("ui_margin_offset", -4)
        self.setContentsMargins(offset, offset, 2 * offset, offset)
        self._tree = self._createTreeWidget()
        layout.addWidget(self._tree)

    def _createTreeWidget(self):
        tree = QtWidgets.QTreeWidget()
        tree.header().hide()
        tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        tree.itemSelectionChanged.connect(self._tree_itemSelectionChanged)
        self._addDefaultTreeItems(tree)
        self._initFilterTypeMappings()
        return tree

    def _addDefaultTreeItems(self, tree):
        self._allTasksItem = FilterTreeWidgetItem(None, ['All'],
                                                  AllTasksFilter(),
                                                  QtGui.QIcon(self.style + '/resources/FilterAll.png'))
        self._dueItem = FilterTreeWidgetItem(None, ['Due'],
                                             HasDueDateFilter(), QtGui.QIcon(self.style + '/resources/FilterDue.png'))
        self._uncategorizedTasksItem = FilterTreeWidgetItem(
            None, ['Uncategorized'],
            UncategorizedTasksFilter(), QtGui.QIcon(self.style + '/resources/FilterUncategorized.png'))
        self._contextsItem = FilterTreeWidgetItem(None, ['Contexts'],
                                                  HasContextsFilter(),
                                                  QtGui.QIcon(self.style + '/resources/FilterContexts.png'))
        self._projectsItem = FilterTreeWidgetItem(None, ['Projects'],
                                                  HasProjectsFilter(),
                                                  QtGui.QIcon(self.style + '/resources/FilterProjects.png'))
        self._priorityItem = FilterTreeWidgetItem(None, ['Priorities'],
                                                  HasPriorityFilter(),
                                                  QtGui.QIcon(self.style + '/resources/FilterComplete.png'))
        self._completeTasksItem = FilterTreeWidgetItem(None, ['Complete'],
                                                       CompleteTasksFilter(),
                                                       QtGui.QIcon(self.style + '/resources/FilterComplete.png'))
        tree.addTopLevelItems([
            self._allTasksItem, self._uncategorizedTasksItem, self._dueItem, self._contextsItem, self._projectsItem,
            self._priorityItem, self._completeTasksItem
        ])

    def _initFilterTypeMappings(self):
        self._filterItemByFilterType[ContextFilter] = self._contextsItem
        self._filterItemByFilterType[ProjectFilter] = self._projectsItem
        self._filterItemByFilterType[DueFilter] = self._dueItem
        self._filterItemByFilterType[PriorityFilter] = self._priorityItem

        self._filterIconByFilterType[ContextFilter] = QtGui.QIcon(self.style + '/resources/FilterContexts.png')
        self._filterIconByFilterType[ProjectFilter] = QtGui.QIcon(self.style + '/resources/FilterProjects.png')

        self._filterIconByFilterType[DueTodayFilter] = QtGui.QIcon(self.style + '/resources/FilterDueToday.png')
        self._filterIconByFilterType[DueTomorrowFilter] = QtGui.QIcon(self.style + '/resources/FilterDueTomorrow.png')
        self._filterIconByFilterType[DueThisWeekFilter] = QtGui.QIcon(self.style + '/resources/FilterDueWeek.png')
        self._filterIconByFilterType[DueThisMonthFilter] = QtGui.QIcon(self.style + '/resources/FilterDueMonth.png')
        self._filterIconByFilterType[DueOverdueFilter] = QtGui.QIcon(self.style + '/resources/FilterDueOverdue.png')
        self._filterIconByFilterType[PriorityFilter] = QtGui.QIcon(self.style + '/resources/FilterComplete.png')

        self._treeItemByFilterType[AllTasksFilter] = self._allTasksItem
        self._treeItemByFilterType[UncategorizedTasksFilter] = self._uncategorizedTasksItem
        self._treeItemByFilterType[CompleteTasksFilter] = self._completeTasksItem
        self._treeItemByFilterType[HasProjectsFilter] = self._projectsItem
        self._treeItemByFilterType[HasDueDateFilter] = self._dueItem
        self._treeItemByFilterType[HasContextsFilter] = self._contextsItem
        self._treeItemByFilterType[HasPriorityFilter] = self._priorityItem

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
        elif isinstance(filter, PriorityFilter):
            self._selectPriority(filter.text)
        else:
            item = self._treeItemByFilterType[type(filter)]
            self._selectItem(item)


class FilterTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, strings, filter=None, icon=None, order=None):
        QtWidgets.QTreeWidgetItem.__init__(self, parent, strings)
        self.filter = filter
        if order:
            self.setText(1, str(order))
        if icon:
            self.setIcon(0, icon)

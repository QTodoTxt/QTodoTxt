from PyQt5 import QtCore
from PyQt5 import QtWidgets
from qtodotxt.lib.filters import ContextFilter, CompleteTasksFilter, DueFilter, DueOverdueFilter, DueThisMonthFilter, \
    DueThisWeekFilter, DueTodayFilter, DueTomorrowFilter, HasContextsFilter, HasDueDateFilter, HasProjectsFilter, \
    ProjectFilter, UncategorizedTasksFilter, AllTasksFilter
from qtodotxt.ui.resource_manager import getIcon


class FiltersTreeView(QtWidgets.QWidget):

    filterSelectionChanged = QtCore.pyqtSignal(list)

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

    def updateTopLevelTitles(self, counters):
        nbPending = counters['Pending']
        nbDue = counters['Due']
        nbUncategorized = counters['Uncategorized']
        nbContexts = counters['Contexts']
        nbProjects = counters['Projects']
        nbComplete = counters['Complete']
        self._allTasksItem.setText(0, "All (%d)" % nbPending)
        self._dueItem.setText(0, "Due (%d)" % nbDue)
        self._uncategorizedTasksItem.setText(0, "Uncategorized (%d)" % nbUncategorized)
        self._contextsItem.setText(0, "Contexts (%d)" % nbContexts)
        self._projectsItem.setText(0, "Projects (%d)" % nbProjects)
        self._completeTasksItem.setText(0, "Complete (%d)" % nbComplete)

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
        self.setContentsMargins(offset, offset,
                                2 * offset, offset)
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
        self._allTasksItem = FilterTreeWidgetItem(None,
                                                  ['All'],
                                                  AllTasksFilter(),
                                                  getIcon('FilterAll.png'))
        self._dueItem = FilterTreeWidgetItem(None,
                                             ['Due'],
                                             HasDueDateFilter(),
                                             getIcon('FilterDue.png'))
        self._uncategorizedTasksItem = FilterTreeWidgetItem(None,
                                                            ['Uncategorized'],
                                                            UncategorizedTasksFilter(),
                                                            getIcon('FilterUncategorized.png'))
        self._contextsItem = FilterTreeWidgetItem(None,
                                                  ['Contexts'],
                                                  HasContextsFilter(),
                                                  getIcon('FilterContexts.png'))
        self._projectsItem = FilterTreeWidgetItem(None,
                                                  ['Projects'],
                                                  HasProjectsFilter(),
                                                  getIcon('FilterProjects.png'))
        self._completeTasksItem = FilterTreeWidgetItem(None,
                                                       ['Complete'],
                                                       CompleteTasksFilter(),
                                                       getIcon('FilterComplete.png'))
        tree.addTopLevelItems([
            self._allTasksItem,
            self._uncategorizedTasksItem,
            self._dueItem,
            self._contextsItem,
            self._projectsItem,
            self._completeTasksItem
        ])

    def _initFilterTypeMappings(self):
        self._filterItemByFilterType[ContextFilter] = self._contextsItem
        self._filterItemByFilterType[ProjectFilter] = self._projectsItem
        self._filterItemByFilterType[DueFilter] = self._dueItem

        self._filterIconByFilterType[ContextFilter] = getIcon('FilterContexts.png')
        self._filterIconByFilterType[ProjectFilter] = getIcon('FilterProjects.png')

        self._filterIconByFilterType[DueTodayFilter] = getIcon('FilterDueToday.png')
        self._filterIconByFilterType[DueTomorrowFilter] = getIcon('FilterDueTomorrow.png')
        self._filterIconByFilterType[DueThisWeekFilter] = getIcon('FilterDueWeek.png')
        self._filterIconByFilterType[DueThisMonthFilter] = getIcon('FilterDueMonth.png')
        self._filterIconByFilterType[DueOverdueFilter] = getIcon('FilterDueOverdue.png')

        self._treeItemByFilterType[AllTasksFilter] = self._allTasksItem
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


class FilterTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, strings, filter=None, icon=None, order=None):
        QtWidgets.QTreeWidgetItem.__init__(self, parent, strings)
        self.filter = filter
        if order:
            self.setText(1, str(order))
        if icon:
            self.setIcon(0, icon)

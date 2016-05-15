import logging
import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from qtodotxt.lib import tasklib
from qtodotxt.lib.file import ErrorLoadingFile, File, FileObserver

from qtodotxt.ui.controllers.tasks_list_controller import TasksListController
from qtodotxt.ui.controllers.filters_tree_controller import FiltersTreeController
from qtodotxt.lib.filters import SimpleTextFilter, FutureFilter, IncompleteTasksFilter, CompleteTasksFilter
from qtodotxt.ui.controllers.menu_controller import MenuController
from qtodotxt.ui.resource_manager import getIcon


logger = logging.getLogger(__name__)

FILENAME_FILTERS = ';;'.join([
    'Text Files (*.txt)',
    'All Files (*.*)'])


class MainController(QtCore.QObject):
    def __init__(self, view, dialogs, task_editor_service, args):
        super(MainController, self).__init__()
        self._args = args
        self.view = view

        # use object variable for setting only used in this class
        # others are accessed through QSettings
        self._settings = QtCore.QSettings()
        # self._show_toolbar = int(self._settings.value("show_toolbar", 1))
        # fix migration issue from old settings
        show_toolbar = self._settings.value("show_toolbar", 1)
        if show_toolbar in ("true", "false"):
            show_toolbar = 1
        self._show_toolbar = int(show_toolbar)
        self._show_completed = True
        self._dialogs = dialogs
        self._task_editor_service = task_editor_service
        self._initControllers()
        self._file = File()
        self._fileObserver = FileObserver(self, self._file)
        self._is_modified = False
        self._setIsModified(False)
        self.view.closeEventSignal.connect(self.view_onCloseEvent)
        filters = self._settings.value("current_filters", ["All"])
        self._filters_tree_controller.view.setSelectedFiltersByNames(filters)

    def auto_save(self):
        if int(self._settings.value("auto_save", 1)):
            self.save()

    def _initControllers(self):
        self._initFiltersTree()
        self._initTasksList()
        self._initMenuBar()
        self._initContextualMenu()
        self._initActions()
        self._initToolBar()
        self._initSearchText()

    def _initMenuBar(self):
        menu = self.view.menuBar()
        self._menu_controller = MenuController(self, menu)

    def _initActions(self):
        self.filterViewAction = QtWidgets.QAction(getIcon('sidepane.png'), '&Show Filters', self)
        self.filterViewAction.setCheckable(True)
        # action.setShortcuts(['Ctrl+E']) # what should it be?
        self.filterViewAction.triggered.connect(self._toggleFilterView)

        self.showFutureAction = QtWidgets.QAction(getIcon('future.png'), '&Show Future Tasks', self)
        self.showFutureAction.setCheckable(True)
        # action.setShortcuts(['Ctrl+E']) # what should it be?
        self.showFutureAction.triggered.connect(self._toggleShowFuture)

        self.showCompletedAction = QtWidgets.QAction(getIcon('show_completed.png'), '&Show Completed Tasks', self)
        self.showCompletedAction.setCheckable(True)
        # action.setShortcuts(['Ctrl+E']) # what should it be?
        self.showCompletedAction.triggered.connect(self._toggleShowCompleted)

        self.archiveAction = QtWidgets.QAction(getIcon('archive.png'), '&Archive Completed Tasks', self)
        # action.setShortcuts(['Ctrl+E']) # what should it be?
        self.archiveAction.triggered.connect(self._archive_all_done_tasks)

    def _initToolBar(self):
        toolbar = self.view.addToolBar("Main Toolbar")
        toolbar.setObjectName("mainToolbar")

        toolbar.addAction(self.filterViewAction)
        toolbar.addAction(self.showFutureAction)
        toolbar.addAction(self.showCompletedAction)

        toolbar.addSeparator()

        toolbar.addAction(self._menu_controller.openAction)
        toolbar.addAction(self._menu_controller.saveAction)
        toolbar.addSeparator()
        toolbar.addAction(self._tasks_list_controller.createTaskAction)
        toolbar.addAction(self._tasks_list_controller.editTaskAction)
        toolbar.addSeparator()
        toolbar.addAction(self._tasks_list_controller.completeSelectedTasksAction)
        if int(self._settings.value("show_delete", 0)):
            toolbar.addAction(self._tasks_list_controller.deleteSelectedTasksAction)
        toolbar.addSeparator()
        toolbar.addAction(self._tasks_list_controller.increasePrioritySelectedTasksAction)
        toolbar.addAction(self._tasks_list_controller.decreasePrioritySelectedTasksAction)
        toolbar.addSeparator()
        toolbar.addAction(self.archiveAction)
        toolbar.visibilityChanged.connect(self._toolbar_visibility_changed)
        if not self._show_toolbar:
            toolbar.hide()

    def _toggleShowCompleted(self):
        if self.showCompletedAction.isChecked():
            self._settings.setValue("show_completed_tasks", 1)
            self._show_completed = True
            self.updateFilters()
        else:
            self._settings.setValue("show_completed_tasks", 0)
            self._show_completed = False
            self.updateFilters()
        self._filters_tree_controller.showFilters(self._file, self._show_completed)

    def _toggleShowFuture(self):
        if self.showFutureAction.isChecked():
            self._settings.setValue("show_future_tasks", 1)
            self.updateFilters()
        else:
            self._settings.setValue("show_future_tasks", 0)
            self.updateFilters()

    def _restoreShowFuture(self):
        val = int(self._settings.value("show_future_tasks", 1))
        if val:
            self.showFutureAction.setChecked(True)
            self._toggleShowFuture()
        else:
            self.showFutureAction.setChecked(False)
            self._toggleShowFuture()

    def _toggleFilterView(self):
        if self.filterViewAction.isChecked():
            self._settings.setValue("show_filter_tree", 1)
            self._filters_tree_controller.view.show()
        else:
            self._settings.setValue("splitter_pos", self.view.centralWidget().sizes())
            self._settings.setValue("show_filter_tree", 0)
            self._filters_tree_controller.view.hide()

    def _restoreFilterView(self):
        val = int(self._settings.value("show_filter_tree", 1))
        if val:
            self.filterViewAction.setChecked(True)
            self._toggleFilterView()
        else:
            self.filterViewAction.setChecked(False)
            self._toggleFilterView()

    def _toolbar_visibility_changed(self, val):
        self._show_toolbar = int(val)

    def exit(self):
        self.view.close()
        sys.exit()

    def getView(self):
        return self.view

    def show(self):
        self._updateView()
        self.view.show()
        self._updateTitle()

        if self._args.file:
            filename = self._args.file
        else:
            filename = self._settings.value("last_open_file")

        if filename:
            try:
                self.openFileByName(filename)
            except ErrorLoadingFile as ex:
                self._dialogs.showError(str(ex))

        if self._args.quickadd:
            self._tasks_list_controller.createTask()
            self.save()
            self.exit()

    def _initFiltersTree(self):
        controller = self._filters_tree_controller = \
            FiltersTreeController(self.view.filters_tree_view)
        controller.filterSelectionChanged.connect(
            self._onFilterSelectionChanged)

    def _onFilterSelectionChanged(self, filters):
        self._applyFilters(filters=filters)

    def _applyFilters(self, filters=None, searchText=None):
        # First we filter with filters tree
        if filters is None:
            filters = self._filters_tree_controller.view.getSelectedFilters()
        tasks = tasklib.filterTasks(filters, self._file.tasks)
        # Then with our search text
        if searchText is None:
            searchText = self.view.tasks_view.tasks_search_view.getSearchText()
        tasks = tasklib.filterTasks([SimpleTextFilter(searchText)], tasks)
        # with future filter if needed
        if not self.showFutureAction.isChecked():
            tasks = tasklib.filterTasks([FutureFilter()], tasks)
        # with complete filter if needed
        if not CompleteTasksFilter() in filters and not self.showCompletedAction.isChecked():
            tasks = tasklib.filterTasks([IncompleteTasksFilter()], tasks)
        self._tasks_list_controller.showTasks(tasks)

    def _initSearchText(self):
        self.view.tasks_view.tasks_search_view.searchTextChanged.connect(
            self._onSearchTextChanged)

    def _onSearchTextChanged(self, searchText):
        self._applyFilters(searchText=searchText)

    def _initTasksList(self):
        controller = self._tasks_list_controller = \
            TasksListController(self.view.tasks_view.tasks_list_view, self._task_editor_service)

        controller.taskCreated.connect(self._tasks_list_taskCreated)
        controller.taskModified.connect(self._tasks_list_taskModified)
        controller.taskDeleted.connect(self._tasks_list_taskDeleted)
        controller.taskArchived.connect(self._tasks_list_taskArchived)

    def _initContextualMenu(self):

        # Context menu
        # controller.view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self._tasks_list_controller.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._tasks_list_controller.view.customContextMenuRequested.connect(self.showContextMenu)
        self._contextMenu = QtWidgets.QMenu()
        self._contextMenu.addAction(self._tasks_list_controller.createTaskAction)
        self._contextMenu.addAction(self._tasks_list_controller.editTaskAction)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self._tasks_list_controller.completeSelectedTasksAction)
        if int(self._settings.value("show_delete", 0)):
            self._contextMenu.addAction(self._tasks_list_controller.deleteSelectedTasksAction)
        self._contextMenu.addSeparator()
        self._contextMenu.addAction(self._tasks_list_controller.increasePrioritySelectedTasksAction)
        self._contextMenu.addAction(self._tasks_list_controller.decreasePrioritySelectedTasksAction)

    def showContextMenu(self, position):
        tasks = self._tasks_list_controller.view.getSelectedTasks()
        if tasks:
            self._contextMenu.exec_(self._tasks_list_controller.view.mapToGlobal(position))

    def _tasks_list_taskDeleted(self, task):
        self._file.tasks.remove(task)
        self._onFileUpdated()

    def _tasks_list_taskCreated(self, task):
        self._file.tasks.append(task)
        self._onFileUpdated()

    def _tasks_list_taskModified(self, task):
        self._onFileUpdated()

    def _tasks_list_taskArchived(self, task):
        self._file.saveDoneTask(task)
        self._file.tasks.remove(task)
        self._onFileUpdated()

    def _archive_all_done_tasks(self):
        done = [task for task in self._file.tasks if task.is_complete]
        for task in done:
            self._file.saveDoneTask(task)
            self._file.tasks.remove(task)
        self._onFileUpdated()

    def _onFileUpdated(self):
        self._filters_tree_controller.showFilters(self._file, self._show_completed)
        self._task_editor_service.updateValues(self._file)
        self._setIsModified(True)
        self.auto_save()

    def _canExit(self):
        if not self._is_modified:
            return True
        button = self._dialogs.showSaveDiscardCancel('Unsaved changes...')
        if button == QtWidgets.QMessageBox.Save:
            self.save()
            return True
        else:
            return button == QtWidgets.QMessageBox.Discard

    def view_onCloseEvent(self, closeEvent):
        if self._canExit():
            self._settings.setValue("show_toolbar", self._show_toolbar)
            if self.filterViewAction.isChecked():  # we only save size if it is visible
                self._settings.setValue("splitter_pos", self.view.centralWidget().sizes())
            self._settings.setValue("current_filters", self._filters_tree_controller.view.getSelectedFilterNames())
            self._settings.setValue("main_window_geometry", self.view.saveGeometry())
            self._settings.setValue("main_window_state", self.view.saveState())

            closeEvent.accept()
        else:
            closeEvent.ignore()

    def _setIsModified(self, is_modified):
        self._is_modified = is_modified
        self._updateTitle()
        self._menu_controller.saveAction.setEnabled(is_modified)
        self._menu_controller.revertAction.setEnabled(is_modified)

    def save(self):
        logger.debug('MainController.save called.')
        self._fileObserver.clear()
        filename = self._file.filename
        ok = True
        if not filename:
            (filename, ok) = \
                QtWidgets.QFileDialog.getSaveFileName(self.view, filter=FILENAME_FILTERS)
        if ok and filename:
            self._file.save(filename)
            self._settings.setValue("last_open_file", filename)
            self._settings.sync()
            self._setIsModified(False)
            logger.debug('Adding {} to watchlist'.format(filename))
            self._fileObserver.addPath(self._file.filename)

    def _updateTitle(self):
        title = 'QTodoTxt - '
        if self._file.filename:
            filename = os.path.basename(self._file.filename)
            title += filename
        else:
            title += 'Untitled'
        if self._is_modified:
            title += ' (*)'
        self.view.setWindowTitle(title)

    def open(self):
        (filename, ok) = \
            QtWidgets.QFileDialog.getOpenFileName(self.view, filter=FILENAME_FILTERS)

        if ok and filename:
            try:
                self.openFileByName(filename)
            except ErrorLoadingFile as ex:
                self._dialogs.showError(str(ex))

    def new(self):
        if self._canExit():
            self._file = File()
            self._loadFileToUI()

    def revert(self):
        if self._dialogs.showConfirm('Revert to saved file (and lose unsaved changes)?'):
            try:
                self.openFileByName(self._file.filename)
            except ErrorLoadingFile as ex:
                self._dialogs.showError(str(ex))

    def openFileByName(self, filename):
        logger.debug('MainController.openFileByName called with filename="{}"'.format(filename))
        self._fileObserver.clear()
        self._file.load(filename)
        self._loadFileToUI()
        self._settings.setValue("last_open_file", filename)
        self._settings.sync()
        logger.debug('Adding {} to watchlist'.format(filename))
        self._fileObserver.addPath(self._file.filename)

    def _loadFileToUI(self):
        self._setIsModified(False)
        self._filters_tree_controller.showFilters(self._file, self._show_completed)
        self._task_editor_service.updateValues(self._file)

    def _updateView(self):
        self.view.restoreGeometry(self._settings.value("main_window_geometry", b""))
        self.view.restoreState(self._settings.value("main_window_state", b""))
        splitterPosition = self._settings.value("splitter_pos", (200, 400))
        splitterPosition = [int(x) for x in splitterPosition]
        self.view.centralWidget().setSizes(splitterPosition)
        self._restoreShowCompleted()
        self._restoreFilterView()
        self._restoreShowFuture()

    def _restoreShowCompleted(self):
        val = int(self._settings.value("show_completed_tasks", 1))
        if val:
            self._show_completed = True
            self.showCompletedAction.setChecked(True)
        else:
            self._show_completed = False
            self.showCompletedAction.setChecked(False)

    def updateFilters(self):
        self._onFilterSelectionChanged(self._filters_tree_controller.view.getSelectedFilters())

    def toggleVisible(self):
        if self.view.isMinimized():
            self.view.showNormal()
            self.view.activateWindow()
        else:
            self.view.showMinimized()

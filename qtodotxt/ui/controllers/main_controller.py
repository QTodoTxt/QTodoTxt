import logging
import os
import sys

from PySide import QtCore
from PySide import QtGui

from qtodotxt.lib import task_parser
from qtodotxt.lib.file import ErrorLoadingFile, File, FileObserver

from qtodotxt.ui.controllers.tasks_list_controller import TasksListController
from qtodotxt.ui.controllers.filters_tree_controller import FiltersTreeController
from qtodotxt.lib.filters import SimpleTextFilter, FutureFilter
from qtodotxt.ui.controllers.menu_controller import MenuController


logger = logging.getLogger(__name__)

FILENAME_FILTERS = ';;'.join([
    'Text Files (*.txt)',
    'All Files (*.*)'])


class MainController(QtCore.QObject):
    def __init__(self, view, dialogs, task_editor_service, args):
        super(MainController, self).__init__()
        self._args = args
        self._view = view
        self._settings = QtCore.QSettings()
        # use object variable for setting only used in this class
        # others are accesed through QSettings
        self._show_toolbar = int(self._settings.value("show_toolbar", 1)) 
        self._auto_save = int(self._settings.value("auto_save", 1))
        self._hide_future_tasks = int(self._settings.value("hide_future_tasks", 1))
        self._dialogs = dialogs
        self._task_editor_service = task_editor_service
        self._initControllers()
        self._file = File()
        self._fileObserver = FileObserver(self, self._file)
        self._is_modified = False
        self._setIsModified(False)
        self._view.closeEventSignal.connect(self._view_onCloseEvent)

    def auto_save(self):
        if self._auto_save:
            self.save()

    def _initControllers(self):
        self._initFiltersTree()
        self._initTasksList()
        self._initMenuBar()
        self._initToolBar()
        self._initFilterText()

    def _initMenuBar(self):
        menu = self._view.menuBar()
        self._menu_controller = MenuController(self, menu)

    def _initToolBar(self):
        toolbar = self._view.addToolBar("Main Toolbar")
        toolbar.addAction(self._menu_controller.saveAction)
        toolbar.addAction(self._tasks_list_controller.createTaskAction)
        toolbar.addAction(self._tasks_list_controller.deleteSelectedTasksAction)
        toolbar.addAction(self._tasks_list_controller.completeSelectedTasksAction)
        toolbar.addAction(self._tasks_list_controller.decreasePrioritySelectedTasksAction)
        toolbar.addAction(self._tasks_list_controller.increasePrioritySelectedTasksAction)
        toolbar.visibilityChanged.connect(self._toolbar_visibility_changed)
        if not self._show_toolbar:
            toolbar.hide()

    def _toolbar_visibility_changed(self, val):
        self._show_toolbar = int(val)

    def exit(self):
        self._view.close()
        sys.exit()

    def getView(self):
        return self._view

    def show(self):
        self._view.show()
        self._updateTitle()
        self._updateCreatePref()
        self._updateAutoSavePref()
        self._updateAutoArchivePref()
        self._updateHideFutureTasksPref()
        self._updateView()

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
            FiltersTreeController(self._view.filters_tree_view)
        controller.filterSelectionChanged.connect(
            self._onFilterSelectionChanged)

    def _onFilterSelectionChanged(self, filters):
        # First we filter with filters tree
        treeTasks = task_parser.filterTasks(filters, self._file.tasks)
        # Then with our filter text
        filterText = self._view.tasks_view.tasks_filter.getText()
        tasks = task_parser.filterTasks([SimpleTextFilter(filterText)], treeTasks)
        # And finally with future filter if needed
        # TODO: refactor all that filters
        if self._hide_future_tasks:
            tasks = task_parser.filterTasks([FutureFilter()], tasks)
        self._tasks_list_controller.showTasks(tasks)

    def _initFilterText(self):
        self._view.tasks_view.tasks_filter.filterTextChanged.connect(
            self._onFilterTextChanged)

    def _onFilterTextChanged(self, text):
        # First we filter with filters tree
        filters = self._filters_tree_controller._view.getSelectedFilters()
        treeTasks = task_parser.filterTasks(filters, self._file.tasks)
        # Then with our filter text
        tasks = task_parser.filterTasks([SimpleTextFilter(text)], treeTasks)
        # And finally with future filter if needed
        # TODO: refactor all that filters
        if self._hide_future_tasks:
            tasks = task_parser.filterTasks([FutureFilter()], tasks)
        self._tasks_list_controller.showTasks(tasks)

    def _initTasksList(self):
        controller = self._tasks_list_controller = \
            TasksListController(self._view.tasks_view.tasks_list_view, self._task_editor_service)

        controller.taskCreated.connect(self._tasks_list_taskCreated)
        controller.taskModified.connect(self._tasks_list_taskModified)
        controller.taskDeleted.connect(self._tasks_list_taskDeleted)
        controller.taskArchived.connect(self._tasks_list_taskArchived)

        # Context menu
        # controller._view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        controller._view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        controller._view.customContextMenuRequested.connect(self.showContextMenu)
        self._contextMenu = QtGui.QMenu()
        self._contextMenu.addAction(self._tasks_list_controller.deleteSelectedTasksAction)
        self._contextMenu.addAction(self._tasks_list_controller.completeSelectedTasksAction)
        self._contextMenu.addAction(self._tasks_list_controller.decreasePrioritySelectedTasksAction)
        self._contextMenu.addAction(self._tasks_list_controller.increasePrioritySelectedTasksAction)

    def showContextMenu(self, position):
        tasks = self._tasks_list_controller._view.getSelectedTasks()
        if tasks:
            self._contextMenu.exec_(self._tasks_list_controller._view.mapToGlobal(position))

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

    def _onFileUpdated(self):
        self._filters_tree_controller.showFilters(self._file)
        self._task_editor_service.updateValues(self._file)
        self._setIsModified(True)
        self.auto_save()

    def _canExit(self):
        if not self._is_modified:
            return True
        button = self._dialogs.showSaveDiscardCancel('Unsaved changes...')
        if button == QtGui.QMessageBox.Save:
            self.save()
            return True
        else:
            return button == QtGui.QMessageBox.Discard

    def _view_onCloseEvent(self, closeEvent):
        if self._canExit():
            self._settings.setValue("main_window_geometry", self._view.saveGeometry())
            self._settings.setValue("main_window_state", self._view.saveState())

            self._settings.setValue("show_toolbar", self._show_toolbar)
            self._settings.setValue("auto_save", self._auto_save)
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
                QtGui.QFileDialog.getSaveFileName(self._view, filter=FILENAME_FILTERS)
        if ok and filename:
            self._file.save(filename)
            self._settings.setValue("last_open_file", filename)
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
        self._view.setWindowTitle(title)

    def open(self):
        (filename, ok) = \
            QtGui.QFileDialog.getOpenFileName(self._view, filter=FILENAME_FILTERS)

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
        logger.debug('Adding {} to watchlist'.format(filename))
        self._fileObserver.addPath(self._file.filename)

    def _loadFileToUI(self):
        self._setIsModified(False)
        self._filters_tree_controller.showFilters(self._file)
        self._task_editor_service.updateValues(self._file)

    def _updateCreatePref(self):
        self._menu_controller.changeCreatedDateState(bool(int(self._settings.value("add_created_date", 1))))

    def _updateAutoSavePref(self):
        self._menu_controller.changeAutoSaveState(self._auto_save)

    def _updateAutoArchivePref(self):
        self._menu_controller.changeAutoArchiveState(bool(int(self._settings.value("auto_archive", 1))))

    def _updateHideFutureTasksPref(self):
        self._menu_controller.changeHideFutureTasksState(bool(int(self._settings.value("hide_future_tasks", 1))))

    def _updateView(self):
        self._view.restoreGeometry(self._settings.value("main_window_geometry"))
        self._view.restoreState(self._settings.value("main_window_state"))

    def createdDate(self):
        self._settings.setValue("add_created_date", 0 if int(self._settings.value("add_created_date", 1)) else 1)

    def toggleAutoSave(self):
        self._auto_save = not self._auto_save

    def toggleAutoArchive(self):
        self._settings.setValue("auto_archive", 0 if int(self._settings.value("auto_archive", 1)) else 1)

    def toggleHideFutureTasks(self):
        self._settings.setValue("hide_future_tasks", 0 if int(self._settings.value("hide_future_tasks", 1)) else 1)
        self._onFilterSelectionChanged(self._filters_tree_controller._view.getSelectedFilters())

    def toggleVisible(self):
        if self._view.isMinimized():
            self._view.showNormal()
            self._view.activateWindow()
        else:
            self._view.showMinimized()

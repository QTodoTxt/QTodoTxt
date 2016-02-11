from PySide import QtCore
from PySide import QtGui

from qtodotxt.ui.dialogs import about_dialog
from qtodotxt.ui.resource_manager import getIcon


class MenuController(QtCore.QObject):
    def __init__(self, main_controller, menu):
        super(MenuController, self).__init__()
        self._main_controller = main_controller
        self._menu = menu
        self._initMenuBar()

    def _initMenuBar(self):
        self._initFileMenu()
        self._initEditMenu()
        self._initHelpMenu()

    def _initFileMenu(self):
        fileMenu = self._menu.addMenu('&File')
        fileMenu.addAction(self._createNewAction())
        fileMenu.addAction(self._createOpenAction())
        fileMenu.addAction(self._createSaveAction())
        fileMenu.addAction(self._createRevertAction())
        fileMenu.addSeparator()
        preferenceMenu = fileMenu.addMenu(getIcon('ApplicationPreferences.png'), '&Preferences')
        preferenceMenu.addAction(self._createPreferenceAction())
        preferenceMenu.addAction(self._autoSavePreferenceAction())
        preferenceMenu.addAction(self._autoArchivePreferenceAction())
        preferenceMenu.addAction(self._hideFutureTasksAction())
        fileMenu.addSeparator()
        fileMenu.addAction(self._createExitAction())

    def _initEditMenu(self):
        editMenu = self._menu.addMenu('&Edit')
        tlc = self._main_controller._tasks_list_controller
        editMenu.addAction(tlc.createTaskAction)
        editMenu.addAction(tlc.editTaskAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.deleteSelectedTasksAction)
        editMenu.addAction(tlc.completeSelectedTasksAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.decreasePrioritySelectedTasksAction)
        editMenu.addAction(tlc.increasePrioritySelectedTasksAction)

    def _initHelpMenu(self):
        helpMenu = self._menu.addMenu('&Help')
        helpMenu.addAction(self._createAboutAction())

    def _createAboutAction(self):
        action = QtGui.QAction(getIcon('ApplicationAbout.png'), '&About', self)
        action.triggered.connect(self._about)
        return action

    def _about(self):
        about_dialog.show(self._menu)

    def _createNewAction(self):
        action = QtGui.QAction(getIcon('FileNew.png'), '&New', self)
        # infrequent action, I prefer to use ctrl+n for new task.
        action.setShortcuts(["Ctrl+Shift+N"])
        action.triggered.connect(self._main_controller.new)
        return action

    def _createOpenAction(self):
        action = QtGui.QAction(getIcon('FileOpen.png'), '&Open', self)
        action.setShortcuts(["Ctrl+O"])
        action.triggered.connect(self._main_controller.open)
        self.openAction = action
        return action

    def _createSaveAction(self):
        action = QtGui.QAction(getIcon('FileSave.svg'), '&Save', self)
        action.setShortcuts(["Ctrl+S"])
        action.triggered.connect(self._main_controller.save)
        self.saveAction = action
        return action

    def _createRevertAction(self):
        action = QtGui.QAction(getIcon('FileRevert.png'), '&Revert', self)
        action.triggered.connect(self._main_controller.revert)
        self.revertAction = action
        return action

    def _createPreferenceAction(self):
        action = QtGui.QAction('Add created date', self, checkable=True)
        action.triggered.connect(self._main_controller.toggleCreatedDate)
        self.prefAction = action
        return action

    def _autoSavePreferenceAction(self):
        action = QtGui.QAction('Enable auto save', self, checkable=True)
        action.triggered.connect(self._main_controller.toggleAutoSave)
        self.autoSaveAction = action
        return action

    def _autoArchivePreferenceAction(self):
        action = QtGui.QAction('Enable auto archive', self, checkable=True)
        action.triggered.connect(self._main_controller.toggleAutoArchive)
        self.autoArchiveAction = action
        return action

    def _hideFutureTasksAction(self):
        action = QtGui.QAction('Hide future tasks', self, checkable=True)
        action.triggered.connect(self._main_controller.toggleHideFutureTasks)
        self.hideFutureTasksAction = action
        return action

    def changeAutoSaveState(self, value=False):
        self.autoSaveAction.setChecked(value)

    def changeCreatedDateState(self, value=False):
        self.prefAction.setChecked(value)

    def changeAutoArchiveState(self, value=False):
        self.autoArchiveAction.setChecked(value)

    def changeHideFutureTasksState(self, value=False):
        self.hideFutureTasksAction.setChecked(value)

    def _createExitAction(self):
        action = QtGui.QAction(getIcon('ApplicationExit.png'), 'E&xit', self)
        action.setShortcuts(["Alt+F4"])
        action.triggered.connect(self._main_controller.exit)
        return action

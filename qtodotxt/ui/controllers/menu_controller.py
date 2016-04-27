from PyQt5 import QtCore
from PyQt5 import QtWidgets

from qtodotxt.ui.dialogs import about_dialog
from qtodotxt.ui.resource_manager import getIcon
from qtodotxt.ui.dialogs.settings import Settings


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
        fileMenu.addAction(self._createPreferenceAction())
        fileMenu.addSeparator()
        fileMenu.addAction(self._createExitAction())

    def _initEditMenu(self):
        editMenu = self._menu.addMenu('&Edit')
        tlc = self._main_controller._tasks_list_controller
        editMenu.addAction(tlc.createTaskAction)
        editMenu.addAction(tlc.editTaskAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.completeSelectedTasksAction)
        if int(QtCore.QSettings().value("show_delete", 0)):
            editMenu.addAction(tlc.deleteSelectedTasksAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.increasePrioritySelectedTasksAction)
        editMenu.addAction(tlc.decreasePrioritySelectedTasksAction)

    def _initHelpMenu(self):
        helpMenu = self._menu.addMenu('&Help')
        helpMenu.addAction(self._createAboutAction())

    def _createAboutAction(self):
        action = QtWidgets.QAction(getIcon('ApplicationAbout.png'), '&About', self)
        action.triggered.connect(self._about)
        return action

    def _about(self):
        about_dialog.show(self._menu)

    def _createNewAction(self):
        action = QtWidgets.QAction(getIcon('FileNew.png'), '&New', self)
        # infrequent action, I prefer to use ctrl+n for new task.
        action.setShortcuts(["Ctrl+Shift+N"])
        action.triggered.connect(self._main_controller.new)
        self.newAction = action
        return action

    def _createOpenAction(self):
        action = QtWidgets.QAction(getIcon('FileOpen.png'), '&Open', self)
        action.setShortcuts(["Ctrl+O"])
        action.triggered.connect(self._main_controller.open)
        self.openAction = action
        return action

    def _createSaveAction(self):
        action = QtWidgets.QAction(getIcon('FileSave.png'), '&Save', self)
        action.setShortcuts(["Ctrl+S"])
        action.triggered.connect(self._main_controller.save)
        self.saveAction = action
        return action

    def _createRevertAction(self):
        action = QtWidgets.QAction(getIcon('FileRevert.png'), '&Revert', self)
        action.triggered.connect(self._main_controller.revert)
        self.revertAction = action
        return action

    def _createPreferenceAction(self):
        action = QtWidgets.QAction('&Preferences', self)
        action.triggered.connect(self._show_preferences)
        self.preferencesAction = action
        return action

    def _createExitAction(self):
        action = QtWidgets.QAction(getIcon('ApplicationExit.png'), 'E&xit', self)
        action.setShortcuts(["Alt+F4"])
        action.triggered.connect(self._main_controller.exit)
        return action

    def _show_preferences(self):
        print(self._main_controller.view)
        settings = Settings(self._main_controller)
        settings.show()

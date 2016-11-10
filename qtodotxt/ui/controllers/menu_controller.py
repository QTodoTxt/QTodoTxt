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
        self.maxRecentFiles = 3  # constant determines the number of files stored in the history
        self.recentFileArray = []
        self._initMenuBar()

    def _initMenuBar(self):
        self._initFileMenu()
        self._initEditMenu()
        self._initViewMenu()
        self._initHelpMenu()

    def _initFileMenu(self):
        fileMenu = self._menu.addMenu(self.tr('&File'))
        fileMenu.addAction(self._createNewAction())
        fileMenu.addAction(self._createOpenAction())

        lastOpened = fileMenu.addMenu(getIcon('FileOpen.png'), "Open &Recent")
        for ind in range(self.maxRecentFiles):
            self.recentFileArray.append(QtWidgets.QAction(self, visible=False, triggered=self.openRecentFile))
            lastOpened.addAction(self.recentFileArray[ind])

        fileMenu.addAction(self._createSaveAction())
        fileMenu.addAction(self._createRevertAction())
        fileMenu.addSeparator()
        fileMenu.addAction(self._createPreferenceAction())
        fileMenu.addSeparator()
        fileMenu.addAction(self._createExitAction())

    def updateRecentFileActions(self):
        recentFileNames = self.getRecentFileNames()
        ind = 1
        for i in range(len(recentFileNames)):
            text = "&%d %s" % (ind, recentFileNames[i])
            self.recentFileArray[i].setText(text)
            self.recentFileArray[i].setIcon(getIcon('FileOpen.png'))
            self.recentFileArray[i].setData(recentFileNames[i])
            self.recentFileArray[i].setVisible(True)
            self.recentFileArray[i].setShortcuts(["Ctrl+" + str(ind)])
            ind += 1

    def getRecentFileNames(self):
        recentFileNames = []
        recentFileNames.append(QtCore.QSettings().value("lastOpened", []))
        return recentFileNames[0]

    def openRecentFile(self):
        action = self.sender()
        if action:
            self._main_controller.openFileByName(action.data())

    def _initEditMenu(self):
        editMenu = self._menu.addMenu(self.tr('&Edit'))
        tlc = self._main_controller._tasks_list_controller
        editMenu.addAction(tlc.createTaskAction)
        editMenu.addAction(tlc.editTaskAction)
        editMenu.addAction(tlc.copySelectedTasksAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.completeSelectedTasksAction)
        if int(QtCore.QSettings().value("show_delete", 0)):
            editMenu.addAction(tlc.deleteSelectedTasksAction)
        editMenu.addSeparator()
        editMenu.addAction(tlc.increasePrioritySelectedTasksAction)
        editMenu.addAction(tlc.decreasePrioritySelectedTasksAction)

    def _initViewMenu(self):
        viewMenu = self._menu.addMenu(self.tr('&View'))
        viewMenu.addAction(self._main_controller.showToolBarAction)
        viewMenu.addSeparator()
        viewMenu.addAction(self._main_controller.filterViewAction)
        viewMenu.addAction(self._main_controller.showFutureAction)
        viewMenu.addAction(self._main_controller.showCompletedAction)
        viewMenu.addAction(self._main_controller.showSearchAction)

    def _initHelpMenu(self):
        helpMenu = self._menu.addMenu(self.tr('&Help'))
        helpMenu.addAction(self._createAboutAction())

    def _createAboutAction(self):
        action = QtWidgets.QAction(getIcon('ApplicationAbout.png'), '&About', self)
        action.triggered.connect(self._about)
        return action

    def _about(self):
        about_dialog.show(self._menu)

    def _createNewAction(self):
        action = QtWidgets.QAction(getIcon('FileNew.png'), self.tr('&New'), self)
        # infrequent action, I prefer to use ctrl+n for new task.
        action.setShortcuts(["Ctrl+Shift+N"])
        action.triggered.connect(self._main_controller.new)
        self.newAction = action
        return action

    def _createOpenAction(self):
        action = QtWidgets.QAction(getIcon('FileOpen.png'), self.tr('&Open'), self)
        action.setShortcuts(["Ctrl+O"])
        action.triggered.connect(self._main_controller.open)
        self.openAction = action
        return action

    def _createSaveAction(self):
        action = QtWidgets.QAction(getIcon('FileSave.png'), self.tr('&Save'), self)
        action.setShortcuts(["Ctrl+S"])
        action.triggered.connect(self._main_controller.save)
        self.saveAction = action
        return action

    def _createRevertAction(self):
        action = QtWidgets.QAction(getIcon('FileRevert.png'), self.tr('&Revert'), self)
        action.triggered.connect(self._main_controller.revert)
        self.revertAction = action
        return action

    def _createPreferenceAction(self):
        action = QtWidgets.QAction(getIcon('ApplicationPreferences.png'), self.tr('&Preferences'), self)
        action.triggered.connect(self._show_preferences)
        self.preferencesAction = action
        return action

    def _createExitAction(self):
        action = QtWidgets.QAction(getIcon('ApplicationExit.png'), self.tr('E&xit'), self)
        action.setShortcuts(["Ctrl+Q"])
        action.triggered.connect(self._main_controller.exit)
        return action

    def _show_preferences(self):
        settings = Settings(self._main_controller)
        # simplest way to stop the preferences dialog from being left on screen
        #  when the main app window is hidden is to create it as a modal dialog
        settings.setModal(True)
        settings.show()

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from qtodotxt.ui.dialogs.settingsui import Ui_SettingsUI


class Settings(QtWidgets.QDialog):

    def __init__(self, maincontroller):
        QtWidgets.QDialog.__init__(self, maincontroller._view)
        self.maincontroller = maincontroller
        self.ui = Ui_SettingsUI()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings()

        self.load_settings()
        self.connect_all()

    def load_settings(self):
        self._int_settings_to_cb("auto_save", self.ui.autoSaveCheckBox)
        self._int_settings_to_cb("auto_archive", self.ui.autoArchiveCheckBox)
        self._int_settings_to_cb("add_created_date", self.ui.addCreatedDateCheckBox)
        self._int_settings_to_cb("hide_future_tasks", self.ui.hideFutureTasksCheckBox)
        self._int_settings_to_cb("confirm_complete", self.ui.confirmCompletionCheckBox)
        self._int_settings_to_cb("enable_tray", self.ui.trayCheckBox)
        priority = self.settings.value("lowest_priority", "D")
        self.ui.lowestPriorityLineEdit.setText(priority)

    def _int_settings_to_cb(self, name, checkBox):
        val = int(self.settings.value(name, 1))
        if val:
            checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            checkBox.setCheckState(QtCore.Qt.Unchecked)

    def connect_all(self):
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.autoSaveCheckBox.stateChanged.connect(self.setAutoSave)
        self.ui.autoArchiveCheckBox.stateChanged.connect(self.setAutoArchive)
        self.ui.addCreatedDateCheckBox.stateChanged.connect(self.setAddCreatedDate)
        self.ui.hideFutureTasksCheckBox.stateChanged.connect(self.setHideFutureTasks)
        self.ui.confirmCompletionCheckBox.stateChanged.connect(self.setConfirmCompletion)
        self.ui.trayCheckBox.stateChanged.connect(self.enableTray)
        self.ui.lowestPriorityLineEdit.textChanged.connect(self.setLowestPriority)

    def _save_int_cb(self, name, val):
        if val == 0:
            self.settings.setValue(name, 0)
        else:
            self.settings.setValue(name, 1)

    def setAutoSave(self, val):
        self._save_int_cb("auto_save", val)

    def setAutoArchive(self, val):
        self._save_int_cb("auto_archive", val)

    def setAddCreatedDate(self, val):
        self._save_int_cb("add_created_date", val)

    def setHideFutureTasks(self, val):
        self._save_int_cb("hide_future_tasks", val)
        self.maincontroller.updateFilters()

    def setConfirmCompletion(self, val):
        self._save_int_cb("confirm_complete", val)

    def enableTray(self, val):
        self._save_int_cb("enable_tray", val)

    def setLowestPriority(self, text):
        self.settings.setValue("lowest_priority", text)


if __name__ == "__main__":
    QtCore.QCoreApplication.setOrganizationName("QTodoTxt")
    QtCore.QCoreApplication.setApplicationName("QTodoTxt")
    app = QtGui.QApplication(sys.argv)
    s = Settings(None)
    s.show()
    sys.exit(app.exec_())

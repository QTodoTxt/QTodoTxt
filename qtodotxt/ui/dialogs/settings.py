import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from qtodotxt.ui.dialogs.settingsui import Ui_SettingsUI


class Settings(QtWidgets.QDialog):

    def __init__(self, maincontroller):
        QtWidgets.QDialog.__init__(self, maincontroller.view)
        self.maincontroller = maincontroller
        self.ui = Ui_SettingsUI()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings()
        self.setWindowFlags(QtCore.Qt.Dialog
                            | QtCore.Qt.MSWindowsFixedSizeDialogHint
                            | QtCore.Qt.WindowStaysOnBottomHint
                            | QtCore.Qt.WindowSystemMenuHint
                            | QtCore.Qt.WindowTitleHint
                            | QtCore.Qt.WindowCloseButtonHint)

        self.load_settings()
        self.connect_all()

    def load_settings(self):
        self._int_settings_to_cb("auto_save", self.ui.autoSaveCheckBox)
        self._int_settings_to_cb("singleton", self.ui.singletonCheckBox, 0)
        self._int_settings_to_cb("auto_archive", self.ui.autoArchiveCheckBox, 0)
        self._int_settings_to_cb("add_created_date", self.ui.addCreatedDateCheckBox, 0)
        self._int_settings_to_cb("confirm_complete", self.ui.confirmCompletionCheckBox)
        self._int_settings_to_cb("show_delete", self.ui.deleteActionCheckBox, 1)
        priority = self.settings.value("lowest_priority", "D")
        self.ui.lowestPriorityLineEdit.setText(priority)
        self._int_settings_to_cb("enable_tray", self.ui.trayCheckBox, 0)
        self._int_settings_to_cb("hide_to_tray", self.ui.hideToTrayCheckBox, 0)
        self._int_settings_to_cb("hide_on_startup", self.ui.hideOnStartupCheckBox, 0)
        self._int_settings_to_cb("close_to_tray", self.ui.closeToTrayCheckBox, 0)
        self._int_settings_to_cb("use_task_dialog", self.ui.useTaskDialogCheckBox, 0)

        val = int(self.settings.value("enable_tray", 0))
        self.ui.hideToTrayCheckBox.setEnabled(val)
        self.ui.hideOnStartupCheckBox.setEnabled(val)
        self.ui.closeToTrayCheckBox.setEnabled(val)

        val = self.settings.value("color_schem", "")
        index = self.ui.colorSchemComboBox.findText(val, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.ui.colorSchemComboBox.setCurrentIndex(index)

    def _int_settings_to_cb(self, name, checkBox, default=1):
        val = int(self.settings.value(name, default))
        if val:
            checkBox.setCheckState(QtCore.Qt.Checked)
        else:
            checkBox.setCheckState(QtCore.Qt.Unchecked)

    def connect_all(self):
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.singletonCheckBox.stateChanged.connect(self.setSingletonCheckBox)
        self.ui.autoSaveCheckBox.stateChanged.connect(self.setAutoSave)
        self.ui.autoArchiveCheckBox.stateChanged.connect(self.setAutoArchive)
        self.ui.addCreatedDateCheckBox.stateChanged.connect(self.setAddCreatedDate)
        self.ui.confirmCompletionCheckBox.stateChanged.connect(self.setConfirmCompletion)
        self.ui.deleteActionCheckBox.stateChanged.connect(self.setDeleteAction)
        self.ui.lowestPriorityLineEdit.textChanged.connect(self.setLowestPriority)
        self.ui.trayCheckBox.stateChanged.connect(self.enableTray)
        self.ui.hideToTrayCheckBox.stateChanged.connect(self.setHideToTray)
        self.ui.hideOnStartupCheckBox.stateChanged.connect(self.setHideOnStartup)
        self.ui.closeToTrayCheckBox.stateChanged.connect(self.setCloseToTray)
        self.ui.colorSchemComboBox.currentIndexChanged.connect(self.setColorSchemCombo)
        self.ui.useTaskDialogCheckBox.stateChanged.connect(self.setUseTaskDialog)

    def _save_int_cb(self, name, val):
        if val == 0:
            self.settings.setValue(name, 0)
        else:
            self.settings.setValue(name, 1)

    def setUseTaskDialog(self, val):
        self._save_int_cb("use_task_dialog", val)

    def setSingletonCheckBox(self, val):
        self._save_int_cb("singleton", val)

    def setAutoSave(self, val):
        self._save_int_cb("auto_save", val)

    def setDeleteAction(self, val):
        self._save_int_cb("show_delete", val)

    def setAutoArchive(self, val):
        self._save_int_cb("auto_archive", val)

    def setAddCreatedDate(self, val):
        self._save_int_cb("add_created_date", val)

    def setConfirmCompletion(self, val):
        self._save_int_cb("confirm_complete", val)

    def setLowestPriority(self, text):
        self.settings.setValue("lowest_priority", text)

    def enableTray(self, val):
        self._save_int_cb("enable_tray", val)
        self.ui.hideToTrayCheckBox.setEnabled(val)
        self.ui.hideOnStartupCheckBox.setEnabled(val)
        self.ui.closeToTrayCheckBox.setEnabled(val)

    def setHideToTray(self, val):
        self._save_int_cb("hide_to_tray", val)

    def setHideOnStartup(self, val):
        self._save_int_cb("hide_on_startup", val)

    def setCloseToTray(self, val):
        self._save_int_cb("close_to_tray", val)

    def closeEvent(self, event):
        self.deleteLater()
        self.maincontroller.view.show()

    def setColorSchemCombo(self, val):
        name = self.ui.colorSchemComboBox.itemText(val)
        self.settings.setValue("color_schem", name)


if __name__ == "__main__":
    QtCore.QCoreApplication.setOrganizationName("QTodoTxt")
    QtCore.QCoreApplication.setApplicationName("QTodoTxt")
    app = QtGui.QApplication(sys.argv)
    s = Settings(None)
    s.show()
    sys.exit(app.exec_())

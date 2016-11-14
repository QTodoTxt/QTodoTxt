import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from qtodotxt.ui.dialogs.shortcutsui import Ui_ShortcutsUI


class Shortcuts(QtWidgets.QDialog):

    def __init__(self, maincontroller):
        QtWidgets.QDialog.__init__(self, maincontroller.view)
        self.maincontroller = maincontroller
        self.ui = Ui_ShortcutsUI()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings()
        self.setWindowFlags(QtCore.Qt.Dialog
                            | QtCore.Qt.MSWindowsFixedSizeDialogHint
                            | QtCore.Qt.WindowStaysOnBottomHint
                            | QtCore.Qt.WindowSystemMenuHint
                            | QtCore.Qt.WindowTitleHint
                            | QtCore.Qt.WindowCloseButtonHint)

        self.model = QtGui.QStandardItemModel(0, 2, self)
        self.model.setHeaderData(0, 1, self.tr("Comment"))
        self.model.setHeaderData(1, 1, self.tr("Shortcut"))

        self.ui.tableView.setModel(self.model)

        self.addShortcuts(self.maincontroller.findChildren(QtWidgets.QAction))
        self.addShortcuts(self.maincontroller.view.findChildren(QtWidgets.QAction))
        self.addShortcuts(self.maincontroller._tasks_list_controller.findChildren(QtWidgets.QAction))
        self.addShortcuts(self.maincontroller._menu_controller.findChildren(QtWidgets.QAction))

        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setColumnWidth(1, 200)

        self.ui.tableView.setColumnWidth(0, 230)
        self.ui.tableView.setColumnWidth(1, 230)

        self.ui.closeButton.clicked.connect(self.close)

    def addShortcuts(self, list):
        row = self.model.rowCount()
        for action in list:
            if action.shortcut().toString() != "":
                comment = action.text()
                for shortcut in action.shortcuts():
                    self.model.insertRow(row)
                    self.model.setData(self.model.index(row, 0), comment)
                    self.model.setData(self.model.index(row, 1), shortcut.toString())
                    row += 1

    def closeEvent(self, event):
        self.deleteLater()
        self.maincontroller.view.show()


if __name__ == "__main__":
    QtCore.QCoreApplication.setOrganizationName("QTodoTxt")
    QtCore.QCoreApplication.setApplicationName("QTodoTxt")
    app = QtGui.QApplication(sys.argv)
    s = Shortcuts(None)
    s.show()
    sys.exit(app.exec_())

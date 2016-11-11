# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
from PyQt5 import QtCore, QtWidgets


class Ui_ShortcutsUI(object):

    def setupUi(self, ShortcutsUI):
        ShortcutsUI.setObjectName("ShortcutsUI")
        ShortcutsUI.resize(579, 334)

        self.gridLayout = QtWidgets.QGridLayout(ShortcutsUI)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("verLayout")

        self.groupBox = QtWidgets.QGroupBox(ShortcutsUI)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setContentsMargins(11, 11, 11, 11)

        self.vLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.vLayout.setContentsMargins(11, 11, 11, 11)

        self.tableView = QtWidgets.QTableView()
        self.tableView.setContentsMargins(11, 11, 11, 11)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 0)
        self.vLayout.addWidget(self.tableView)

        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMaximumWidth(150)
        self.closeButton.setContentsMargins(11, 11, 11, 11)

        self.gridLayout.addWidget(self.closeButton, 4, 2)
        self.gridLayout.setSpacing(10)

        self.retranslateUi(ShortcutsUI)
        QtCore.QMetaObject.connectSlotsByName(ShortcutsUI)

    def retranslateUi(self, ShortcutsUI):
        _translate = QtCore.QCoreApplication.translate
        ShortcutsUI.setWindowTitle(_translate("ShortcutsUI", "Shortcuts"))
        self.groupBox.setTitle(_translate("ShortcutsUI", "Shortcuts list"))
        self.closeButton.setText(_translate("ShortcutsUI", "Close"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsUI(object):
    def setupUi(self, SettingsUI):
        SettingsUI.setObjectName("SettingsUI")
        SettingsUI.resize(579, 298)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SettingsUI)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(SettingsUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.autoSaveCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.autoSaveCheckBox.setChecked(True)
        self.autoSaveCheckBox.setObjectName("autoSaveCheckBox")
        self.gridLayout.addWidget(self.autoSaveCheckBox, 0, 0, 1, 1)
        self.autoArchiveCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.autoArchiveCheckBox.setChecked(True)
        self.autoArchiveCheckBox.setObjectName("autoArchiveCheckBox")
        self.gridLayout.addWidget(self.autoArchiveCheckBox, 1, 0, 1, 1)
        self.addCreatedDateCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.addCreatedDateCheckBox.setChecked(True)
        self.addCreatedDateCheckBox.setObjectName("addCreatedDateCheckBox")
        self.gridLayout.addWidget(self.addCreatedDateCheckBox, 2, 0, 1, 1)
        self.confirmCompletionCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.confirmCompletionCheckBox.setChecked(True)
        self.confirmCompletionCheckBox.setObjectName("confirmCompletionCheckBox")
        self.gridLayout.addWidget(self.confirmCompletionCheckBox, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(self.groupBox)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 9, 2, 1, 1)
        self.trayCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.trayCheckBox.setObjectName("trayCheckBox")
        self.gridLayout.addWidget(self.trayCheckBox, 6, 0, 1, 1)
        self.lowestPriorityLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lowestPriorityLineEdit.sizePolicy().hasHeightForWidth())
        self.lowestPriorityLineEdit.setSizePolicy(sizePolicy)
        self.lowestPriorityLineEdit.setMaximumSize(QtCore.QSize(16777212, 16777215))
        self.lowestPriorityLineEdit.setObjectName("lowestPriorityLineEdit")
        self.gridLayout.addWidget(self.lowestPriorityLineEdit, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 2, 1, 1)
        self.deleteActionCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.deleteActionCheckBox.setObjectName("deleteActionCheckBox")
        self.gridLayout.addWidget(self.deleteActionCheckBox, 4, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(SettingsUI)
        QtCore.QMetaObject.connectSlotsByName(SettingsUI)

    def retranslateUi(self, SettingsUI):
        _translate = QtCore.QCoreApplication.translate
        SettingsUI.setWindowTitle(_translate("SettingsUI", "SettingsUI"))
        self.groupBox.setTitle(_translate("SettingsUI", "QTodoTxt Settings"))
        self.autoSaveCheckBox.setText(_translate("SettingsUI", "Autosave"))
        self.autoArchiveCheckBox.setText(_translate("SettingsUI", "AutoArchive"))
        self.addCreatedDateCheckBox.setText(_translate("SettingsUI", "Add created date"))
        self.confirmCompletionCheckBox.setText(_translate("SettingsUI", "Ask for confirmation before task completion"))
        self.label.setText(_translate("SettingsUI", "Lowest task priority"))
        self.closeButton.setText(_translate("SettingsUI", "Close"))
        self.trayCheckBox.setText(_translate("SettingsUI", "Enable system tray (Require restart)"))
        self.lowestPriorityLineEdit.setText(_translate("SettingsUI", "D"))
        self.deleteActionCheckBox.setText(_translate("SettingsUI", "Show Delete action (Require restart)"))


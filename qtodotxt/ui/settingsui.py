# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsui.ui'
#
# Created: Thu Feb 25 10:23:26 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SettingsUI(object):
    def setupUi(self, SettingsUI):
        SettingsUI.setObjectName("SettingsUI")
        SettingsUI.resize(552, 309)
        self.horizontalLayout = QtGui.QHBoxLayout(SettingsUI)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(SettingsUI)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.autoSaveCheckBox = QtGui.QCheckBox(self.groupBox)
        self.autoSaveCheckBox.setChecked(True)
        self.autoSaveCheckBox.setObjectName("autoSaveCheckBox")
        self.gridLayout.addWidget(self.autoSaveCheckBox, 0, 0, 1, 1)
        self.autoArchiveCheckBox = QtGui.QCheckBox(self.groupBox)
        self.autoArchiveCheckBox.setChecked(True)
        self.autoArchiveCheckBox.setObjectName("autoArchiveCheckBox")
        self.gridLayout.addWidget(self.autoArchiveCheckBox, 1, 0, 1, 1)
        self.addCreatedDateCheckBox = QtGui.QCheckBox(self.groupBox)
        self.addCreatedDateCheckBox.setChecked(True)
        self.addCreatedDateCheckBox.setObjectName("addCreatedDateCheckBox")
        self.gridLayout.addWidget(self.addCreatedDateCheckBox, 2, 0, 1, 1)
        self.hideFutureTasksCheckBox = QtGui.QCheckBox(self.groupBox)
        self.hideFutureTasksCheckBox.setChecked(False)
        self.hideFutureTasksCheckBox.setObjectName("hideFutureTasksCheckBox")
        self.gridLayout.addWidget(self.hideFutureTasksCheckBox, 3, 0, 1, 1)
        self.confirmCompletionCheckBox = QtGui.QCheckBox(self.groupBox)
        self.confirmCompletionCheckBox.setChecked(True)
        self.confirmCompletionCheckBox.setObjectName("confirmCompletionCheckBox")
        self.gridLayout.addWidget(self.confirmCompletionCheckBox, 4, 0, 1, 2)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.lowestPriorityLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lowestPriorityLineEdit.sizePolicy().hasHeightForWidth())
        self.lowestPriorityLineEdit.setSizePolicy(sizePolicy)
        self.lowestPriorityLineEdit.setMaximumSize(QtCore.QSize(16777212, 16777215))
        self.lowestPriorityLineEdit.setObjectName("lowestPriorityLineEdit")
        self.gridLayout.addWidget(self.lowestPriorityLineEdit, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 80, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 2, 1, 1)
        self.closeButton = QtGui.QPushButton(self.groupBox)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 7, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(SettingsUI)
        QtCore.QMetaObject.connectSlotsByName(SettingsUI)

    def retranslateUi(self, SettingsUI):
        SettingsUI.setWindowTitle(QtGui.QApplication.translate("SettingsUI", "SettingsUI", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SettingsUI", "QTodoTxt Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.autoSaveCheckBox.setText(QtGui.QApplication.translate("SettingsUI", "Autosave", None, QtGui.QApplication.UnicodeUTF8))
        self.autoArchiveCheckBox.setText(QtGui.QApplication.translate("SettingsUI", "AutoArchive", None, QtGui.QApplication.UnicodeUTF8))
        self.addCreatedDateCheckBox.setText(QtGui.QApplication.translate("SettingsUI", "Add created date", None, QtGui.QApplication.UnicodeUTF8))
        self.hideFutureTasksCheckBox.setText(QtGui.QApplication.translate("SettingsUI", "Add future tasks", None, QtGui.QApplication.UnicodeUTF8))
        self.confirmCompletionCheckBox.setText(QtGui.QApplication.translate("SettingsUI", "Ask for confirmation before task completion", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsUI", "Lowest task priority", None, QtGui.QApplication.UnicodeUTF8))
        self.lowestPriorityLineEdit.setText(QtGui.QApplication.translate("SettingsUI", "D", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("SettingsUI", "Close", None, QtGui.QApplication.UnicodeUTF8))


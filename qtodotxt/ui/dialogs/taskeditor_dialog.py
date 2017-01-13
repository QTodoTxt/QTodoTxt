import sys
from PyQt5 import QtWidgets, QtCore
from qtodotxt.ui.dialogs.taskeditor_lineedit import TaskEditorLineEdit


class TaskEditorDialog(QtWidgets.QDialog):

    def __init__(self, parent, mfile):
        QtWidgets.QDialog.__init__(self)
        self._mfile = mfile
        self._initUI()
        #self.setWindowFlags(QtCore.Qt.Dialog
                            #| QtCore.Qt.MSWindowsFixedSizeDialogHint
                            #| QtCore.Qt.WindowStaysOnBottomHint
                            #| QtCore.Qt.WindowSystemMenuHint
                            #| QtCore.Qt.WindowTitleHint
                            #| QtCore.Qt.WindowCloseButtonHint)

    def _initUI(self):
        self.setWindowTitle("Task Editor")
        vbox = QtWidgets.QVBoxLayout()

        self._label = QtWidgets.QLabel("Task:")
        vbox.addWidget(self._label)

        self._edit = TaskEditorLineEdit(self, self._mfile)
        vbox.addWidget(self._edit)

        hbox = QtWidgets.QHBoxLayout()
        okButton = QtWidgets.QPushButton("Ok")
        okButton.clicked.connect(self.accept)
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(500, 100)

    def textValue(self):
        return self._edit.text()

    def setTextValue(self, text):
        self._edit.setText(text)

    def setLabelText(self, text):
        self._label.setText(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    values = ['(A)', '(B)', '(C)', '@home', '@call', '@work', '+qtodotxt', '+sqlvisualizer']
    view = TaskEditorDialog(values)
    view.show()
    sys.exit(app.exec_())

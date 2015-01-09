import sys
from PySide import QtGui, QtCore
from qtodotxt.ui.controls.autocomplete_multilineedit import AutoCompleteMultilineEdit
from qtodotxt.ui.controls.autocomplete_lineedit import AutoCompleteEdit


class AutoCompleteInputDialog(QtGui.QDialog):
    def __init__(self, values, parent=None, multilineTasks=False):
        super(AutoCompleteInputDialog, self).__init__(parent)
        self._multilineTasks = multilineTasks
        self._initUI(values)

    def _initUI(self, values):
        self.setWindowTitle("Task Editor")
        vbox = QtGui.QVBoxLayout()

        self._label = QtGui.QLabel("Task:")
        vbox.addWidget(self._label)

        if self._multilineTasks:
            self._edit = AutoCompleteMultilineEdit(values)
        else:
            self._edit = AutoCompleteEdit(values)
        
        vbox.addWidget(self._edit)

        hbox = QtGui.QHBoxLayout()
        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(self.accept)
        cancelButton = QtGui.QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(500, 100)
        
        """ select OK on CTRL + Return """
        shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Return'), self)
        self.connect(shortcut, QtCore.SIGNAL('activated()'), self.accept)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Enter'), self)
        self.connect(shortcut, QtCore.SIGNAL('activated()'), self.accept)


    def textValue(self):
        return self._edit.toTaskText()

    def setTextValue(self, text):
        self._edit.setTaskText(text)

    def setLabelText(self, text):
        self._label.setText(text)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    values = ['(A)', '(B)', '(C)', '@home', '@call', '@work', '+qtodotxt', '+sqlvisualizer']
    view = AutoCompleteInputDialog(values)
    view.show()
    sys.exit(app.exec_())  

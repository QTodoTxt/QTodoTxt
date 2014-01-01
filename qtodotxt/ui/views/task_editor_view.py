import sys
from PySide import QtCore
from PySide import QtGui

class TaskEditorView(QtGui.QDialog):
    def __init__(self):
        super(TaskEditorView, self).__init__()
        self._initUI()

    def _initUI(self):
        self._edit = QtGui.QLineEdit()
        self.setWindowTitle("Task Editor")
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(QtGui.QLabel("Task:"))
        vbox.addWidget(self._edit)
        
        hbox = QtGui.QHBoxLayout()
        okButton = QtGui.QPushButton("Ok")
        cancelButton = QtGui.QPushButton("Cancel")
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(500, 100)

        self._completer = QtGui.QCompleter(['+one', '+two', '+three'])
        self._edit.setCompleter(self._completer)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    view = TaskEditorView()
    view.show()
    sys.exit(app.exec_())
    
    


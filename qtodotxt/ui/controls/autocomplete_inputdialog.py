import sys
from PySide import QtGui
from qtodotxt.ui.controls.autocomplete_lineedit import AutoCompleteEdit
from datetime import date, timedelta

class AutoCompleteInputDialog(QtGui.QDialog):

    autocomplete_pairs = {'due:EndOfWeek': '',
                          'due:EndOfMonth': '',
                          'due:EndOfYear': '',
                          'due:Today': '',
                          'due:Tomorrow': ''}

    def __init__(self, values, parent=None):
        super(AutoCompleteInputDialog, self).__init__(parent)
        self._initUI(values)
        self._populateKeys(self.autocomplete_pairs)

    def _populateKeys(self, keys):
        today = 'due:' + date.today().strftime('%Y-%m-%d')
        tomorrow = 'due:' + (date.today() + timedelta(days = 1)).strftime('%Y-%m-%d')
        EOW = 'due:' + (date.today() + timedelta((6-date.today().weekday()) % 7)).strftime('%Y-%m-%d')
        EOM = 'due:' + (date.today().replace(month=date.today().month+1, day=1) - timedelta(days=1)).strftime('%Y-%m-%d')
        EOY = 'due:' + (date.today().replace(year=date.today().year+1, month=1, day=1) - timedelta(days=1)).strftime('%Y-%m-%d')

        keys['due:EndOfWeek'] = EOW
        keys['due:EndOfMonth'] = EOM
        keys['due:EndOfYear'] = EOY
        keys['due:Today'] = today
        keys['due:Tomorrow'] = tomorrow
        return keys

    def _initUI(self, values):
        self.setWindowTitle("Task Editor")
        vbox = QtGui.QVBoxLayout()

        self._label = QtGui.QLabel("Task:")
        vbox.addWidget(self._label)

        self._edit = AutoCompleteEdit(values, self.autocomplete_pairs)
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

    def textValue(self):
        return self._edit.text()

    def setTextValue(self, text):
        self._edit.setText(text)

    def setLabelText(self, text):
        self._label.setText(text)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    values = ['(A)', '(B)', '(C)', '@home', '@call', '@work', '+qtodotxt', '+sqlvisualizer']
    view = AutoCompleteInputDialog(values)
    view.show()
    sys.exit(app.exec_())  

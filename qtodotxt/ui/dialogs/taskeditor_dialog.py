import sys
from PyQt5 import QtWidgets
from qtodotxt.ui.dialogs.taskeditor_lineedit import TaskEditorLineEdit
from datetime import date, timedelta
import collections


class TaskEditorDialog(QtWidgets.QDialog):
    autocomplete_pairs = collections.OrderedDict([
        ('due:Today', ''),
        ('due:Tomorrow', ''),
        ('due:EndOfWeek', ''),
        ('due:EndOfNextWeek', ''),
        ('due:EndOfMonth', ''),
        ('due:EndOfNextMonth', ''),
        ('due:EndOfYear', ''),
        ('due:January', ''),
        ('due:February', ''),
        ('due:March', ''),
        ('due:April', ''),
        ('due:May', ''),
        ('due:June', ''),
        ('due:July', ''),
        ('due:August', ''),
        ('due:September', ''),
        ('due:October', ''),
        ('due:November', ''),
        ('due:December', '')
    ])

    def __init__(self, values, parent=None):
        super(TaskEditorDialog, self).__init__(parent)
        self._initUI(values)
        self._populateKeys(self.autocomplete_pairs)

    def _endOfMonth(self, month):
        today = date.today()
        month = month + 1
        year = today.year
        if month > 12:
            month = month - 12
            year += 1
        if month <= today.month:
            year += 1
        eom = date(year=year, month=month, day=1) - timedelta(days=1)
        return eom.isoformat()

    def _populateKeys(self, keys):
        today = 'due:' + date.today().isoformat()
        tomorrow = 'due:' + (date.today() + timedelta(days=1)).isoformat()
        EOW = 'due:' + (date.today() + timedelta((6 - date.today().weekday()) % 7)).isoformat()
        EONW = 'due:' + (date.today() + timedelta((13 - date.today().weekday()) % 14)).isoformat()
        EOM = 'due:' + self._endOfMonth(date.today().month)
        EONM = 'due:' + self._endOfMonth(date.today().month + 1)
        EOY = 'due:' + (date(year=date.today().year + 1, month=1, day=1) - timedelta(days=1)).isoformat()

        keys['due:EndOfWeek'] = EOW
        keys['due:EndOfNextWeek'] = EONW
        keys['due:EndOfMonth'] = EOM
        keys['due:EndOfNextMonth'] = EONM
        keys['due:EndOfYear'] = EOY
        keys['due:Today'] = today
        keys['due:Tomorrow'] = tomorrow
        keys['due:January'] = "due:" + self._endOfMonth(1)
        keys['due:February'] = "due:" + self._endOfMonth(2)
        keys['due:March'] = "due:" + self._endOfMonth(3)
        keys['due:April'] = "due:" + self._endOfMonth(4)
        keys['due:May'] = "due:" + self._endOfMonth(5)
        keys['due:June'] = "due:" + self._endOfMonth(6)
        keys['due:July'] = "due:" + self._endOfMonth(7)
        keys['due:August'] = "due:" + self._endOfMonth(8)
        keys['due:September'] = "due:" + self._endOfMonth(9)
        keys['due:October'] = "due:" + self._endOfMonth(10)
        keys['due:November'] = "due:" + self._endOfMonth(11)
        keys['due:December'] = "due:" + self._endOfMonth(12)
        return keys

    def _initUI(self, values):
        self.setWindowTitle("Task Editor")
        vbox = QtWidgets.QVBoxLayout()

        self._label = QtWidgets.QLabel("Task:")
        vbox.addWidget(self._label)

        self._edit = TaskEditorLineEdit(values, self.autocomplete_pairs)
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

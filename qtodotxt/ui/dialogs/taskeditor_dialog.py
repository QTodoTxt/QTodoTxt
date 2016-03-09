import sys
from PyQt5 import QtWidgets
from qtodotxt.ui.dialogs.taskeditor_lineedit import TaskEditorLineEdit
from datetime import date, timedelta
import collections
import calendar
from dateutil.relativedelta import relativedelta


def end_of_month(today=None, month=None):
    if today is None:
        today = date.today()
    if month is None:
        month = today.month
    year = today.year
    if month < today.month:
        year += 1
    eom = date(year=year, month=month, day=calendar.monthrange(year, month)[1])
    return eom.isoformat()


def end_of_next_month(today=None):
    if today is None:
        today = date.today()
    today += relativedelta(months=1)
    eom = date(year=today.year, month=today.month, day=calendar.monthrange(today.year, today.month)[1])
    return eom.isoformat()


def end_of_week(day=None):
    if day is None:
        day = date.today()
    return (day + timedelta((6 - day.weekday()) % 7)).isoformat()


def end_of_next_week(day=None):
    if day is None:
        day = date.today()
    return (day + timedelta((13 - day.weekday()) % 14)).isoformat()


def end_of_year(day=None):
    if day is None:
        day = date.today()
    return (date(year=day.year + 1, month=1, day=1) - timedelta(days=1)).isoformat()


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
        ('t:Today', ''),
        ('t:Tomorrow', ''),
        ('t:EndOfWeek', ''),
        ('t:EndOfNextWeek', ''),
        ('t:EndOfMonth', ''),
        ('t:EndOfNextMonth', ''),
        ('t:EndOfYear', ''),
        ('due:December', '')
    ])

    def __init__(self, values, parent=None):
        super(TaskEditorDialog, self).__init__(parent)
        self._initUI(values)
        self._populateKeys(self.autocomplete_pairs)

    def _populateKeys(self, keys):
        self._populateDues(keys)
        self._populateThresholds(keys)

    def _populateThresholds(self, keys):
        keys['t:Today'] = 't:' + date.today().isoformat()
        keys['t:Tomorrow'] = 't:' + (date.today() + timedelta(days=1)).isoformat()
        keys['t:EndOfWeek'] = 't:' + end_of_week()
        keys['t:EndOfNextWeek'] = 't:' + end_of_next_week()
        keys['t:EndOfMonth'] = 't:' + end_of_month()
        keys['t:EndOfNextMonth'] = 't:' + end_of_next_month()
        keys['t:EndOfYear'] = 't:' + end_of_year()

    def _populateDues(self, keys):
        keys['due:Today'] = 'due:' + date.today().isoformat()
        keys['due:Tomorrow'] = 'due:' + (date.today() + timedelta(days=1)).isoformat()
        keys['due:EndOfWeek'] = 'due:' + end_of_week()
        keys['due:EndOfNextWeek'] = 'due:' + end_of_next_week()
        keys['due:EndOfMonth'] = 'due:' + end_of_month()
        keys['due:EndOfNextMonth'] = 'due:' + end_of_next_month()
        keys['due:EndOfYear'] = 'due:' + end_of_year()
        keys['due:January'] = "due:" + end_of_month(month=1)
        keys['due:February'] = "due:" + end_of_month(month=2)
        keys['due:March'] = "due:" + end_of_month(month=3)
        keys['due:April'] = "due:" + end_of_month(month=4)
        keys['due:May'] = "due:" + end_of_month(month=5)
        keys['due:June'] = "due:" + end_of_month(month=6)
        keys['due:July'] = "due:" + end_of_month(month=7)
        keys['due:August'] = "due:" + end_of_month(month=8)
        keys['due:September'] = "due:" + end_of_month(month=9)
        keys['due:October'] = "due:" + end_of_month(month=10)
        keys['due:November'] = "due:" + end_of_month(month=11)
        keys['due:December'] = "due:" + end_of_month(month=12)

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

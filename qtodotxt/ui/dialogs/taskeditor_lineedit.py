from PyQt5 import QtCore, QtGui, QtWidgets


class TaskEditorLineEdit(QtWidgets.QLineEdit):
    def __init__(self, model, autocomplete_pairs, separator=' '):
        super(TaskEditorLineEdit, self).__init__()
        self._separator = separator
        self._autocomplete_pairs = autocomplete_pairs
        self._completer = QtWidgets.QCompleter(model)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._completer.activated.connect(self._insertCompletion)
        self._keysToIgnore = [QtCore.Qt.Key_Enter,
                              QtCore.Qt.Key_Return,
                              QtCore.Qt.Key_Escape,
                              QtCore.Qt.Key_Tab]

    def _insertCompletion(self, completion):
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        currentText = self.text()
        completionPrefixSize = len(self._completer.completionPrefix())
        textFirstPart = self.cursorPosition() - completionPrefixSize
        textLastPart = textFirstPart + completionPrefixSize

        if completion in self._autocomplete_pairs:
            completion = self.replaceAutocompleteKeys(completion)

        newtext = currentText[:textFirstPart] + completion + " " + currentText[textLastPart:]
        newCursorPos = self.cursorPosition() + (len(completion) - completionPrefixSize) + 1

        self.setText(newtext)
        self.setCursorPosition(newCursorPos)

    def replaceAutocompleteKeys(self, completion):
        if completion in self._autocomplete_pairs.keys():
            return self._autocomplete_pairs[completion]

    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1
        while i >= 0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(TaskEditorLineEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()
        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)
        if len(event.text()) > 0 and len(completionPrefix) > 0:
            if event.key() not in self._keysToIgnore:
                self._completer.complete()
        if len(completionPrefix) == 0:
            self._completer.popup().hide()

    def _updateCompleterPopupItems(self, completionPrefix):
        """
        Filters the completer's popup items to only show items
        with the given prefix.
        """
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0))

if __name__ == '__main__':
    def demo():
        import sys
        app = QtGui.QApplication(sys.argv)
        values = ['@call', '@bug', '+qtodotxt', '+sqlvisualizer']
        editor = TaskEditorLineEdit(values)
        window = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(editor)
        window.setLayout(hbox)
        window.show()

        sys.exit(app.exec_())

    demo()

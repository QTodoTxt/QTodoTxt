from PySide import QtCore, QtGui
from PySide.QtGui import QFontMetrics, QSizePolicy


class AutoCompleteMultilineEdit(QtGui.QPlainTextEdit):
    def __init__(self, model, separator=' '):
        super(AutoCompleteMultilineEdit, self).__init__()
        self._separator = separator
        self._completer = QtGui.QCompleter(model)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        fm = QFontMetrics(self.font())
        textHeight = fm.height() + 5
        #self.setFixedHeight(textHeight)
        self.heightMin = 0
        self.heightMax = 65000
        #self.document().contentsChanged.connect(self.sizeChange)
        self.connect(
            self._completer,
            QtCore.SIGNAL('activated(QString)'),
            self._insertCompletion)
        self._keysToIgnore = [QtCore.Qt.Key_Enter,
                              QtCore.Qt.Key_Return,
                              QtCore.Qt.Key_Escape,
                              QtCore.Qt.Key_Tab]

    def setTaskText(self, text):
        # Replace \\ with newlines
        text = text.replace(r' \\ ','\n')
        return super(AutoCompleteMultilineEdit, self).setPlainText(text)
    
    def toTaskText(self):
        # Replace newlines AutoCompleteMultilineEdit \\
        text = super(AutoCompleteMultilineEdit, self).toPlainText()
        text = text.rstrip() # trailing empty lines cause issues
        text = text.replace('\n',r' \\ ')
        return text
    
    def _insertCompletion(self, completion):
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        currentText = self.toPlainText()
        completionPrefixSize = len(self._completer.completionPrefix())
        textFirstPart = self.textCursor().position() - completionPrefixSize
        textLastPart = textFirstPart + completionPrefixSize
        newtext = currentText[:textFirstPart] + completion + " " + currentText[textLastPart:]
        newCursorPos = self.textCursor().position() + (len(completion) - completionPrefixSize) + 1
        
        """ Insert text an reposition cursor after text """
        self.setPlainText(newtext)
        currentCursor = self.textCursor()
        currentCursor.setPosition(newCursorPos)
        self.setTextCursor(currentCursor)

    def textUnderCursor(self):
        text = self.toPlainText()
        textUnderCursor = ''
        i = self.textCursor().position() - 1
        while i >= 0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event):
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(AutoCompleteMultilineEdit, self).keyPressEvent(event)
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

    def sizeChange(self):
        fm = QFontMetrics(self.font())
        textHeight = fm.height() + 5
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setFixedHeight(textHeight*docHeight)

if __name__ == '__main__':
    def demo():
        import sys
        app = QtGui.QApplication(sys.argv)
        values = ['@call', '@bug', '+qtodotxt', '+sqlvisualizer']
        editor = AutoCompleteMultilineEdit(values)
        window = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(editor)
        window.setLayout(hbox)
        window.show()

        sys.exit(app.exec_())

    demo()
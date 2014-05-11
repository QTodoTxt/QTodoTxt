from PySide import QtCore, QtGui


class FilterTasksView(QtGui.QLineEdit):

    filterTextChanged = QtCore.Signal(str)

    def __init__(self, searchIcon, clearIcon, parent=None):
        QtGui.QLineEdit.__init__(self, parent)

        self._text = ""

        self.clearButton = QtGui.QToolButton(self)
        self.clearButton.setIcon(clearIcon)
        self.clearButton.setCursor(QtCore.Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.updateText)

        self.searchButton = QtGui.QToolButton(self)
        self.searchButton.setIcon(searchIcon)
        self.searchButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonWidth = self.clearButton.sizeHint().width()
        self.setStyleSheet("QLineEdit { padding-left: %spx; padding-right: %spx; } " % (
            self.searchButton.sizeHint().width() + frameWidth + 1, buttonWidth + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(),
                                self.searchButton.sizeHint().width() + buttonWidth + frameWidth * 2 + 2),
                            max(msz.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2))
        self.setPlaceholderText("filter")

        focusShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
        focusShortcut.activated.connect(self.setFocus)

    def resizeEvent(self, event):
        sz = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(),
                              (self.rect().bottom() + 1 - sz.height()) / 2)
        self.searchButton.move(self.rect().left() + 1, (self.rect().bottom() + 1 - sz.height()) / 2)

    def getText(self):
        return self._text

    def updateText(self, text):
        self._text = text
        self.filterTextChanged.emit(text)
        self.updateCloseButton(bool(text))

    def updateCloseButton(self, visible):
            self.clearButton.setVisible(visible)

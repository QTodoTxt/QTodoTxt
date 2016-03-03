from PyQt5 import QtCore, QtGui, QtWidgets


class TasksSearchView(QtWidgets.QLineEdit):

    searchTextChanged = QtCore.pyqtSignal(str)

    def __init__(self, searchIcon, clearIcon, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)

        self._searchText = ""

        self.clearButton = QtWidgets.QToolButton(self)
        self.clearButton.setIcon(clearIcon)
        self.clearButton.setCursor(QtCore.Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.updateSearchText)

        self.searchButton = QtWidgets.QToolButton(self)
        self.searchButton.setIcon(searchIcon)
        self.searchButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        buttonWidth = self.clearButton.sizeHint().width()
        self.setStyleSheet("QLineEdit { padding-left: %spx; padding-right: %spx; } " % (
            self.searchButton.sizeHint().width() + frameWidth + 1, buttonWidth + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(),
                                self.searchButton.sizeHint().width() + buttonWidth + frameWidth * 2 + 2),
                            max(msz.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2))
        self.setPlaceholderText("Search")

        focusShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), self)
        focusShortcut.activated.connect(self.setFocus)

    def resizeEvent(self, event):
        sz = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(),
                              (self.rect().bottom() + 1 - sz.height()) / 2)
        self.searchButton.move(self.rect().left() + 1, (self.rect().bottom() + 1 - sz.height()) / 2)

    def getSearchText(self):
        return self._searchText

    def updateSearchText(self, searchText):
        self._searchText = searchText
        self.searchTextChanged.emit(searchText)
        self.updateCloseButton(bool(searchText))

    def updateCloseButton(self, visible):
            self.clearButton.setVisible(visible)

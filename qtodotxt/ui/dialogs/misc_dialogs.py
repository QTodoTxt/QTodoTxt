from PyQt5 import QtGui


class Dialogs(object):

    def __init__(self, parent_window, default_title):
        self._parent_window = parent_window
        self._default_title = default_title

    def showMessage(self, message, title=None):
        if not title:
            title = self._default_title

        QtGui.QMessageBox.information(self._parent_window, title, message)

    def showError(self, message, title=None):
        if not title:
            title = self._default_title + ' - Error'

        QtGui.QMessageBox.critical(self._parent_window, title, message)

    def showSaveDiscardCancel(self, message):
        """
        Returns:
            QtGui.QMessageBox.Save or
            QtGui.QMessageBox.Discard or
            QtGui.QMessageBox.Cancel
        """
        dialog = QtGui.QMessageBox(self._parent_window)
        dialog.setWindowTitle('%s - Confirm' % self._default_title)
        dialog.setText(message)
        dialog.setStandardButtons(
            QtGui.QMessageBox.Save |
            QtGui.QMessageBox.Discard |
            QtGui.QMessageBox.Cancel)
        return dialog.exec_()

    def showConfirm(self, message):
        result = QtGui.QMessageBox.question(
            self._parent_window,
            '%s - Confirm' % self._default_title,
            message,
            buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            defaultButton=QtGui.QMessageBox.Yes)

        return result == QtGui.QMessageBox.Yes

if __name__ == "__main__":
    app = QtGui.QApplication([])
    service = Dialogs(None, 'Default Title')
    service.showMessage("DialogsService.message()")
    service.showError("DialogsService.error()")
    result = service.showSaveDiscardCancel("Unsaved changes...")
    message = 'You clicked '
    if result == QtGui.QMessageBox.Save:
        message += '"Save"'
    elif result == QtGui.QMessageBox.Discard:
        message += '"Discard"'
    else:
        message += '"Cancel"'
    service.showMessage(message)
    service.showConfirm('Sure?')

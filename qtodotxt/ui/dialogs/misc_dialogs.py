from PyQt5 import QtWidgets, QtCore


class Dialogs(object):

    def __init__(self, parent_window, default_title):
        self._parent_window = parent_window
        self._default_title = default_title

    def showMessage(self, message, title=None):
        if not title:
            title = self._default_title
        QtWidgets.QMessageBox.information(self._parent_window, title, message)

    def showError(self, message, title=None):
        if not title:
            title = self._default_title + ' - Error'
        QtWidgets.QMessageBox.critical(self._parent_window, title, message)

    def showSaveDiscardCancel(self, message):
        """
        Returns:
            QtWidgets.QMessageBox.Save or
            QtWidgets.QMessageBox.Discard or
            QtWidgets.QMessageBox.Cancel
        """
        dialog = QtWidgets.QMessageBox(self._parent_window)
        dialog.setWindowTitle('%s - Confirm' % self._default_title)
        dialog.setText(message)
        dialog.setStandardButtons(
            QtWidgets.QMessageBox.Save |
            QtWidgets.QMessageBox.Discard |
            QtWidgets.QMessageBox.Cancel)
        return dialog.exec_()

    def showConfirm(self, message):
        result = QtWidgets.QMessageBox.question(
            self._parent_window,
            '%s - Confirm' % self._default_title,
            message,
            buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            defaultButton=QtWidgets.QMessageBox.Yes)
        return result == QtWidgets.QMessageBox.Yes


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    _tr = QtCore.QCoreApplication.translate
    service = Dialogs(None, 'Default Title')
    service.showMessage("DialogsService.message()")
    service.showError("DialogsService.error()")
    result = service.showSaveDiscardCancel(_tr("misc_dialog", "Unsaved changes..."))
    message = _tr("misc_dialog", 'You clicked ')
    if result == QtWidgets.QMessageBox.Save:
        message += _tr("misc_dialog", '"Save"')
    elif result == QtWidgets.QMessageBox.Discard:
        message += _tr("misc_dialog", '"Discard"')
    else:
        message += _tr("misc_dialog", '"Cancel"')
    service.showMessage(message)
    service.showConfirm(_tr("misc_dialog", 'Sure?'))

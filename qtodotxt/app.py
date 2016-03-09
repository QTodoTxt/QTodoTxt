#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from qtodotxt.ui.controllers.main_controller import MainController
from qtodotxt.ui.dialogs.misc_dialogs import Dialogs
from qtodotxt.ui.dialogs.taskeditor import TaskEditor
from qtodotxt.ui.resource_manager import getIcon
from qtodotxt.ui.views.main_view import MainView


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, main_controller):
        self._controller = main_controller
        self._initIcon()

    def _initIcon(self):
        view = self._controller.getView()
        icon = getIcon('qtodotxt.png')
        QtWidgets.QSystemTrayIcon.__init__(self, icon, view)
        self.activated.connect(self._onActivated)
        self.setToolTip('QTodoTxt')

    def _onActivated(self):
        self._controller._tasks_list_controller.createTask()


def _parseArgs():
    if len(sys.argv) > 1 and sys.argv[1].startswith('-psn'):
        del sys.argv[1]
    parser = argparse.ArgumentParser(description='QTodoTxt')
    parser.add_argument('file', type=str, nargs='?', metavar='TEXTFILE',
                        help='open the specified file')
    parser.add_argument('-q', '--quickadd', action='store_true',
                        help='opens the add task dialog and exit the application when done')
    parser.add_argument('-l', '--loglevel', type=str, nargs=1, metavar='LOGLEVEL', default=['WARN'],
                        choices=['DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'CRITICAL'],
                        help='set one of these logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    return parser.parse_args()


def _setupLogging(loglevel):
    numeric_level = getattr(logging, loglevel[0].upper(), None)
    if isinstance(numeric_level, int):
        logging.basicConfig(format='{asctime}.{msecs:.0f} [{name}] {levelname}: {message}',
                            level=numeric_level, style='{', datefmt='%H:%M:%S')


def _createController(args):
    window = MainView()
    dialogs = Dialogs(window, 'QTodoTxt')
    taskeditor = TaskEditor(window)
    return MainController(window, dialogs, taskeditor, args)


def run():
    # First set some application settings for QSettings
    QtCore.QCoreApplication.setOrganizationName("QTodoTxt")
    QtCore.QCoreApplication.setApplicationName("QTodoTxt")
    # Now set up our application and start
    app = QtWidgets.QApplication(sys.argv)
    args = _parseArgs()
    _setupLogging(args.loglevel)
    #    logger = logging.getLogger(__file__[:-3]) # in case someone wants to log here
    controller = _createController(args)
    controller.show()
    if int(QtCore.QSettings().value("enable_tray", 0)):
        icon = TrayIcon(controller)
        icon.show()
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    run()

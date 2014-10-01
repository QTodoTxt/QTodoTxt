#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from PySide import QtGui
from qtodotxt.ui.controllers import MainController
from qtodotxt.ui.resource_manager import getIcon
from qtodotxt.ui.services.dialogs_service import DialogsService
from qtodotxt.ui.services.task_editor_service import TaskEditorService
from qtodotxt.ui.views import MainView


class TrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, main_controller):
        self._controller = main_controller
        self._initIcon()

    def _initIcon(self):
        view = self._controller.getView()
        icon = getIcon('qtodotxt.png')
        QtGui.QSystemTrayIcon.__init__(self, icon, view)
        self.activated.connect(self._onActivated)
        self.setToolTip('QTodoTxt')

    def _onActivated(self):
        self._controller._tasks_list_controller.createTask()

def _parseArgs():
    if len(sys.argv) > 1 and sys.argv[1].startswith('-psn'):
        del sys.argv[1]
    parser = argparse.ArgumentParser(description='QTodoTxt')
    parser.add_argument('-f', '--file', type=str, nargs=1, metavar='TEXTFILE',
                        help='open the specified file')
    parser.add_argument('-q', '--quickadd', action='store_true',
                        help='opens the add task dialog and exit the application when done')
    parser.add_argument('-l', '--loglevel', type=str, nargs=1, metavar='LOGLEVEL', default=['NOTSET'],
                        choices=['DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'CRITICAL'],
                        help='set one of these logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    return parser.parse_args()

def _setupLogging(loglevel):
    loglevel = logging._nameToLevel[loglevel[0]]
    if loglevel:
        logging.basicConfig(format='{asctime}.{msecs:.0f} [{name}] {levelname}: {message}',
                            level=loglevel, style='{', datefmt='%H:%M:%S')

def _createController(args):
    window = MainView()
    dialogs_service = DialogsService(window, 'QTodoTxt')
    task_editor_service = TaskEditorService(window)
    return MainController(window, dialogs_service, task_editor_service, args)

def run():
    app = QtGui.QApplication(sys.argv)
    args = _parseArgs()
    _setupLogging(args.loglevel)
#    logger = logging.getLogger(__file__[:-3]) # in case someone wants to log here
    controller = _createController(args)
    icon = TrayIcon(controller)
    controller.show()
    icon.show()
    app.exec_()
    sys.exit()

if __name__ == "__main__":
    run()

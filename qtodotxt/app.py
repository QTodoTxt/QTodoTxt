#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import os

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
# import resource for darkstyle
# taken from https://github.com/ColinDuquesnoy/QDarkStyleSheet
import qtodotxt.ui.resources.pyqt5_style_rc  # noqa: F401
import qtodotxt.ui.resources.qTodoTxt_style_rc  # noqa: F401
import qtodotxt.ui.resources.qTodoTxt_dark_style_rc  # noqa: F401

from qtodotxt.ui.controllers.main_controller import MainController
from qtodotxt.ui.dialogs.misc_dialogs import Dialogs
from qtodotxt.ui.dialogs.taskeditor import TaskEditor
from qtodotxt.ui.views.main_view import MainView
from qtodotxt.lib.file import FileObserver
from qtodotxt.lib.tendo_singleton import SingleInstance


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, main_controller):
        self._controller = main_controller
        self.style = ":/white_icons"
        if str(QtCore.QSettings().value("color_schem", "")).find("dark") >= 0:
            self.style = ":/dark_icons"
        self._initIcon()

    def _initIcon(self):
        view = self._controller.getView()

        icon = QtGui.QIcon(self.style + "/resources/qtodotxt.png")
        QtWidgets.QSystemTrayIcon.__init__(self, icon, view)
        self.activated.connect(self._onActivated)
        self.setToolTip('QTodoTxt')

        menu = QtWidgets.QMenu(self._controller.view)
        create_task_action = menu.addAction(QtGui.QIcon(self.style + "/resources/TaskCreate.png"),
                                            self.tr("Create New Task"))
        create_task_action.triggered.connect(self._createTask)
        toggle_visible_action = menu.addAction(self.tr("Show/Hide Window"))
        toggle_visible_action.triggered.connect(self._controller.toggleVisible)
        exit_action = menu.addAction(QtGui.QIcon(self.style + '/resources/ApplicationExit.png'), self.tr("Exit"))
        exit_action.triggered.connect(self._controller.exit)
        self.setContextMenu(menu)

    def _onActivated(self, activation_reason):
        # Tray Icon has been activated.
        # [0] QSystemTrayIcon.Unknown       Unknown reason
        # [1] QSystemTrayIcon.Context       The context menu for the system tray entry was requested
        # [2] QSystemTrayIcon.DoubleClick   The system tray entry was double clicked
        # [3] QSystemTrayIcon.Trigger       The system tray entry was clicked
        # [4] QSystemTrayIcon.MiddleClick   The system tray entry was clicked with the middle mouse button
        if activation_reason == QtWidgets.QSystemTrayIcon.Trigger:
            if (int(QtCore.QSettings().value("enable_tray", 0)) and
                    int(QtCore.QSettings().value("hide_to_tray", 0))):
                self._controller.toggleVisible()
            else:
                self._createTask()

    def _createTask(self):

        self._controller.view.show()
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


def setupAnotherInstanceEvent(controller, dir):
    fileObserver = FileObserver(controller, dir)
    fileObserver.addPath(dir)
    fileObserver.dirChangetSig.connect(controller.anotherInstanceEvent)


def setupSingleton(args, me):
    dir = os.path.dirname(sys.argv[0])
    tempFileName = dir + "/qtodo.tmp"
    if me.initialized is True:
        if os.path.isfile(tempFileName):
            os.remove(tempFileName)
    else:
        f = open(tempFileName, 'w')
        if args.quickadd is False:
            f.write("1")
        if args.quickadd is True:
            f.write("2")
        f.flush()
        f.close()
        sys.exit(-1)


def run():
    # First set some application settings for QSettings
    QtCore.QCoreApplication.setOrganizationName("QTodoTxt")
    QtCore.QCoreApplication.setApplicationName("QTodoTxt")
    # Now set up our application and start
    app = QtWidgets.QApplication(sys.argv)

    name = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    if translator.load(str(name) + ".qm", "..//i18n"):
        app.installTranslator(translator)

    args = _parseArgs()

    dir = os.path.dirname(sys.argv[0])
    needSingleton = QtCore.QSettings().value("singleton", 0)

    # clear or write to TMP file, of main instance
    if int(needSingleton):
        me = SingleInstance()
        setupSingleton(args, me)

    _setupLogging(args.loglevel)
    #    logger = logging.getLogger(__file__[:-3]) # in case someone wants to log here
    controller = _createController(args)

    # Connecting to a processor reading TMP file
    if needSingleton:
        setupAnotherInstanceEvent(controller, dir)

    controller.show()
    if int(QtCore.QSettings().value("enable_tray", 0)):
        # If the controller.show() method is not called, the todo.txt file
        #  is not loaded.  If the controller.show() method is modified to do the
        #  initial setup but not show the main view (or to show the main view
        #  *after* the setup is done) then the layout is borked.
        # This is a simple solution that solves the immediate problem, but a
        #  rewrite of the initialization code that affords a better solution
        #  would be worth considering at some point.
        if int(QtCore.QSettings().value("hide_on_startup", 0)):
            controller.view.hide()
        icon = TrayIcon(controller)
        icon.show()
        controller.hasTrayIcon = True
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    run()

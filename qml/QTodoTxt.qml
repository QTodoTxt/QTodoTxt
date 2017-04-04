import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.1

//this imports the MainControllerQml class which is exported in python
import MCQ 1.0
//import MC 1.0

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("QTodoTxt")

    //This instanciates the MainControllerQml class:
    MCQ {
        id: mcq
        Component.onCompleted: console.log("hallo")
    }

//    MC {
//        id: mc
//        view: parent
//        Component.onCompleted: console.log("hallo mc")
//    }

    //the Actions are already defined in python, we just need to make them available to qml
    Action {
        id: fileOpen
        iconName: "document-open"
        text: qsTr("Open")
        shortcut: StandardKey.Open
        onTriggered: {        }
    }

    Action {
        id: fileSave
        iconName: "document-save"
        text: qsTr("Save")
        shortcut: StandardKey.Save
        onTriggered: {        }
    }

    Action {
        id: fileRevert
        iconName: "document-save"
        text: qsTr("Revert")
        onTriggered: {        }
    }

    Action {
        id: editNewTask
        iconName: "list-add"
        text: qsTr("Create New Task")
        shortcut: "Ins"
        onTriggered: {        }
    }

    Action {
        id: editEditTask
        iconName: "document-edit"
        text: qsTr("Edit Task")
        shortcut: "Ctrl+E"
        onTriggered: {        }
    }

    Action {
        id: editCompleteTasks
        iconName: "document-edit"
        text: qsTr("Complete Selected Tasks")
        shortcut: "X"
        onTriggered: {        }
    }

    Action {
        id: showSearchAction
        iconName: "search"
        text: qsTr("Show Search Field")
        shortcut: "Ctrl+F"
        checkable: true
    }

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem { text: qsTr("New"); shortcut: "Ctrl+Shift+N" }
            MenuItem { action: fileOpen}
            MenuItem { action: fileSave }
            MenuItem { action: fileRevert }
            MenuSeparator {}
            MenuItem { text: qsTr("Preferences") }
            MenuSeparator {}
            MenuItem { text: qsTr("Exit");  shortcut: "Alt+F4"}
        }
        Menu {
            title: qsTr("Edit")
            MenuItem { action: editNewTask }
            MenuItem { action: editEditTask }
            MenuSeparator {}
            MenuItem { action: editCompleteTasks}
        }
        Menu {
            title: qsTr("View")
            MenuItem { action: showSearchAction}
        }
        Menu {
            title: qsTr("Help")
            MenuItem { }
        }
    }

    toolBar: ToolBar {
        RowLayout {
            anchors.fill: parent
            MenuSeparator{}
            ToolButton { action: fileOpen }
            ToolButton { action: fileSave }
            //ToolBarSeparator { }
            ToolButton { action: editNewTask }
            ToolButton { action: editEditTask }
            ToolButton { action:  mc.actions['showSearchAction']}
            Item { Layout.fillWidth: true }
        }
    }

    SplitView {
        anchors.fill: parent
        orientation: Qt.Horizontal
        Rectangle {
            id: treeViewPlaceHolder
            color: "white"
            width: 150
            Layout.minimumWidth: 150
            Layout.fillHeight: true

        }
        ColumnLayout {
            Layout.minimumWidth: 50
            Layout.fillWidth: true
            TextField {
                Layout.fillWidth: true
                visible: showSearchAction.checked
                placeholderText: "Search"
            }
            TaskListView {
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }

}

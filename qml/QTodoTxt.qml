import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.1

import MCQ 1.0
//import MC 1.0

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("QTodoTxt")

    MCQ {
        id: mcq
        Component.onCompleted: console.log("hallo")
    }


//    MC {
//        id: mc
//        view: parent
//        Component.onCompleted: console.log("hallo mc")
//    }

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
        iconName: "task-plus"
        text: qsTr("Create New Task")
        shortcut: "Ins"
        onTriggered: {        }
    }

    Action {
        id: editEditTask
        iconName: "task-edit"
        text: qsTr("Edit Task")
        shortcut: "Ctrl+E"
        onTriggered: {        }
    }

    Action {
        id: editCompleteTasks
        iconName: "task-check"
        text: qsTr("Complete Selected Tasks")
        shortcut: "X"
        onTriggered: {        }
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
                placeholderText: mc.test + mc.taskList.length + typeof mc.taskList//mcq.name
            }
            ListView {
                Layout.fillHeight: true
                Layout.fillWidth: true
//                alternatingRowColors: true
//                headerVisible: false
                model: mc.taskList
//                    ListModel {
//                    ListElement { text: "Task 2" }
//                    ListElement { text: "Task 2" }
//                    ListElement { text: "Task 3" }
//                    ListElement { text: "Task 4" }
//                }
//                TableViewColumn {
//                    role: "text"
//                }
                delegate: Label { text: mc.taskList[model.index].text }
                Component.onCompleted: console.log(mc.taskList)
            }
        }
    }

}

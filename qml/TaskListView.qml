import QtQuick 2.7
import QtQuick.Controls 1.4

ListView {
    id: lv
    function editCurrentTask() {
        if (currentItem !== null) {
            currentItem.state = "edit"
        }
    }

    highlight:
        Rectangle {
        width: 180; height: 40
        color: "lightsteelblue"; radius: 5
        y: lv.currentItem.y
        Behavior on y {
            SpringAnimation {
                spring: 3
                damping: 0.2
            }
        }
    }
    highlightFollowsCurrentItem: true
//    currentIndex: -1
    spacing: 10
    interactive: true
//    keyNavigationEnabled: true

    model: mc.taskList
    delegate: TaskLine {
        width: lv.width
        text: mc.taskList[model.index].text
        html: mc.taskList[model.index].html
        current: (currentIndex === model.index)
        onActivated: lv.currentIndex = model.index
        onShowContextMenu: {
            console.log("rightclick")
            contextMenu.popup()
        }
    }

    Menu {
        id: contextMenu
        MenuItem { action: editNewTask }
        MenuItem { action: editEditTask }
    }
}


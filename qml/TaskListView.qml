import QtQuick 2.5

ListView {
    currentIndex: -1
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
    id: lv
    spacing: 10
    model: mc.taskList
    delegate: TaskLine {
        width: lv.width
        text: mc.taskList[model.index].text
        html: mc.taskList[model.index].html
        current: (currentIndex === model.index)
        onActivated: lv.currentIndex = model.index
    }
}


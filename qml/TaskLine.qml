import QtQuick 2.2
import QtQuick.Controls 1.2


Loader {
    id: loader
    property string text: ""
    property string html: ""
    property bool current: false
    onCurrentChanged: if (!current) state = "show"
    signal activated()
    height: item.height

    state: "show"
    sourceComponent: labelComp

    Component {
        id: labelComp
        Label {
            id: label
            text: loader.html
            width: loader.width
            textFormat: Qt.RichText
            wrapMode: Text.Wrap
            MouseArea {
                anchors.fill: parent
                onDoubleClicked: {
                    loader.activated()
                    loader.state = "edit"
                }
                onClicked: loader.activated()
            }
        }
    }

    Component {
        id: editor
        TextField {
            text: loader.text
            width: loader.width
            onEditingFinished: {
                loader.state = "show"
            }
            onActiveFocusChanged: if (!activeFocus) loader.state = "show"
        }
    }

    states: [
        State {
            name: "show"
            PropertyChanges {
                target: loader
                sourceComponent: labelComp
            }
        },
        State {
            name: "edit"
            PropertyChanges {
                target: loader
                sourceComponent: editor
            }
        }
    ]
}

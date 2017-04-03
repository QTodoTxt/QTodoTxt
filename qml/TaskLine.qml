import QtQuick 2.2
import QtQuick.Controls 1.2


Item {
    id: root
    state: "show"
    property string text: ""
    property string html: ""
    Loader {
        id: loader
        sourceComponent: label
    }

    Component {
        id: label
        Label {
            text: root.html
            width: root.width
            textFormat: Qt.RichText
            wrapMode: Text.Wrap
            MouseArea {
                anchors.fill: parent
                onClicked: root.state = "edit"
            }
        }
    }

    Component {
        id: editor
        TextField {
            text: root.text
            width: root.width
        }
    }

    states: [
        State {
            name: "show"
            PropertyChanges {
                target: loader
                sourceComponent: label

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

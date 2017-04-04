import QtQuick 2.2
import QtQuick.Controls 1.2


Loader {
    id: loader
    property string text: ""
    property string html: ""
    height: item.height

    state: "show"
    sourceComponent: label

    Component {
        id: label
        Label {
            text: loader.html
            width: loader.width
            textFormat: Qt.RichText
            wrapMode: Text.Wrap
            MouseArea {
                anchors.fill: parent
                onClicked: loader.state = "edit"
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

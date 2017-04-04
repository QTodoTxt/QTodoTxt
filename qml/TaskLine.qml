import QtQuick 2.2
import QtQuick.Controls 1.2


Loader {
    id: loader
    property string text: ""
    property string html: ""
    property bool current: false
    onCurrentChanged: if (!current) state = "show"
    signal activated()
    signal showContextMenu(real x, real y)
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
                //                enabled: false
                anchors.fill: parent
                onDoubleClicked: {
                    loader.activated()
                    loader.state = "edit"
                }
                onClicked: {
//                    if (mouse.button === Qt.LeftButton)
                        loader.activated()
                    console.log("rightclick")
                    if (mouse.button === Qt.RightButton) loader.showContextMenu(mouse.x, mouse.y)
                }
            }
            onLinkActivated: Qt.openUrlExternally(link)
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
            //            onActiveFocusChanged: if (!activeFocus) loader.state = "show"
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

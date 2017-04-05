import QtQuick 2.2
import QtQuick.Controls 1.2


Loader {
    id: loader
    property string text: ""
    property string html: ""

    property bool current: false
    onCurrentChanged: if (!current) state = "show"
    signal activated()
    signal showContextMenu()

    state: "show"
    sourceComponent: labelComp

    Component {
        id: labelComp
        MouseArea {
            anchors.fill: parent
            property alias lblHeight: label.height
            acceptedButtons: Qt.LeftButton | Qt.RightButton
            onClicked: {
                loader.activated()
                if (mouse.button === Qt.RightButton) loader.showContextMenu()
            }
            onDoubleClicked: {
                loader.activated()
                loader.state = "edit"
            }
            Label {
                id: label
                anchors.verticalCenter: parent.verticalCenter
                text: loader.html
                width: loader.width
                textFormat: Qt.RichText
                wrapMode: Text.Wrap
                onLinkActivated: {
                    console.log(link)
                    Qt.openUrlExternally(link)
                }
            }
        }
    }

    Component {
        id: editorComp
        TextField {
            id: editor
//            width: loader.width
//            anchors.verticalCenter: parent.verticalCenter

            text: loader.text
            focus: true
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
                height: loader.item.lblHeight + 10
            }
        },
        State {
            name: "edit"
            PropertyChanges {
                target: loader
                sourceComponent: editorComp
                height: loader.item.implicitHeight + 10
            }
        }
    ]
}

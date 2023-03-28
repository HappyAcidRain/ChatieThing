/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 6.4
import QtQuick.Controls 6.4
import ChatGpt
import QtQuick.Timeline 1.0

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height
    color: "#7f7f7f"


    TextInput {
        id: ti_userEnter
        x: 8
        y: 1058
        width: 618
        height: 249
        text: "задайте вопрос"
        font.pixelSize: 25
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.styleName: "Обычный"
    }

    Text {
        id: te_chatAnswer
        x: 8
        y: 8
        width: 752
        height: 744
        text: qsTr("Здесь будет ответ...")
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        StackView {
            id: stackView
            x: 286
            y: 475
            width: 200
            height: 200
        }
    }

    Button {
        id: btn_commit
        x: 632
        y: 1156
        width: 128
        height: 53
        text: qsTr("Спросить")
        antialiasing: false
        display: AbstractButton.TextBesideIcon
        highlighted: true
        flat: true
    }

    Timeline {
        id: t_main
        animations: [
            TimelineAnimation {
                id: a_answerInWork
                loops: 1
                running: true
                duration: 1000
                to: 700
                from: 0
            }
        ]
        enabled: true
        endFrame: 1000
        startFrame: 0

        KeyframeGroup {
            target: ti_userEnter
            property: "x"
            Keyframe {
                frame: 0
                value: 8
            }

            Keyframe {
                frame: 652
                value: 8
            }
        }

        KeyframeGroup {
            target: ti_userEnter
            property: "y"
            Keyframe {
                frame: 0
                value: 758
            }

            Keyframe {
                frame: 652
                value: 1052
            }
        }

        KeyframeGroup {
            target: btn_commit
            property: "x"
            Keyframe {
                frame: 0
                value: 632
            }

            Keyframe {
                frame: 651
                value: 632
            }
        }

        KeyframeGroup {
            target: btn_commit
            property: "y"
            Keyframe {
                frame: 0
                value: 856
            }

            Keyframe {
                frame: 651
                value: 1150
            }
        }

        KeyframeGroup {
            target: te_chatAnswer
            property: "width"
            Keyframe {
                frame: 698
                value: 752
            }
        }

        KeyframeGroup {
            target: te_chatAnswer
            property: "height"
            Keyframe {
                frame: 698
                value: 945
            }
        }

        KeyframeGroup {
            target: te_chatAnswer
            property: "x"
            Keyframe {
                frame: 698
                value: 8
            }
        }

        KeyframeGroup {
            target: te_chatAnswer
            property: "y"
            Keyframe {
                frame: 698
                value: 8
            }
        }
    }
    states: [
        State {
            name: "clicked"
            when: btn_commit.checked

            PropertyChanges {
                target: t_main
            }
        }
    ]
}

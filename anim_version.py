# база
import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect

# окно
import MainWin

# чат гпт даёт ответы
import GPT as G


class MainWindow(QtWidgets.QMainWindow, MainWin.Ui_MainWindow, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # настройки окна
        self.setWindowTitle("ChatieThing")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(2)
        self.btn_commit.setGraphicsEffect(shadow)

        # настройка анимации
        self.anim_btn = QPropertyAnimation(self.btn_commit, b"pos")
        self.anim_te = QPropertyAnimation(self.te_userEnter, b"pos")

        # кнопушка
        self.btn_commit.clicked.connect(self.get_answer)
        self.btn_commit.clicked.connect(self.animation)

    def get_answer(self):
        question = str(self.te_userEnter.toPlainText())
        answer = str(G.askGpt(question))

        self.te_gptAnswer.setText(answer)

    def animation(self):
        # анимация кнопки
        self.anim_btn.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_btn.setEndValue(QPoint(250, 460))
        self.anim_btn.setDuration(900)
        self.anim_btn.start()

        # анимация текстового поля
        self.anim_te.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_te.setEndValue(QPoint(10, 460))
        self.anim_te.setDuration(900)
        self.anim_te.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    w = QtWidgets.QStackedWidget()
    w.addWidget(mainWindow)
    w.show()
    sys.exit(app.exec())

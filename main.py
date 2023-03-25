# база
import sys
from PyQt6 import QtWidgets 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect

# окно
import MainWin

# чат GPT
import openai
openai.api_key = "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"

# иное 
import time


class MainWindow(QtWidgets.QMainWindow, MainWin.Ui_MainWindow, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        user_message = []
        bot_answer = []
        history_ = []

        # основные настройки окна
        self.setWindowTitle("ChatieThing")

        # косметические настрйоки окна 
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(2)
        self.btn_commit.setGraphicsEffect(shadow)
        self.te_gptAnswer.setGraphicsEffect(shadow)
        self.te_userEnter.setGraphicsEffect(shadow)
        self.pb_progress.setGraphicsEffect(shadow)

        # кнопушка 
        self.btn_commit.clicked.connect(self.get_answer)
        

    def get_answer(self):

        # обновляем прогрессБар
        self.pb_progress.setRange(0,2)
        self.pb_progress.setValue(1)

        # генерируем ответ
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt= str(self.te_userEnter.toPlainText()),
            max_tokens=2048,
            temperature=0.3
        )

        # еще раз обновляем прогрессБар
        self.pb_progress.setValue(2)
        self.pb_progress.reset()

        # выводим ответ 
        self.te_gptAnswer.setText(str(completion.choices[0].text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()

    # фиксируем размеры окна
    m.setFixedWidth(300)
    m.setFixedHeight(480)

    m.show()
    sys.exit(app.exec())

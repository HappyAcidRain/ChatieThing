# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer

# окна
import mainUI
import regUI

# прочее
import sqlite3
import openai

class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow, QtCore.QTimer, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # стартовые позиции эллементов (an_wellcome)
        self.le_username.move(70, 220)
        self.btn_commitLogin.move(70, 220)

        # настройка анимации (an_wellcome)
        self.anW_username = QPropertyAnimation(self.le_username, b"pos")
        self.anW_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")

        # настройка анимации (an_shake)
        self.anS_password = QPropertyAnimation(self.le_password, b"pos")
        self.anS_username = QPropertyAnimation(self.le_username, b"pos")
        self.anS_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")

        # настройка анимации (an_chat)
        self.anC_password = QPropertyAnimation(self.le_password, b"pos")
        self.anC_username = QPropertyAnimation(self.le_username, b"pos")
        self.anC_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")
        self.anC_answer = QPropertyAnimation(self.tb_answer, b"pos")
        self.anC_question = QPropertyAnimation(self.te_question, b"pos")
        self.anC_commitQue = QPropertyAnimation(self.btn_commitQue, b"pos")
        self.delay = QTimer()

        # привязка анимации
        self.le_username.textEdited.connect(self.an_wellcome)

        # кнопушка 
        self.btn_commitLogin.clicked.connect(self.login) # заменить на login
        self.btn_commitQue.clicked.connect(self.chatGPT)

    def login(self):

        # подключение к БД
        connect = sqlite3.connect("loginData.db")
        cursor = connect.cursor()

        # получение данных 
        usernameFind = str(self.le_username.text())
        passwordFind = str(self.le_password.text())

        try:
            # ищем пользователя в БД
            cursor.execute(f"SELECT key FROM data WHERE username LIKE '%{usernameFind}%' ")
            DB_key = cursor.fetchone()

            # конвертация DB_key(typle) в str
            DB_key_str=""
            for i in DB_key:
                DB_key_str+=str(i)

            # записываем ключ
            openai.api_key = DB_key_str

            # открываем чат
            self.an_chat()

        except TypeError:

            # показываем ошибку
            self.an_shake()

    def reg(self):      # TODO: реворк

        # подключение к БД
        connect = sqlite3.connect("loginData.db")
        cursor = connect.cursor()

        # получение данных 
        usernameInput = str(self.le_username.text())
        passwordInput = str(self.le_password.text())

        try:
            # изменение данных (имя)
            cursor.execute("INSERT INTO data(username) VALUES(?);", (usernameInput,))
            cursor.execute("UPDATE data SET password = (?) WHERE username = (?);", (passwordInput, usernameInput))
            connect.commit()

            # закрываем БД
            connect.close()

            # открываем чат
            self.an_chat()

        except sqlite3.IntegrityError:
            # закрываем БД
            connect.close()

            # показвываем ошибку
            self.an_shake()

    # анимация "раздвижения" кнопок 
    def an_wellcome(self):

        # анимация кнопки
        self.anW_commitLogin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anW_commitLogin.setEndValue(QPoint(70, 270))
        self.anW_commitLogin.setDuration(700)
        self.anW_commitLogin.start()

        # анимация текстового поля
        self.anW_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anW_username.setEndValue(QPoint(70, 170))
        self.anW_username.setDuration(700)
        self.anW_username.start()

    # анимация тряски
    def an_shake(self):

        # чистим поля
        self.le_username.clear()
        self.le_password.clear()

        # ввыодим в Placeholder'ы сообщения 
        self.le_username.setPlaceholderText("Данный пользователь уже есть")
        self.le_password.setPlaceholderText("Попробуйте еще раз")

        # анмиация кнопки 
        self.anS_commitLogin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_commitLogin.setKeyValueAt(0.1, QPoint(50, 270))
        self.anS_commitLogin.setKeyValueAt(0.3, QPoint(90, 270))
        self.anS_commitLogin.setEndValue(QPoint(70, 270))
        self.anS_commitLogin.setDuration(400)
        self.anS_commitLogin.start()

        # анимация поля пароля
        self.anS_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_password.setKeyValueAt(0.1, QPoint(50, 220))
        self.anS_password.setKeyValueAt(0.3, QPoint(90, 220))
        self.anS_password.setEndValue(QPoint(70, 220))
        self.anS_password.setDuration(400)
        self.anS_password.start()

        # анимация поля имени
        self.anS_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_username.setKeyValueAt(0.1, QPoint(50, 170))
        self.anS_username.setKeyValueAt(0.3, QPoint(90, 170))
        self.anS_username.setEndValue(QPoint(70, 170))
        self.anS_username.setDuration(400)
        self.anS_username.start()

    # анимация появления чата
    def an_chat(self):

        """ анимация "ухода" полей и кнопки входа """

        # анимация кнопки входа
        self.anC_commitLogin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_commitLogin.setEndValue(QPoint(-400, 270))
        self.anC_commitLogin.setDuration(700)
        self.delay.singleShot(100, self.anC_commitLogin.start)

        # анимация поля пароля
        self.anC_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_password.setEndValue(QPoint(-400, 220))
        self.anC_password.setDuration(700)
        self.delay.singleShot(50, self.anC_password.start)

        # анимация поля имени
        self.anC_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_username.setEndValue(QPoint(-400, 170))
        self.anC_username.setDuration(700)
        self.anC_username.start()


        """ анимация "появления" полей и кнопки ChatGPT """

        # анимация поля ответа
        self.anC_answer.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_answer.setEndValue(QPoint(40, 30))
        self.anC_answer.setDuration(700)
        self.delay.singleShot(200, self.anC_answer.start)

        # анимация поля вопроса
        self.anC_question.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_question.setEndValue(QPoint(40, 420))
        self.anC_question.setDuration(700)
        self.delay.singleShot(100, self.anC_question.start)

        # анимация кнопки отправки
        self.anC_commitQue.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anC_commitQue.setEndValue(QPoint(320, 420))
        self.anC_commitQue.setDuration(700)
        self.delay.singleShot(100, self.anC_commitQue.start)
    
    # получаем ответ 
    def chatGPT(self):
        """
        # генерируем ответ
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=str(self.te_question.toPlainText()),
            max_tokens=2048,
            temperature=0.3
        )

        # выводим овтет
        self.tb_answer.setPlainText(str(completion.choices[0].text)) """

        pass

class RegWindow(QtWidgets.QMainWindow, regUI.Ui_MainWindow, QtCore.QTimer, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def reg(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()

    # фиксируем размеры окна
    m.setFixedWidth(400)
    m.setFixedHeight(500)

    m.show()	
    sys.exit(app.exec())

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

        # настройки окна
        self.setFixedWidth(400)
        self.setFixedHeight(500)

        # стартовые позиции эллементов (an_wellcome)
        self.le_username.move(70, 220)
        self.btn_commitLogin.move(70, 220)

        # настройка анимации (an_wellcome)
        self.anW_username = QPropertyAnimation(self.le_username, b"pos")
        self.anW_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")
        self.anW_reg = QPropertyAnimation(self.btn_reg, b"pos")

        # настройка анимации (an_shake)
        self.anS_password = QPropertyAnimation(self.le_password, b"pos")
        self.anS_username = QPropertyAnimation(self.le_username, b"pos")
        self.anS_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")

        # настройка анимации (an_chat)
        self.anC_password = QPropertyAnimation(self.le_password, b"pos")
        self.anC_username = QPropertyAnimation(self.le_username, b"pos")
        self.anC_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")
        self.anС_btnReg = QPropertyAnimation(self.btn_reg, b"pos")
        self.anC_answer = QPropertyAnimation(self.tb_answer, b"pos")
        self.anC_question = QPropertyAnimation(self.te_question, b"pos")
        self.anC_commitQue = QPropertyAnimation(self.btn_commitQue, b"pos")
        self.delay = QTimer()

        # привязка анимации
        self.le_username.textEdited.connect(self.an_wellcome)

        # кнопушки 
        self.btn_reg.clicked.connect(self.reg)
        self.btn_commitLogin.clicked.connect(self.login) 
        self.btn_commitQue.clicked.connect(self.chatGPT)

    # вход
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

    # окно регистрации
    def reg(self):
        self.reg_window = RegWindow()
        self.reg_window.show()

    # получаем ответ 
    def chatGPT(self):
        
        # генерируем ответ
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=str(self.te_question.toPlainText()),
            max_tokens=2048,
            temperature=0.3
        )

        # выводим овтет
        self.tb_answer.setPlainText(str(completion.choices[0].text))

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

        """ анимация "ухода" полей и кнопок """

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

        # анимация кнопки регистрации
        self.anС_btnReg.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anС_btnReg.setEndValue(QPoint(89, 520))
        self.anС_btnReg.setDuration(700)
        self.anС_btnReg.start()


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

class RegWindow(QtWidgets.QMainWindow, regUI.Ui_MainWindow, QtCore.QTimer, QDialog):

    def __init__(self):
        super(RegWindow, self).__init__()
        self.setupUi(self)

        # настройки окна
        self.setFixedWidth(370)
        self.setFixedHeight(390)

        # TODO: реворк
        # настройка ярлыка помощи  
        # rllink = "<a href = https://www.youtube.com/watch?v=dQw4w9WgXcQ >как получить API-ключ</a>"
        # self.lbl_help.setText(urllink)

        # настройка анимации (an_shake)
        self.anS_password = QPropertyAnimation(self.le_password, b"pos")
        self.anS_username = QPropertyAnimation(self.le_username, b"pos")
        self.anS_key = QPropertyAnimation(self.le_key, b"pos")
        self.anS_reg = QPropertyAnimation(self.btn_reg, b"pos")

        # настрйока анмиации (an_pass)
        self.anP_password = QPropertyAnimation(self.le_password, b"pos")
        self.anP_username = QPropertyAnimation(self.le_username, b"pos")
        self.anP_key = QPropertyAnimation(self.le_key, b"pos")
        self.anP_btnReg = QPropertyAnimation(self.btn_reg, b"pos")
        self.anP_LabelHelp = QPropertyAnimation(self.lbl_help, b"pos")
        self.anP_LabelPass = QPropertyAnimation(self.lbl_pass, b"pos")
        self.anP_LabelCloseWin = QPropertyAnimation(self.lbl_closeWin, b"pos")
        self.delay = QTimer()

        # кнопушка
        self.btn_reg.clicked.connect(self.reg)

    # регистрация
    def reg(self):

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

            # проигрываем анимацию 
            self.an_pass()

        except sqlite3.IntegrityError:
            # закрываем БД
            connect.close()

            # показвываем ошибку
            self.an_shake()

    # анимация успещной регистрации
    def an_pass(self):
        
        """ анимация "ухода" полей, кнопок и ярлыка помощи """

        # анимация поля имени
        self.anP_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_username.setEndValue(QPoint(-250, 60))
        self.anP_username.setDuration(700)
        self.anP_username.start()

        # анимация поля пароля
        self.anP_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_password.setEndValue(QPoint(-250, 110))
        self.anP_password.setDuration(700)
        self.delay.singleShot(50, self.anP_password.start)

        # анимация поля ключа
        self.anP_key.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_key.setEndValue(QPoint(-250, 160))
        self.anP_key.setDuration(700)
        self.delay.singleShot(100, self.anP_key.start)

        # анимация кнопки регистрации
        self.anP_btnReg.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_btnReg.setEndValue(QPoint(-250, 210))
        self.anP_btnReg.setDuration(700)
        self.delay.singleShot(150, self.anP_btnReg.start)

        # анимация ярлыка помощи
        self.anP_LabelHelp.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_LabelHelp.setEndValue(QPoint(-250, 310))
        self.anP_LabelHelp.setDuration(700)
        self.delay.singleShot(200, self.anP_LabelHelp.start)


        """ анимация "появления" ярлыков """

        # анимация ярлыка успешной регистрации
        self.anP_LabelPass.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_LabelPass.setEndValue(QPoint(60, 180))
        self.anP_LabelPass.setDuration(700)
        self.delay.singleShot(250, self.anP_LabelPass.start)

        # анимация ярлыка закрытия окна
        self.anP_LabelCloseWin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anP_LabelCloseWin.setEndValue(QPoint(60, 350))
        self.anP_LabelCloseWin.setDuration(700)
        self.delay.singleShot(300, self.anP_LabelCloseWin.start)

    # анимация тряски
    def an_shake(self):

        # чистим поля
        self.le_username.clear()
        self.le_password.clear()
        self.le_key.clear()

        # ввыодим в Placeholder'ы сообщения 
        self.le_username.setPlaceholderText("Ошибка!")
        self.le_password.setPlaceholderText("Данный пользователь уже есть")
        self.le_key.setPlaceholderText("Попробуйте еще раз")

        # анмиация кнопки 
        self.anS_reg.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_reg.setKeyValueAt(0.1, QPoint(40, 210))
        self.anS_reg.setKeyValueAt(0.3, QPoint(80, 210))
        self.anS_reg.setEndValue(QPoint(60, 210))
        self.anS_reg.setDuration(400)
        self.anS_reg.start()

        # анимация поля пароля
        self.anS_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_password.setKeyValueAt(0.1, QPoint(40, 110))
        self.anS_password.setKeyValueAt(0.3, QPoint(80, 110))
        self.anS_password.setEndValue(QPoint(60, 110))
        self.anS_password.setDuration(400)
        self.anS_password.start()

        # анимация поля имени
        self.anS_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_username.setKeyValueAt(0.1, QPoint(40, 60))
        self.anS_username.setKeyValueAt(0.3, QPoint(80, 60))
        self.anS_username.setEndValue(QPoint(60, 60))
        self.anS_username.setDuration(400)
        self.anS_username.start()

        # анимация поля ключа
        self.anS_key.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anS_key.setKeyValueAt(0.1, QPoint(40, 160))
        self.anS_key.setKeyValueAt(0.3, QPoint(80, 160))
        self.anS_key.setEndValue(QPoint(60, 160))
        self.anS_key.setDuration(400)
        self.anS_key.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()	
    sys.exit(app.exec())

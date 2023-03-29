# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint

# окно
import mainUI

# прочее
import sqlite3

class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # стартовые позиции эллементов (an_wellcome)
        self.le_username.move(70, 220)
        self.btn_commitLogin.move(70, 220)

        # настройка анимации (an_wellcome)
        self.an1_username = QPropertyAnimation(self.le_username, b"pos")
        self.an1_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")

        # настройка анимации (an_shake)
        self.an_password = QPropertyAnimation(self.le_password, b"pos")
        self.an_username = QPropertyAnimation(self.le_username, b"pos")
        self.an_commitLogin = QPropertyAnimation(self.btn_commitLogin, b"pos")

        # привязка анимации
        self.le_username.textEdited.connect(self.an_wellcome)

        # кнопушка 
        self.btn_commitLogin.clicked.connect(self.login)

    def login(self):

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
            # чистим поля
            self.le_username.clear()
            self.le_password.clear()

            # ввыодим в Placeholder'ы сообщения 
            self.le_username.setPlaceholderText("Данный пользователь уже есть")
            self.le_password.setPlaceholderText("Попробуйте еще раз")

            # закрываем БД
            connect.close()

            # анимация тряски
            self.an_shake()

    # анимация "раздвижения" кнопок 
    def an_wellcome(self):

        # анимация кнопки
        self.an1_commitLogin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an1_commitLogin.setEndValue(QPoint(70, 270))
        self.an1_commitLogin.setDuration(700)
        self.an1_commitLogin.start()

        # анимация текстового поля
        self.an1_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an1_username.setEndValue(QPoint(70, 170))
        self.an1_username.setDuration(700)
        self.an1_username.start()

    # анимация тряски
    def an_shake(self):

        # анмиация кнопки 
        self.an_commitLogin.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an_commitLogin.setKeyValueAt(0.1, QPoint(50, 270))
        self.an_commitLogin.setKeyValueAt(0.3, QPoint(90, 270))
        self.an_commitLogin.setEndValue(QPoint(70, 270))
        self.an_commitLogin.setDuration(400)
        self.an_commitLogin.start()

        # анимация поля пароля
        self.an_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an_password.setKeyValueAt(0.1, QPoint(50, 220))
        self.an_password.setKeyValueAt(0.3, QPoint(90, 220))
        self.an_password.setEndValue(QPoint(70, 220))
        self.an_password.setDuration(400)
        self.an_password.start()

        # анимация поля имени
        self.an_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an_username.setKeyValueAt(0.1, QPoint(50, 170))
        self.an_username.setKeyValueAt(0.3, QPoint(90, 170))
        self.an_username.setEndValue(QPoint(70, 170))
        self.an_username.setDuration(400)
        self.an_username.start()

    # анимация появления чата
    def an_chat(self):
        pass 

        # TODO: сделай аниацию "лесенкой"

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()    
    m.show()	
    sys.exit(app.exec())

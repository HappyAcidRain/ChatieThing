# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint

# окно
import LoginTest

# прочее
import sqlite3


class MainWindow(QtWidgets.QMainWindow, LoginTest.Ui_MainWindow, QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # настройка анимации
        self.an_commit = QPropertyAnimation(self.btn_commit, b"pos")
        self.an_password = QPropertyAnimation(self.le_password, b"pos")
        self.an_username = QPropertyAnimation(self.le_username, b"pos")

        # привязка анимации
        self.le_username.textEdited.connect(self.anim)

        # стартовые позиции эллементов
        self.le_password.move(70, 160)
        self.btn_commit.move(70, 210)

        # кнопушка 
        self.btn_commit.clicked.connect(self.login)


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

        except sqlite3.IntegrityError:
            # чистим поля
            self.le_username.clear()
            self.le_password.clear()

            # ввыодим в Placeholder'ы сообщения 
            self.le_username.setPlaceholderText("Данный пользователь уже есть")
            self.le_password.setPlaceholderText("Попробуйте еще раз")

            # закрываем БД
            connect.close()

            # анмиация тряски
            self.shake()

            # TODO: почини постоянную тряску при вводе текста 

    def anim(self):

        # анимация кнопки
        self.an_commit.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an_commit.setEndValue(QPoint(70, 260))
        self.an_commit.setDuration(700)
        self.an_commit.start()

        # анимация текстового поля
        self.an_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.an_password.setEndValue(QPoint(70, 210))
        self.an_password.setDuration(700)
        self.an_password.start()

    def shake(self):

        global times
        times = 0

        if times == 0:

            # анимация тряски
            self.an_commit.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.an_commit.setKeyValueAt(0.1, QPoint(50, 260))
            self.an_commit.setKeyValueAt(0.3, QPoint(90, 260))
            self.an_commit.setEndValue(QPoint(70, 260))
            self.an_commit.setDuration(400)
            self.an_commit.start()

            self.an_password.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.an_password.setKeyValueAt(0.1, QPoint(50, 210))
            self.an_password.setKeyValueAt(0.3, QPoint(90, 210))
            self.an_password.setEndValue(QPoint(70, 210))
            self.an_password.setDuration(400)
            self.an_password.start()

            self.an_username.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.an_username.setKeyValueAt(0.1, QPoint(50, 160))
            self.an_username.setKeyValueAt(0.3, QPoint(90, 160))
            self.an_username.setEndValue(QPoint(70, 160))
            self.an_username.setDuration(400)
            self.an_username.start()

            # записываем колличесвто раз воспроизведения
            times += 1

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()    
    m.show()	
    sys.exit(app.exec())

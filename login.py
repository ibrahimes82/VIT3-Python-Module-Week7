from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLineEdit

import main
from login_ui import Ui_MainWindow
from admin_menu import AdminMenuPage
from user_menu import UserMenuPage


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.users = main.connection_hub('key.json', 'Kullanicilar')
        self.form_login = Ui_MainWindow()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.form_login.setupUi(self)
        self.menu_admin = None
        self.menu_user = None

        # Password alaninda iken Enter tusuna basinca yetki kontrolu yapmak icin kodlar
        self.form_login.lineEditPassword.returnPressed.connect(self.app_login)

        # 'pushButton_log_login' butonuna tiklandiginda yetki kontrolu yapmak icin kodlar
        self.form_login.pushButtonLogin.clicked.connect(self.app_login)
        self.form_login.pushButtonExit.clicked.connect(self.app_exit)

        # Checking the correctness of the password
        self.form_login.checkBoxPassword.clicked.connect(self.check_password)

    def app_login(self):
        username = self.form_login.lineEditUsername.text()
        password = self.form_login.lineEditPassword.text()

        for user in self.users[1:]:
            if username == user[0] and password == user[1] and user[2] == 'admin':
                self.hide()
                self.menu_admin = AdminMenuPage(user)
                self.menu_admin.show()

            elif username == user[0] and password == user[1] and user[2] == 'user':
                self.hide()
                self.menu_user = UserMenuPage(user)
                self.menu_user.show()
            else:
                self.form_login.labelFail.setText("<b>Your email or password is incorrect.</b>")
                self.form_login.lineEditUsername.setText("")
                self.form_login.lineEditPassword.setText("")

    # To check the correctness of the password
    def check_password(self):
        if self.form_login.checkBoxPassword.isChecked():
            self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.form_login.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def app_exit(self):
        self.close()

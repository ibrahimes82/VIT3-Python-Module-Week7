from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore
import gspread
from login_ui import Ui_MainWindow
from user_admin_preference import UserAdminPreferencePage
from user_preference import UserPreferencePage
import json
import os
credentials = 'key.json'
gc = gspread.service_account(filename=credentials)
spreadsheet_users = gc.open('Kullanicilar')
worksheet_users = spreadsheet_users.get_worksheet(0)
users = worksheet_users.get_all_values()
users.pop(0)


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loginForm = Ui_MainWindow()
        self.loginForm.setupUi(self)
        self.useradminwindow_open = UserAdminPreferencePage()
        self.userprewindow_open = UserPreferencePage()
        
        # Herhangi bir anda Enter tusuna basinca yetki kontrolu yapmak icin kodlar
        self.loginForm.lineEdit_password.returnPressed.connect(self.app_login)
        self.loginForm.lineEdit_username.returnPressed.connect(self.app_login)

        # 'pushButton_log_login' butonuna tiklandiginda yetki kontrolu yapmak icin kodlar
        self.loginForm.pushButton_login.clicked.connect(self.app_login)
        self.loginForm.pushButton_exit.clicked.connect(self.log_exit)
        
    def log_exit(self):
        self.close() 


    def app_login(self):
        user_type = None
        username = self.loginForm.lineEdit_username.text()
        password = self.loginForm.lineEdit_password.text()
        
         
        for user in users:
            if os.path.exists('user_type.json'):
                with open('user_type.json', 'w') as json_file:
                    json.dump({}, json_file)
                    
            if username == user[0] and password == user[1] and user[2] == 'admin':
                user_type = 'admin'
                with open('user_type.json', 'w') as json_file:
                   json.dump({"user_type": user_type}, json_file)
                
                self.hide()
                self.useradminwindow_open.show()
                self.loginForm.lineEdit_username.setText("")
                self.loginForm.lineEdit_password.setText("")
                self.loginForm.label_fail.setText("")
                
                break
            elif username == user[0] and password == user[1] and user[2] == 'user':
                user_type = 'user'
                with open('user_type.json', 'w') as json_file:
                   json.dump({"user_type": user_type}, json_file)
                self.hide()
                self.userprewindow_open.show()
                self.loginForm.lineEdit_username.setText("")
                self.loginForm.lineEdit_password.setText("")
                self.loginForm.label_fail.setText("")
                break

        else:
            self.loginForm.label_fail.setText("<b>Your email or password is incorrect.</b>")
            self.loginForm.lineEdit_username.setText("")
            self.loginForm.lineEdit_password.setText("") 
    
       
    def fail_del(self):
        self.loginForm.label_fail.setText("")
        
    
    
    

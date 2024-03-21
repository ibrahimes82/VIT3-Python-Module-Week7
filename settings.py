import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtWidgets import QWidget

import main
from settings_ui import Ui_FormSettings

# Google Sheets API'ye erişim için izinlerin belirlenmesi
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(credentials)
# sheet = client.open('Kullanicilar').worksheet('Form Yanıtları 1')


class SettingsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.decision = None
        self.form_settings = Ui_FormSettings()
        self.form_settings.setupUi(self)
        self.form_settings.labelCurrentUser.setText(self.current_user[0])
        self.form_settings.pushButtonApprove.hide()  # Acilista APPROVE butonunu gorunmez yapiyoruz

        self.form_settings.lineEditUserName.setText(current_user[0])
        # self.form_settings.lineEditUserName.setText(current_user[0])
        # self.form_settings.lineEditUserName.setText(current_user[0])
        self.form_settings.lineEditAccountType.setText(current_user[2])
        self.form_settings.pushButtonChangePassword.clicked.connect(self.change_password_page_start)
        self.form_settings.pushButtonChangeAccountDetails.clicked.connect(self.edit_account_details_start)
        self.form_settings.pushButtonApprove.clicked.connect(self.click_approve_button)

    def click_approve_button(self):
        if self.decision == '1':
            try:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Information MessageBox")
                if self.current_user[1] == self.form_settings.lineEditUserName.text():
                    if self.form_settings.lineEditName.text() == self.form_settings.lineEditSurname.text():
                        changed_user = self.current_user
                        changed_user[1] = self.form_settings.lineEditSurname.text()

                        # Process of changing the password
                        result = self.update_user(changed_user)

                        if result:
                            msg_box.setIcon(QMessageBox.Icon.Information)
                            msg_box.setText("The password has been successfully changed.")
                            self.close()
                        else:
                            msg_box.setIcon(QMessageBox.Icon.Critical)
                            msg_box.setText("WARNING! There is a problem while changing the password...\n"
                                            "The password couldn't be changed!!!")
                    else:
                        msg_box.setIcon(QMessageBox.Icon.Warning)
                        msg_box.setText("You didn't enter new passwords as same!")
                else:
                    msg_box.setIcon(QMessageBox.Icon.Warning)
                    msg_box.setText('Current password is not right!')
                msg_box.exec()
                self.change_password_page_start()
            except Exception as e:
                raise e
        else:
            pass  # Kullanici detaylari islemleri

    def update_user(self, current_u):
        users = main.connection_hub('key.json', 'Kullanicilar')
        sheet = client.open('Kullanicilar').worksheet('Form Yanıtları 1')
        for i, u in enumerate(users):
            if u[0] == self.current_user[0]:
                u[1] = current_u[1]
                sheet.update_cell(i+1, 1+1, u[1])  # Writing data to Google Sheets file
                return True
        else:
            return False

    def change_password_page_start(self):
        self.decision = '1'
        self.form_settings.labelHosgeldiniz.setText('Change the password for   :')
        self.form_settings.labelUserName.setText('Current Password')
        self.form_settings.labelName.setText('New Password')
        self.form_settings.labelSurname.setText('<html><head/><body><p><center>New Password<span style=" '
                                                'font-style:italic;"><br>(Again)</center></span></p></body></html>')
        self.form_settings.labelAccountType.close()
        self.form_settings.lineEditAccountType.close()

        self.form_settings.lineEditUserName.setEnabled(True)
        self.form_settings.lineEditName.setEnabled(True)
        self.form_settings.lineEditSurname.setEnabled(True)

        self.form_settings.lineEditUserName.setText('')
        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')
        self.form_settings.lineEditName.setPlaceholderText('')
        self.form_settings.lineEditSurname.setPlaceholderText('')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def edit_account_details_start(self):
        self.decision = '2'
        self.form_settings.labelAccountType.show()
        self.form_settings.lineEditAccountType.show()

        self.form_settings.lineEditUserName.setEnabled(True)
        self.form_settings.lineEditName.setEnabled(True)
        self.form_settings.lineEditSurname.setEnabled(True)

        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')
        self.form_settings.lineEditName.setPlaceholderText('')
        self.form_settings.lineEditSurname.setPlaceholderText('')

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def user_info_page_start(self):
        self.decision = None
        self.form_settings.labelHosgeldiniz.setText('Wellcome')
        self.form_settings.labelUserName.setText('UserName')
        self.form_settings.labelName.setText('Name')
        self.form_settings.labelSurname.setText('Surname')
        self.form_settings.labelAccountType.show()
        self.form_settings.lineEditAccountType.show()

        self.form_settings.lineEditUserName.setEnabled(False)
        self.form_settings.lineEditName.setEnabled(False)
        self.form_settings.lineEditSurname.setEnabled(False)

        self.form_settings.lineEditUserName.setText(self.current_user[0])
        self.form_settings.lineEditName.setText('')
        self.form_settings.lineEditSurname.setText('')
        self.form_settings.lineEditName.setPlaceholderText('John')
        self.form_settings.lineEditSurname.setPlaceholderText('DOE')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

        self.form_settings.pushButtonChangePassword.show()
        self.form_settings.pushButtonChangeAccountDetails.show()
        self.form_settings.pushButtonApprove.hide()


if __name__ == "__main__":
    app = QApplication([])
    main_window = SettingsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt6.QtWidgets import QWidget

from settings_ui import Ui_FormSettings


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
        self.form_settings.pushButtonChangePassword.clicked.connect(self.change_password)
        self.form_settings.pushButtonChangeAccountDetails.clicked.connect(self.edit_account_details)
        self.form_settings.pushButtonApprove.clicked.connect(self.click_approve_button)

    def change_password(self):
        self.decision = '1'
        self.form_settings.labelHosgeldiniz.setText('Change the password for   ->')
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
        self.form_settings.lineEditName.setPlaceholderText('')
        self.form_settings.lineEditSurname.setPlaceholderText('')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def edit_account_details(self):
        self.decision = '2'
        self.form_settings.labelAccountType.show()
        self.form_settings.lineEditAccountType.show()

        self.form_settings.lineEditUserName.setEnabled(True)
        self.form_settings.lineEditName.setEnabled(True)
        self.form_settings.lineEditSurname.setEnabled(True)

        self.form_settings.lineEditName.setPlaceholderText('')
        self.form_settings.lineEditSurname.setPlaceholderText('')

        self.form_settings.pushButtonChangePassword.hide()
        self.form_settings.pushButtonChangeAccountDetails.hide()
        self.form_settings.pushButtonApprove.show()

    def click_approve_button(self):
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
        self.form_settings.lineEditName.setPlaceholderText('John')
        self.form_settings.lineEditSurname.setPlaceholderText('DOE')

        self.form_settings.lineEditUserName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditName.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.form_settings.lineEditSurname.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

        self.form_settings.pushButtonChangePassword.show()
        self.form_settings.pushButtonChangeAccountDetails.show()
        self.form_settings.pushButtonApprove.hide()

        if self.decision == '1':
            pass # Sifre degisim islemleri
        else:
            pass    # Kullanici detaylari islemleri

        self.decision = None


if __name__ == "__main__":
    app = QApplication([])
    main_window = SettingsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

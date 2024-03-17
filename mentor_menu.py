from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from mentor_menu_ui import Ui_Form
import gspread
import pandas as pd
from PyQt6.QtCore import QTimer

credentials = 'key.json'
gc = gspread.service_account(filename=credentials)
spreadsheet_users = gc.open('Mentor')
worksheet_users = spreadsheet_users.get_worksheet(0)
users = worksheet_users.get_all_values()
users.pop(0)


class MentorMenuPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.mentorMenuForm = Ui_Form()
        self.mentorMenuForm.setupUi(self)
        self.timer = QTimer(self)  # Timer oluştur
        self.timer.timeout.connect(self.update_table)  # Timer her tetiklendiğinde update_table fonksiyonunu çağır
        # self.timer.start(60000)
        self.mentorMenuForm.pushButton_mentor_search.clicked.connect(self.search)
        self.mentorMenuForm.pushButton_mentor_all_app.clicked.connect(self.all_app)
        self.mentorMenuForm.pushButton_mentor_back.clicked.connect(self.back_menu)
        self.mentorMenuForm.pushButton_mentor_exit.clicked.connect(self.exit)
        self.mentorMenuForm.mentor_comboBox.currentIndexChanged.connect(self.update_table)

    def write2table(self, my_list):
        table_widget = self.mentorMenuForm.tableWidget_mentor
        table_widget.setRowCount(len(my_list))
        for row_index, item in enumerate(my_list):
            for col_index, data in enumerate(item):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def search(self):
        search_users = []
        for user in users:
            if (self.mentorMenuForm.lineEdit_mentor_username.text().lower() in user[1].lower() or self.mentorMenuForm.lineEdit_mentor_username.text().lower() in user[2].lower()) and self.mentorMenuForm.lineEdit_mentor_username.text().lower() != '':
                search_users.append(user)

        if search_users:
            return self.write2table(search_users)
        else:
            return self.write2table([['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]])

    def all_app(self):
        self.write2table(users)

    def update_table(self):
        selected_item = self.mentorMenuForm.mentor_comboBox.currentText()
        selected_row = self.mentorMenuForm.tableWidget_mentor.currentRow()

        if selected_row != -1:
            col_index = 4
            self.mentorMenuForm.tableWidget_mentor.setItem(selected_row, col_index, QTableWidgetItem(''))
            item = QTableWidgetItem(selected_item)
            self.mentorMenuForm.tableWidget_mentor.setItem(selected_row, col_index, item)
            updated_value = self.mentorMenuForm.tableWidget_mentor.item(selected_row, col_index).text()
            cell_to_update = worksheet_users.cell(selected_row + 2,
                                                  col_index + 1)  # Satır ve sütun indeksleri 1'den başladığı için +2 ve +1 ekliyoruz
            cell_to_update.value = updated_value
            worksheet_users.update_cell(selected_row + 2, col_index + 1,
                                        updated_value)  # Google Sheets'te hücreyi güncelle
            # self.timer.start(60000)

    def back_menu(self):
        import json

        # JSON dosyasındaki bilgileri oku

        with open('user_type.json', 'r') as json_file:
            data = json.load(json_file)

        # Kullanıcı türünü al
        user_type = data["user_type"]

        if user_type == "admin":
            from admin_menu import UserAdminPreferencePage
            self.hide()
            self.useradminwindow = UserAdminPreferencePage()
            self.useradminwindow.show()

        else:
            from user_menu import UserPreferencePage
            self.hide()
            self.userwindow = UserPreferencePage()
            self.userwindow.show()

    def exit(self):
        self.close()

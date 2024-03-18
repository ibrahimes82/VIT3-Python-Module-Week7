from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from mentor_menu_ui import Ui_FormMentor
import gspread
import pandas as pd
from PyQt6.QtCore import QTimer

credentials = 'key.json'
gc = gspread.service_account(filename=credentials)
spreadsheet_users = gc.open('Mentor')
worksheet_users = spreadsheet_users.get_worksheet(0)
mentees = worksheet_users.get_all_values()
headers = mentees[0]  # Başlıkları al
mentees.pop(0)  # Başlıkları at


class MentorPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user

        self.menu_user = None
        self.menu_admin = None
        self.form_mentor = Ui_FormMentor()
        self.form_mentor.setupUi(self)
        self.timer = QTimer(self)  # Timer oluştur
        self.timer.timeout.connect(self.update_table)  # Timer her tetiklendiğinde update_table fonksiyonunu çağır
        # self.timer.start(60000)
        self.form_mentor.pushButtonSearch.clicked.connect(self.search)
        self.form_mentor.pushButtonAllApplications.clicked.connect(self.all_app)
        self.form_mentor.comboBoxOptions.currentIndexChanged.connect(self.update_table)
        self.form_mentor.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_mentor.pushButtonExit.clicked.connect(self.app_exit)

    def write2table(self, a_list):
        table_widget = self.form_mentor.tableWidget
        # Tabloyu temizle
        table_widget.clearContents()
        # Tabloya başlık ekle
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        # Tabloyu doldur
        table_widget.setRowCount(len(a_list))
        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                table_widget.setItem(i, j, item)
        return True

    def search(self):
        searched_mentees = []
        for mentee in mentees:
            if (self.form_mentor.lineEditSearch.text().lower() in mentee[1].lower() or self.form_mentor.lineEditSearch.text().lower() in mentee[
                    2].lower()) and self.form_mentor.lineEditSearch.text().lower() != '':
                searched_mentees.append(mentee)

        if searched_mentees:
            return self.write2table(searched_mentees)
        else:
            return self.write2table([['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]])

    def all_app(self):
        self.write2table(mentees)

    def update_table(self):
        selected_item = self.form_mentor.comboBoxOptions.currentText()
        selected_row = self.form_mentor.tableWidget.currentRow()

        if selected_row != -1:
            col_index = 4
            self.form_mentor.tableWidget.setItem(selected_row, col_index, QTableWidgetItem(''))
            item = QTableWidgetItem(selected_item)
            self.form_mentor.tableWidget.setItem(selected_row, col_index, item)
            updated_value = self.form_mentor.tableWidget.item(selected_row, col_index).text()
            cell_to_update = worksheet_users.cell(selected_row + 2,
                                                  col_index + 1)  # Satır ve sütun indeksleri 1'den başladığı için +2 ve +1 ekliyoruz
            cell_to_update.value = updated_value
            worksheet_users.update_cell(selected_row + 2, col_index + 1,
                                        updated_value)  # Google Sheets'te hücreyi güncelle
            # self.timer.start(60000)

    def back_menu(self):
        if self.current_user[2] == "admin":
            from admin_menu import UserAdminPreferencePage
            self.hide()
            self.menu_admin = UserAdminPreferencePage(self.current_user)
            self.menu_admin.show()
        else:
            from user_menu import UserPreferencePage
            self.hide()
            self.menu_user = UserPreferencePage(self.current_user)
            self.menu_user.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = MentorPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

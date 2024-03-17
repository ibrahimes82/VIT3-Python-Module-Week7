from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from applications_ui import Ui_Form
from mentor_menu import MentorMenuPage
import gspread


def folders(folder_name):
    credentials = 'key.json'
    gc = gspread.service_account(filename=credentials)
    spreadsheet_users = gc.open(folder_name)
    worksheet_users = spreadsheet_users.get_worksheet(0)
    users = worksheet_users.get_all_values()
    users.pop(0)
    return users


class ApplicationsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.applicationsForm = Ui_Form()
        self.applicationsForm.setupUi(self)
        self.users = folders('Basvurular')

        self.applicationsForm.pushButton_app_search.clicked.connect(self.search_app)
        self.applicationsForm.pushButton_app_all_app.clicked.connect(self.app_all_app)
        self.applicationsForm.pushButton_app_planned_mentor.clicked.connect(self.planned_mentor_app)
        self.applicationsForm.pushButton_app_unscheduled_meeting.clicked.connect(self.unscheduled)
        self.applicationsForm.pushButton_app_pre_vit_control.clicked.connect(self.vits_and_applications)
        self.applicationsForm.pushButton_app_rep_registrations.clicked.connect(self.rep_registrations)
        self.applicationsForm.pushButton_diff_registration.clicked.connect(self.search_app)
        self.applicationsForm.pushButton_app_back_menu.clicked.connect(self.preferences_app)
        self.applicationsForm.pushButton_app_filter_app.clicked.connect(self.search_app)
        self.applicationsForm.pushButton_app_exit.clicked.connect(self.exit)

    def write2table(self, my_list):
        table_widget = self.applicationsForm.tableWidget_app
        table_widget.setRowCount(len(my_list))
        for row_index, item in enumerate(my_list):
            for col_index, data in enumerate(item):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def search_app(self):
        search_users = []
        self.users = folders('Basvurular')
        for user in self.users:
            if self.applicationsForm.lineEdit_app_username.text().lower() in user[1].lower() \
                    and self.applicationsForm.lineEdit_app_username.text().lower() != '':
                search_users.append(user)

        if search_users:
            return self.write2table(search_users)
        else:
            return self.write2table([['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]])

    def write3table(self, my_list, excluded_column_index):
        table_widget = self.applicationsForm.tableWidget_app
        table_widget.setRowCount(len(my_list))
        for row_index, item in enumerate(my_list):
            row_data = [item[i] for i in range(len(item)) if i != excluded_column_index]
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def app_all_app(self):
        self.write2table(self.users)
        self.write3table(self.users, 7)

    def planned_and_unscheduled(self, search_text):
        search_users = []
        for user in self.users:
            if search_text in user[20]:
                search_users.append(user)
        self.users = folders('Basvurular')
        if search_users:
            return self.write2table(search_users)
        else:
            return self.write2table([['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]])

    def planned_mentor_app(self):
        self.planned_and_unscheduled("OK")

    def unscheduled(self):
        self.planned_and_unscheduled("ATANMADI")

    def commen(self):
        common_users = []
        applications = {user[1] for user in folders('Basvurular')}
        vits1 = {user[1] for user in folders('VIT1')}
        vits2 = {user[1] for user in folders('VIT2')}
        common_users = [user for user in applications if user in vits1 and user in vits2]
        return common_users

    def vits_and_applications(self):
        search_users = []
        self.users = folders('Basvurular')
        common_users = self.commen()
        for user in self.users:
            for common_user in common_users:
                if common_user in user[1]:
                    search_users.append(user)
                    break
        if search_users:
            return self.write3table(search_users, 7)
        else:

            return self.write2table([['Kullanıcı veya Mentor Bulunamadı!', '-', '-', '-', '-', '-', '-', '-']])

    def rep_registrations(self):
        vits_common = []
        vits1 = {user[1] for user in folders('VIT1')}
        vits2 = {user[1] for user in folders('VIT2')}
        vits_common = [user for user in vits1 if user in vits2]
        pass

    def preferences_app(self):
        MentorMenuPage.back_menu(self)

    def exit(self):
        self.close()

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
import gspread

import main
from applications_ui import Ui_FormApplications


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)
        self.users = main.connection_hub('key.json', 'Basvurular')

        self.menu_user = None
        self.menu_admin = None

        self.form_applications.pushButton_app_search.clicked.connect(self.search_app)
        self.form_applications.pushButton_app_all_app.clicked.connect(self.app_all_app)
        self.form_applications.pushButton_app_planned_mentor.clicked.connect(self.planned_mentor_app)
        self.form_applications.pushButton_app_unscheduled_meeting.clicked.connect(self.unscheduled)
        self.form_applications.pushButton_app_pre_vit_control.clicked.connect(self.vits_and_applications)
        self.form_applications.pushButton_app_rep_registrations.clicked.connect(self.rep_registrations)
        self.form_applications.pushButton_diff_registration.clicked.connect(self.diff_registrations)
        self.form_applications.pushButton_app_back_menu.clicked.connect(self.back_menu)
        self.form_applications.pushButton_app_filter_app.clicked.connect(self.filter_applications)
        self.form_applications.pushButton_app_exit.clicked.connect(self.app_exit)

    def write2table(self, my_list):
        table_widget = self.form_applications.tableWidget_app
        table_widget.setRowCount(len(my_list))
        for row_index, item in enumerate(my_list):
            for col_index, data in enumerate(item):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def search_app(self):
        search_users = []
        for user in self.users[1:]:
            if self.form_applications.lineEdit_app_username.text().lower() in user[1].lower() \
                    and self.form_applications.lineEdit_app_username.text().lower() != '':
                search_users.append(user)

        if search_users:
            return self.write2table(search_users)
        else:
            return self.write2table([['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ]])

    def write3table(self, my_list, excluded_column_index):
        table_widget = self.form_applications.tableWidget_app
        table_widget.setRowCount(len(my_list))
        for row_index, item in enumerate(my_list):
            row_data = [item[i] for i in range(len(item)) if i != excluded_column_index]
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def app_all_app(self):
        self.write2table(self.users[1:])
        self.write3table(self.users[1:], 7)

    def planned_and_unscheduled(self, text):
        searched_users = []
        for user in self.users[1:]:
            if text in user[20]:
                searched_users.append(user)
        if searched_users:
            return self.write3table(searched_users, 7)
        else:
            return self.write3table([['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]])

    def planned_mentor_app(self):
        self.planned_and_unscheduled("OK")

    def unscheduled(self):
        self.planned_and_unscheduled('ATANMADI')
        # self.write3table(self.users, 7)

    def commen(self):
        common_users = []
        applications = {user[1] for user in self.users[1:]}
        vits1 = {user[1] for user in main.connection_hub('key.json', 'VIT1')}
        vits2 = {user[1] for user in main.connection_hub('key.json', 'VIT2')}
        common_users = [user for user in applications if user in vits1 and user in vits2]
        return common_users

    def vits_and_applications(self):
        search_users = []
        common_users = self.commen()
        for user in self.users[1:]:
            for common_user in common_users:
                if common_user in user[1]:
                    search_users.append(user)
                    break
        if search_users:
            return self.write3table(search_users, 7)
        else:

            return self.write2table([['Kullanıcı veya Mentor Bulunamadı!', '-', '-', '-', '-', '-', '-', '-']])

    def vit1_vit2(self):
        vits_common = []
        vits1 = {user[1] for user in main.connection_hub('key.json', 'VIT1')}
        vits2 = {user[1] for user in main.connection_hub('key.json', 'VIT2')}
        vits_common = [user for user in vits1 if user in vits2]
        return vits_common

    def rep_registrations(self):
        search_users = []
        vit1_users = main.connection_hub('key.json', 'VIT1')
        vits_common = self.vit1_vit2()
        for user in vit1_users[1:]:
            for common_user in vits_common:
                if common_user in user[1]:
                    search_users.append(user)
                    break
        if search_users:
            return self.write3table(search_users, 7)
        else:

            return self.write2table([['Kullanıcı veya Mentor Bulunamadı!', '-', '-', '-', '-', '-', '-', '-']])

    def diff_registrations(self):
        vit1_users = main.connection_hub('key.json', 'VIT1')
        vit2_users = main.connection_hub('key.json', 'VIT2')

        different_users = []
        for user1 in vit1_users:
            found = False
            for user2 in vit2_users:
                if user1[1] == user2[1]:
                    found = True
                    break
            if not found:
                different_users.append(user1)

        for user2 in vit2_users:
            found = False
            for user1 in vit1_users:
                if user1[1] == user2[1]:
                    found = True
                    break
            if not found:
                different_users.append(user2)

        self.write2table(different_users)
        self.write3table(different_users, 7)

    def filter_applications(self):
        applications = self.users[1:]
        unique_names = set()
        filtered_applications = []
        for application in applications:
            if application[1] not in unique_names:
                filtered_applications.append(application)
                unique_names.add(application[1])

        self.write2table(filtered_applications)
        self.write3table(filtered_applications, 7)

    def back_menu(self):
        if self.current_user[2] == "admin":
            from admin_menu import AdminMenuPage
            self.hide()
            self.menu_admin = AdminMenuPage(self.current_user)
            self.menu_admin.show()
        else:
            from user_menu import UserMenuPage
            self.hide()
            self.menu_user = UserMenuPage(self.current_user)
            self.menu_user.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = ApplicationsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

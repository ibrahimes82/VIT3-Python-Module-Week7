from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.applications_ui import Ui_FormApplications


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)
        self.applications = main.connection_hub('credentials/key.json', 'Basvurular')

        #   This is a special code list manipulation for "total applications"
        #   You can change the wanted columns for tableWidget here
        #
        #
        excluding_list = [x for x in range(21, 27)]     # Unwanted columns
        new_list = main.list_exclude(list(self.applications), excluding_list)
        self.applications = new_list
        #
        #
        #
        #

        self.menu_user = None
        self.menu_admin = None

        self.form_applications.pushButtonSearch.clicked.connect(self.app_search)
        self.form_applications.pushButtonAllApplications.clicked.connect(self.app_all_applications)
        self.form_applications.pushButtonPlannedMeetings.clicked.connect(self.app_planned_meetings)
        self.form_applications.pushButtonUnscheduledMeeting.clicked.connect(self.app_unscheduled_meetings)
        self.form_applications.pushButtonPreviousVitCheck.clicked.connect(self.app_previous_vits_check)
        self.form_applications.pushButtonDuplicateRegistrations.clicked.connect(self.app_duplicate_records)
        self.form_applications.pushButtonDifferentialRegistrations.clicked.connect(self.app_differential_registrations)
        self.form_applications.pushButtonFilterApplications.clicked.connect(self.app_filter_applications)
        self.form_applications.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_applications.pushButtonExit.clicked.connect(self.app_exit)

    def app_search(self):
        searched_applications = [self.applications[0]]
        for application in self.applications[1:]:
            if self.form_applications.lineEditSearch.text().lower() in application[1].lower() and self.form_applications.lineEditSearch.text().lower() != '':
                searched_applications.append(application)

        # Make empty the search area
        self.form_applications.lineEditSearch.setText('')

        if len(searched_applications) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['No User or Mentor Found!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            searched_applications.append(no_application)
            # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, searched_applications)

    def app_all_applications(self):
        main.write2table(self.form_applications, self.applications)

    # This method is for next two method
    def app_column_checker(self, text, col):
        searched_applications = []
        for application in self.applications[1:]:
            if text in application[col]:
                searched_applications.append(application)
        return searched_applications

    def app_planned_meetings(self):
        planned_applications = self.app_column_checker("OK", 20)
        if planned_applications:
            main.write2table(self.form_applications, planned_applications)
        else:
            return main.write2table(self.form_applications,
                                    [['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]], )

    def app_unscheduled_meetings(self):
        unscheduled_applications = self.app_column_checker("ATANMADI", 20)
        if unscheduled_applications:
            main.write2table(self.form_applications, unscheduled_applications)
        else:
            return main.write2table(self.form_applications,
                                    [['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ]], )

    def app_duplicate_records(self):
        unique_list = []
        duplicate_list = [self.applications[0]]
        for application in self.applications[1:]:
            if application not in unique_list:
                unique_list.append(application)
            else:
                duplicate_list.append(application)
        main.write2table(self.form_applications, duplicate_list)

    def app_previous_vits_check(self):
        pass

    # def common(self):
    #     applications = {[application[1], application[2]] for application in self.applications[1:]}
    #     vits1 = {user[1] for user in main.connection_hub('credentials/key.json', 'VIT1')}
    #     vits2 = {user[1] for user in main.connection_hub('credentials/key.json', 'VIT2')}
    #     common_users = [user for user in applications if user in vits1 and user in vits2]
    #     return common_users
    #
    # def vits_and_applications(self):
    #     search_users = []
    #     common_users = self.common()
    #     for user in self.applications[1:]:
    #         for common_user in common_users:
    #             if common_user in user[1]:
    #                 search_users.append(user)
    #                 break
    #     if search_users:
    #         return self.list_exclude(search_users, 7)
    #     else:
    #
    #         return main.write2table(self.form_applications,
    #                                 [['Kullanıcı veya Mentor Bulunamadı!', '-', '-', '-', '-', '-', '-', '-']])
    #
    # def vit1_vit2(self):
    #     vits_common = []
    #     vits1 = {user[1] for user in main.connection_hub('credentials/key.json', 'VIT1')}
    #     vits2 = {user[1] for user in main.connection_hub('credentials/key.json', 'VIT2')}
    #     vits_common = [user for user in vits1 if user in vits2]
    #     return vits_common
    #
    # def rep_registrations(self):
    #     search_users = []
    #     vit1_users = main.connection_hub('credentials/key.json', 'VIT1')
    #     vits_common = self.vit1_vit2()
    #     for user in vit1_users[1:]:
    #         for common_user in vits_common:
    #             if common_user in user[1]:
    #                 search_users.append(user)
    #                 break
    #     if search_users:
    #         return self.list_exclude(search_users, 7)
    #     else:
    #
    #         return main.write2table(self.form_applications,
    #                                 [['Kullanıcı veya Mentor Bulunamadı!', '-', '-', '-', '-', '-', '-', '-']])

    def app_differential_registrations(self):
        vit1_users = main.connection_hub('credentials/key.json', 'VIT1')
        vit2_users = main.connection_hub('credentials/key.json', 'VIT2')

        differential_users = [vit1_users[0]]
        for user1 in vit1_users:
            found = False
            for user2 in vit2_users:
                if user1[1] == user2[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user1)

        for user2 in vit2_users:
            found = False
            for user1 in vit1_users:
                if user1[1] == user2[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user2)

        main.write2table(self.form_applications, differential_users)

    def app_filter_applications(self):
        applications = self.applications[1:]
        unique_names = set()
        filtered_applications = []
        for application in applications:
            if application[1] not in unique_names:
                filtered_applications.append(application)
                unique_names.add(application[1])
        main.write2table(self.form_applications, filtered_applications)

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
    main_window = ApplicationsPage(['s', 'd', 'user'])
    main_window.show()
    app.exec()

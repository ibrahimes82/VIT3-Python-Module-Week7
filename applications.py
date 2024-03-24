from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.applications_ui import Ui_FormApplications


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.worksheet = None
        self.VIT1 = None
        self.VIT2 = None
        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)
        self.worksheet = main.connection_hub('credentials/key.json', 'Basvurular', 'Sayfa1')
        self.applications = self.worksheet.get_all_values()

        #   This is a special code list manipulation for "total applications"
        #   You can change the wanted columns for tableWidget here
        #
        #
        excluding_list = [x for x in range(21, 27)]  # Unwanted columns
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
        excluding_list = [x for x in range(21, 27)]  # Unwanted columns
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        new_vit1 = main.list_exclude(list(self.VIT1), excluding_list)
        self.VIT1 = new_vit1[1:]
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()
        new_vit2 = main.list_exclude(list(self.VIT2), excluding_list)
        self.VIT2 = new_vit2[1:]

        double_applicants = [self.applications[0]]
        for user in self.VIT1:
            if self.find_same(self.applications, user):
                double_applicants.append(user)
            elif self.find_same(self.VIT2, user):
                double_applicants.append(user)
            else:
                continue

        for user in self.VIT2:
            if self.find_same(self.applications, user):
                double_applicants.append(user)
###############################
        data = []
        newlist = [self.applications[0]]
        for row in double_applicants[1:]:
            data.append(row[1])
        data = sorted(data)
        for d in data:
            for i in double_applicants[1:]:
                if d == i[1]:
                    newlist.append(i)

        if len(newlist) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['There is no double applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            newlist.append(no_application)
            # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, newlist)

        # if len(double_applicants) > 1:  # If the searched_people variable is not empty!
        #     pass
        # else:
        #     no_application = ['There is no double applicant!']
        #     [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
        #     double_applicants.append(no_application)
        #     # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
        #     # Above - one line - code works as same as active code. But active code is automated for cell amount
        # return main.write2table(self.form_applications, double_applicants)

    @staticmethod
    def find_same(a_list, element):
        for i in a_list:
            if element[1] in i[1] and element[2] in i[2]:
                return True
        else:
            return False

    def app_differential_registrations(self):
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        vit1_users = self.worksheet.get_all_values()
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()
        vit2_users = self.worksheet.get_all_values()

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

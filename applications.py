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
        self.excluding_list = [x for x in range(21, 27)]  # Unwanted columns
        new_list = main.list_exclude(list(self.applications), self.excluding_list)
        self.applications = new_list
        #
        #
        #
        # This code updates the tableWidget headers
        main.write2table(self.form_applications, main.list_exclude([self.applications[0]], self.excluding_list))

        self.menu_user = None
        self.menu_admin = None

        self.form_applications.pushButtonSearch.clicked.connect(self.app_search)
        self.form_applications.pushButtonAllApplications.clicked.connect(self.app_all_applications)
        self.form_applications.pushButtonPlannedMeetings.clicked.connect(self.app_planned_meetings)
        self.form_applications.pushButtonUnscheduledMeeting.clicked.connect(self.app_unscheduled_meetings)
        self.form_applications.pushButtonPreviousVitCheck.clicked.connect(self.app_previous_application_check)
        self.form_applications.pushButtonDuplicateRegistrations.clicked.connect(self.app_duplicate_records)
        self.form_applications.pushButtonDifferentialRegistrations.clicked.connect(self.app_differential_registrations)
        self.form_applications.pushButtonFilterApplications.clicked.connect(self.app_filter_applications)
        self.form_applications.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_applications.pushButtonExit.clicked.connect(self.app_exit)

    def app_search(self):
        searched_applications = [self.applications[0]]
        for application in self.applications[1:]:
            if self.form_applications.lineEditSearch.text().lower() in \
                    application[1].lower() and self.form_applications.lineEditSearch.text().lower() != '':
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
    @staticmethod
    def app_column_checker(a_list, text, col):
        searched_applications = []
        for application in a_list[1:]:
            if text in application[col]:
                searched_applications.append(application)
        return searched_applications

    def app_planned_meetings(self):
        planned_applications = [self.applications[0]]
        planned_applications.extend(self.app_column_checker(self.applications, "OK", 20))
        if len(planned_applications) > 1:  # If the unscheduled_applications variable is not empty!
            pass
        else:
            no_application = ['There is no planned meetings!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            planned_applications.append(no_application)
            # planned_applications.append(['There is no planned meetings!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, planned_applications)

    def app_unscheduled_meetings(self):
        unscheduled_applications = [self.applications[0]]
        unscheduled_applications.extend(self.app_column_checker(self.applications, "ATANMADI", 20))
        if len(unscheduled_applications) > 1:  # If the unscheduled_applications variable is not empty!
            pass
        else:
            no_application = ['There is no unscheduled meetings!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            unscheduled_applications.append(no_application)
            # unscheduled_applications.append(['There is no unscheduled meetings!', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, unscheduled_applications)

    def app_duplicate_records(self):
        unique_list = []
        duplicate_list = [self.applications[0]]
        for application in self.applications[1:]:
            if application not in unique_list:
                unique_list.append(application)
            else:
                duplicate_list.append(application)
        main.write2table(self.form_applications, duplicate_list)

    # This method will be used in next method only
    # This method finds common elements in two lists with given properties
    @staticmethod
    def find_common_elements(nested_list1, nested_list2):
        common_elements = []
        for sublist1 in nested_list1:
            for sublist2 in nested_list2:
                if (sublist1[1].strip().lower() in sublist2[1].strip().lower() or sublist2[1].strip().lower() in
                        sublist1[1].strip().lower() or sublist1[2].strip().lower() == sublist2[2].strip().lower()):
                    common_elements.append(sublist1)
                    common_elements.append(sublist2)
        return common_elements

    # !!! Explanations for program user, not for developers: This method(below method with above method's help)
    # finds users that apply with the same email or the same name before
    def app_previous_application_check(self):
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        self.VIT1 = main.list_exclude(list(self.VIT1), self.excluding_list)
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()
        self.VIT2 = main.list_exclude(list(self.VIT2), self.excluding_list)

        double_applicants = [self.applications[0]]  # Adding headers to the list

        double_applicants.extend(self.find_common_elements(self.VIT1[1:], self.VIT2[1:]))
        double_applicants.extend(self.find_common_elements(self.VIT1[1:], self.applications[1:]))
        double_applicants.extend(self.find_common_elements(self.VIT2[1:], self.applications[1:]))

        unique_list = []
        [unique_list.append(x) for x in double_applicants if x not in unique_list]
        double_applicants = unique_list

        # These codes(below) are my first codes. I improved new codes above later with help of chatgpt.
        #
        # for user in self.VIT1:
        #     if self.find_same(self.applications, user):
        #         double_applicants.append(user)
        #     elif self.find_same(self.VIT2, user):
        #         double_applicants.append(user)
        #     else:
        #         continue
        #
        # for user in self.VIT2:
        #     if self.find_same(self.applications, user):
        #         double_applicants.append(user)
        #
        #
        # @staticmethod
        # def find_same(a_list, element):
        #     for i in a_list:
        #         if element[1] in i[1] and element[2] in i[2]:
        #             return True
        #     else:
        #         return False

        # The code below reorders the list according to the data in the first index of the elements of the relevant
        # nested list.
        sorted_list = sorted(double_applicants, key=lambda x: x[1].lower())

        if len(sorted_list) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['There is no double applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            sorted_list.append(no_application)
            # sorted_list.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, sorted_list)

    def app_differential_registrations(self):
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()

        differential_users = [self.applications[0]]
        for user1 in self.VIT1[1:]:
            found = False
            for user2 in self.VIT2[1:]:
                if user1[1] in user2[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user1)

        for user2 in self.VIT2:
            found = False
            for user1 in self.VIT1:
                if user2[1] in user1[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user2)

        if len(differential_users) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['There is no differential applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            differential_users.append(no_application)
            # differential_users.append(['There is no differential applicant!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, differential_users)

    def app_filter_applications(self):
        filtered_unique_applications = [self.applications[0]]
        unique_names = set()
        for application in self.applications[1:]:
            if application[1].strip().lower() not in unique_names:
                filtered_unique_applications.append(application)
                unique_names.add(application[1].strip().lower())
        if len(filtered_unique_applications) > 1:  # If the filtered_unique_applications variable is not empty!
            pass
        else:
            no_application = ['There is no application!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            filtered_unique_applications.append(no_application)
            # filtered_unique_applications.append(['There is no application!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, filtered_unique_applications)

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

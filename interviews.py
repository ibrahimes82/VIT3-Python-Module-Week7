from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.interviews_ui import Ui_FormInterviews


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)

        self.worksheet = main.connection_hub('credentials/key.json', 'Mulakatlar', 'Sayfa1')
        self.interviews = self.worksheet.get_all_values()
        main.write2table(self.form_interviews, [self.interviews[0]])  # This code updates the tableWidget headers
        self.menu_admin = None
        self.menu_user = None

        self.form_interviews.pushButtonSearch.clicked.connect(self.search_name)
        self.form_interviews.lineEditUsername.returnPressed.connect(self.search_name)
        self.form_interviews.pushButtonSubmittedProjects.clicked.connect(self.get_submitted_projects)
        self.form_interviews.pushButtonProjectArrivals.clicked.connect(self.get_projects_arrivals)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)

    def search_name(self):
        searched_people = [self.interviews[0]]
        for person in self.interviews[1:]:
            # If the text in the textbox appears within one of the names in the list AND is not empty at the same time!
            if self.form_interviews.lineEditUsername.text().lower() in str(person[0]).lower() and self.form_interviews.lineEditUsername.text() != '':
                searched_people.append(person)

        # Make empty the search area
        self.form_interviews.lineEditUsername.setText('')

        if len(searched_people) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_user = ['No User Found!']
            [no_user.append('-') for i in range(len(self.interviews[0]) - 1)]
            searched_people.append(no_user)
            # searched_people.append(['No user found!', '-', '-'])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_interviews, searched_people)

    def get_submitted_projects(self):
        submitted_projects = [self.interviews[0]]
        for i in self.interviews[1:]:
            if i[1]:
                submitted_projects.append(i)
        return main.write2table(self.form_interviews, submitted_projects)

    def get_projects_arrivals(self):
        projects_arrivals = [self.interviews[0]]
        for i in self.interviews[1:]:
            if i[2]:
                projects_arrivals.append(i)
        return main.write2table(self.form_interviews, projects_arrivals)

    def back_menu(self):
        if self.current_user[2] == "admin":
            from admin_menu import AdminMenuPage
            self.hide()
            self.menu_admin = AdminMenuPage(self.current_user)
            self.menu_admin.show()
        else:
            from menu import UserMenuPage
            self.hide()
            self.menu_user = UserMenuPage(self.current_user)
            self.menu_user.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

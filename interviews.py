from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from interviews_ui import Ui_FormInterviews


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)

        self.interviews = main.connection_hub('key.json', 'Mulakatlar')
        self.menu_admin = None
        self.menu_user = None

        self.form_interviews.pushButtonSearch.clicked.connect(self.search_name)
        self.form_interviews.pushButtonSubmittedProjects.clicked.connect(self.get_submitted_projects)
        self.form_interviews.pushButtonProjectArrivals.clicked.connect(self.get_projects_arrivals)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)
        self.form_interviews.lineEditUsername.returnPressed.connect(self.search_name)

    def write2table(self, a_list):
        table_widget = self.form_interviews.tableWidget
        # Tabloyu temizle
        table_widget.clearContents()
        # Tabloya başlık ekle
        table_widget.setColumnCount(len(self.interviews[0]))
        table_widget.setHorizontalHeaderLabels(self.interviews[0])
        # Tabloyu doldur
        table_widget.setRowCount(len(a_list))
        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                table_widget.setItem(i, j, item)
        return True

    def search_name(self):
        searched_people = []
        for person in self.interviews[1:]:
            # If the text in the textbox appears within one of the names in the list AND is not empty at the same time!
            if self.form_interviews.lineEditUsername.text().lower() in str(person[0]).lower() and self.form_interviews.lineEditUsername.text() != '':
                searched_people += [person]

        # Make empty the search area
        self.form_interviews.lineEditUsername.setText('')

        if searched_people:  # If the searched_people variable is not empty!
            return self.write2table(searched_people)
        else:
            return self.write2table([['No user found!', '-', '-']])

    def get_submitted_projects(self):
        submitted_projects = self.interviews[1:]
        for i in submitted_projects:
            if not i[1]:
                submitted_projects.remove(i)
        return self.write2table(submitted_projects)

    def get_projects_arrivals(self):
        projects_arrivals = self.interviews[1:]
        for i in projects_arrivals:
            if not i[2]:
                projects_arrivals.remove(i)
        return self.write2table(projects_arrivals)

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
    main_window = InterviewsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

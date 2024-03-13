from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
import gspread

import login as lgn
from interviews_ui import Ui_FormInterviews

credentials = 'key.json'
gc = gspread.service_account(filename=credentials)
spreadsheet_users = gc.open('Mulakatlar')
worksheet_interviews = spreadsheet_users.get_worksheet(0)
interviews = worksheet_interviews.get_all_values()
interviews.pop(0)


class InterviewsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.interviews_form = Ui_FormInterviews()
        self.interviews_form.setupUi(self)

        self.interviews_form.pushButtonSearch.clicked.connect(self.search_name)
        self.interviews_form.pushButtonSubmittedProjects.clicked.connect(self.get_submitted_projects)
        self.interviews_form.pushButtonProjectArrivals.clicked.connect(self.get_projects_arrivals)
        #self.interviews_form.pushButtonPreferences.clicked.connect(lgn.LoginPage.back2menu(lgn.LoginPage.active_user))
        self.interviews_form.pushButtonExit.clicked.connect(self.app_exit)

    def write2table(self, a_list):
        table_widget = self.interviews_form.tableWidget
        table_widget.setRowCount(len(a_list))
        for row_index, item in enumerate(a_list):
            for col_index, data in enumerate(item):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_index, col_index, item)
        return True

    def search_name(self):
        searched_people = []
        for person in interviews:
            # If the text in the textbox appears within one of the names in the list AND is not empty at the same time!
            if self.interviews_form.lineEditUsername.text() in person[0] and self.interviews_form.lineEditUsername.text() != '':
                searched_people += [person]

        if searched_people:     # If the searched_people variable is not empty!
            return self.write2table(searched_people)
        else:
            return self.write2table([['No user found!', '-', '-']])

    def get_submitted_projects(self):
        submitted_projects = interviews
        for i in submitted_projects:
            if not i[1]:
                submitted_projects.remove(i)
        return self.write2table(submitted_projects)

    def get_projects_arrivals(self):
        projects_arrivals = interviews
        for i in projects_arrivals:
            if not i[2]:
                projects_arrivals.remove(i)
        return self.write2table(projects_arrivals)

    def app_exit(self):
        self.close()







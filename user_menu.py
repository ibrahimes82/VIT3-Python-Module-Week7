from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from user_menu_ui import Ui_Form
from applications import ApplicationsPage
from interviews import InterviewsPage
from mentor_menu import MentorMenuPage


class UserPreferencePage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.user_menu_form = Ui_Form()
        self.user_menu_form.setupUi(self)
        self.user_menu_form.labelAccountName.setText(str(current_user[0]).split(' ')[0])

        self.login_window = None
        self.applications_window_open = ApplicationsPage()
        self.interviews_window_open = None
        self.mentor_menu_open = MentorMenuPage()

        self.user_menu_form.pushButtonInterviews.clicked.connect(self.inter_in)
        self.user_menu_form.pushButtonApplications.clicked.connect(self.app_in)
        self.user_menu_form.pushButtonMentorMeeting.clicked.connect(self.mentor_in)
        self.user_menu_form.pushButtonSignOut.clicked.connect(self.logpage_in)
        self.user_menu_form.pushButtonExit.clicked.connect(self.exit_in)

    def app_in(self):
        self.hide()
        self.applications_window_open.show()

    def inter_in(self):
        self.hide()
        self.interviews_window_open = InterviewsPage(self.current_user)
        self.interviews_window_open.show()

    def exit_in(self):
        self.close()
        
    def logpage_in(self):
        from login import LoginPage
        self.hide()
        self.login_window = LoginPage()
        self.login_window.show()
        
    def mentor_in(self):
        self.hide()
        self.mentor_menu_open.show()
        

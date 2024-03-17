
from PyQt6.QtWidgets import QWidget
from admin_menu_ui import Ui_Form
from applications import ApplicationsPage
from interviews import InterviewsPage
from mentor_menu import MentorMenuPage
from main_admin_menu import MainAdminMenuPage


class UserAdminPreferencePage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.loginwindow = None
        self.current_user = current_user
        self.useradminform = Ui_Form()
        self.useradminform.setupUi(self)
        self.applicationswindow_open = ApplicationsPage()
        self.interviewswindow_open = InterviewsPage(self.current_user)
        self.mentormenu_open = MentorMenuPage()
        self.mainadminmenu_open = MainAdminMenuPage()
        self.useradminform.pushButton_user_admin_applications.clicked.connect(self.app_in)
        self.useradminform.pushButton_user_admin_interviews.clicked.connect(self.inter_in)
        self.useradminform.pushButton_user_admin_exit.clicked.connect(self.exit_in)
        self.useradminform.pushButton_user_admin_login_page.clicked.connect(self.logpage_in)
        self.useradminform.pushButton_user_admin_mentor_meeting.clicked.connect(self.mentor_in)
        self.useradminform.pushButton_user_admin_menu.clicked.connect(self.adminmenu_in)

    def app_in(self):
        self.hide()
        self.applicationswindow_open.show()

    def inter_in(self):
        self.hide()
        self.interviewswindow_open = InterviewsPage(self.current_user)
        self.interviewswindow_open.show()

    def exit_in(self):
        self.close()

    def logpage_in(self):
        from login import LoginPage
        self.hide()
        self.loginwindow = LoginPage()
        self.loginwindow.show()

    def mentor_in(self):
        self.hide()
        self.mentormenu_open.show()

    def adminmenu_in(self):
        self.close()
        self.mainadminmenu_open.show()

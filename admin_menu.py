from PyQt6.QtWidgets import QWidget
from admin_menu_ui import Ui_FormAdminMenu


class AdminMenuPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.admin_menu_form = Ui_FormAdminMenu()
        self.admin_menu_form.setupUi(self)
        self.admin_menu_form.labelCurrentUser.setText(str(self.current_user[0]).split(' ')[0])

        self.login_window = None
        self.applications_window_open = None
        self.interviews_window_open = None
        self.mentor_menu_open = None
        self.management_menu_open = None

        self.admin_menu_form.pushButtonInterviews.clicked.connect(self.inter_in)
        self.admin_menu_form.pushButtonApplications.clicked.connect(self.app_in)
        self.admin_menu_form.pushButtonMentorMeeting.clicked.connect(self.mentor_in)
        self.admin_menu_form.pushButtonSignOut.clicked.connect(self.logpage_in)
        self.admin_menu_form.pushButtonExit.clicked.connect(self.exit_in)
        self.admin_menu_form.pushButtonManagement.clicked.connect(self.adminmenu_in)

    def app_in(self):
        from applications import ApplicationsPage
        self.hide()
        self.applications_window_open = ApplicationsPage(self.current_user)
        self.applications_window_open.show()

    def inter_in(self):
        from interviews import InterviewsPage
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
        from mentor_menu import MentorPage
        self.hide()
        self.mentor_menu_open = MentorPage(self.current_user)
        self.mentor_menu_open.show()

    def adminmenu_in(self):
        from management import ManagementPage
        self.close()
        self.management_menu_open = ManagementPage(self.current_user)
        self.management_menu_open.show()

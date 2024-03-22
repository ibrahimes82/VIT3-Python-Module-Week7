from PyQt6.QtWidgets import QWidget, QApplication

from UI_Files.admin_menu_ui import Ui_FormAdminMenu


class AdminMenuPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.admin_menu_form = Ui_FormAdminMenu()
        self.admin_menu_form.setupUi(self)
        self.admin_menu_form.labelCurrentUser.setText(str(self.current_user[0]).split(' ')[0])

        self.settings_window_open = None
        self.login_window = None
        self.applications_window_open = None
        self.interviews_window_open = None
        self.mentor_menu_open = None
        self.management_menu_open = None

        self.admin_menu_form.toolButtonAccount.clicked.connect(self.go_settings_page)
        self.admin_menu_form.pushButtonInterviews.clicked.connect(self.go_interviews_page)
        self.admin_menu_form.pushButtonApplications.clicked.connect(self.go_applications_page)
        self.admin_menu_form.pushButtonMentorMeeting.clicked.connect(self.go_mentors_page)
        self.admin_menu_form.pushButtonManagement.clicked.connect(self.go_management_page)
        self.admin_menu_form.pushButtonSignOut.clicked.connect(self.goback_login_page)
        self.admin_menu_form.pushButtonExit.clicked.connect(self.app_exit)

    def go_settings_page(self):
        from settings import SettingsPage
        self.settings_window_open = SettingsPage(self.current_user)
        self.settings_window_open.show()

    def go_mentors_page(self):
        from mentors import MentorPage
        self.hide()
        self.mentor_menu_open = MentorPage(self.current_user)
        self.mentor_menu_open.show()

    def go_applications_page(self):
        from applications import ApplicationsPage
        self.hide()
        self.applications_window_open = ApplicationsPage(self.current_user)
        self.applications_window_open.show()

    def go_interviews_page(self):
        from interviews import InterviewsPage
        self.hide()
        self.interviews_window_open = InterviewsPage(self.current_user)
        self.interviews_window_open.show()

    def go_management_page(self):
        from management import ManagementPage
        self.close()
        self.management_menu_open = ManagementPage(self.current_user)
        self.management_menu_open.show()

    def goback_login_page(self):
        from login import LoginPage
        self.hide()
        self.login_window = LoginPage()
        self.login_window.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = AdminMenuPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

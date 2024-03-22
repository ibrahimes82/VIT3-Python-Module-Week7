from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.mentors_ui import Ui_FormMentor


class MentorPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.form_mentor = Ui_FormMentor()
        self.form_mentor.setupUi(self)
        self.form_mentor.comboBoxFilterOptions.setPlaceholderText("Katılımcı Hakkındaki Tavsiyelere Göre Filtreleyin")

        self.mentees = main.connection_hub('credentials/key.json', 'Mentor')
        self.menu_user = None
        self.menu_admin = None

        self.form_mentor.pushButtonSearch.clicked.connect(self.search)
        self.form_mentor.lineEditSearch.returnPressed.connect(self.search)
        self.form_mentor.pushButtonGetAllApplications.clicked.connect(self.get_all_applications)
        self.form_mentor.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        self.form_mentor.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_mentor.pushButtonExit.clicked.connect(self.app_exit)
        self.form_mentor.comboBoxFilterOptions.addItems(self.filter_options)

    @property
    def filter_options(self, index=4):
        option_elements = []
        for row in self.mentees[1:]:
            option_elements.append(str(row[index]).strip())
        filter_options = list(set(option_elements))
        filter_options.sort()
        filter_options.remove('Diger')
        filter_options.append('Diger')
        return filter_options

    def search(self):
        searched_mentees = [self.mentees[0]]
        for mentee in self.mentees[1:]:
            if (self.form_mentor.lineEditSearch.text().lower() in mentee[1].lower() or self.form_mentor.lineEditSearch.text().lower() in mentee[2].lower()) and self.form_mentor.lineEditSearch.text().lower() != '':
                searched_mentees.append(mentee)
        if len(searched_mentees) > 1:
            pass
        else:
            searched_mentees.append(['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ])
        return main.write2table(self.form_mentor, searched_mentees)

    def get_all_applications(self):
        main.write2table(self.form_mentor, self.mentees)

    def filter_table(self, index=4):
        filtered_data = [self.mentees[0]]
        selected_item = self.form_mentor.comboBoxFilterOptions.currentText()

        for row in self.mentees[1:]:

            if str(row[4]).lower().strip() == selected_item.lower().strip():
                filtered_data.append(row)
        main.write2table(self.form_mentor, filtered_data)

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
    main_window = MentorPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

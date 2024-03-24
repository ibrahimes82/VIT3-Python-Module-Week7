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

        # The number written here determines the column to be sorted in the combobox below.
        # Different filtering opportunities can be obtained by changing the application while it is running.
        self.filtering_column = 4
        self.form_mentor.comboBoxFilterOptions.setPlaceholderText("Katılımcı Hakkındaki Tavsiyelere Göre Filtreleyin")

        self.worksheet = main.connection_hub('credentials/key.json', 'Mentor', 'Sayfa1')
        self.mentees = self.worksheet.get_all_values()
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
    def filter_options(self):
        option_elements = []
        for row in self.mentees[1:]:
            option_elements.append(row[self.filtering_column].strip())
        filter_options = list(set(option_elements))
        filter_options.sort()
        # This(two rows which are below) is an issue that is inside the code, and it is in a specific language.
        # It must be changed while updating the application for any other language
        filter_options.remove('Diger')
        filter_options.append('Diger')
        return filter_options

    def search(self):
        searched_mentees = [self.mentees[0]]
        for mentee in self.mentees[1:]:
            if (self.form_mentor.lineEditSearch.text().lower() in mentee[
                1].lower() or self.form_mentor.lineEditSearch.text().lower() in mentee[
                    2].lower()) and self.form_mentor.lineEditSearch.text().lower() != '':
                searched_mentees.append(mentee)
        if len(searched_mentees) > 1:
            pass
        else:
            no_mentee = ['No User or Mentor Found!']
            [no_mentee.append('-') for i in range(len(self.mentees[0]) - 1)]
            searched_mentees.append(no_mentee)
            # searched_mentees.append(['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_mentor, searched_mentees)

    def get_all_applications(self):
        main.write2table(self.form_mentor, self.mentees)

    def filter_table(self):
        filtered_data = [self.mentees[0]]
        selected_item = self.form_mentor.comboBoxFilterOptions.currentText().strip()

        for row in self.mentees[1:]:
            if row[self.filtering_column].strip().lower() == selected_item.strip().lower():
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

from PyQt6.QtWidgets import QApplication, QTableWidgetItem
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connection_hub(credentials, table, worksheet_name):
    # Google Sheets API'ya erişim için kimlik doğrulama bilgileri
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
    client = gspread.authorize(creds)  # Kimlik doğrulama bilgileriyle oturum açma
    worksheet = client.open(table).worksheet(worksheet_name)  # Çalışma sayfasına erişim
    return worksheet


def write2table(page, a_list):
    table_widget = page.tableWidget
    table_widget.clearContents()  # Clear table
    table_widget.setColumnCount(len(a_list[0]))  # Add title to table
    table_widget.setHorizontalHeaderLabels(a_list[0])
    table_widget.setRowCount(len(a_list[1:]))  # Fill in the table
    for i, row in enumerate(a_list[1:]):
        for j, col in enumerate(row):
            item = QTableWidgetItem(str(col))
            table_widget.setItem(i, j, item)
    return True


def list_exclude(a_list, excluded_column_indexes):
    n_list = []
    for i, row in enumerate(a_list):
        item = []
        for j, col in enumerate(row):
            # if "column index" is inside our exclude list, come inside "if code block" and pass the loop.
            # don't add anything to item
            if j in excluded_column_indexes:
                continue
            # Otherwise add col to the item, which will become a row for new list
            item.append(col)
        n_list.append(item)  # add new item(row) to the new list
    return n_list


def filter_active_options(a_list, filtering_column):
    option_elements = []
    for row in a_list[1:]:
        option_elements.append(row[filtering_column].strip())
    filter_options = list(set(option_elements))

    if filter_options[0].isdigit():
        filter_options = sorted(filter_options, key=int)
    else:
        filter_options.sort()
    return filter_options


if __name__ == '__main__':
    from login import LoginPage

    app = QApplication([])
    window = LoginPage()
    window.show()
    app.exec()

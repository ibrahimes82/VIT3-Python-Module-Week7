import gspread
from PyQt6.QtWidgets import QApplication


def connection_hub(credentials, table):
    gc = gspread.service_account(filename=credentials)
    spreadsheet = gc.open(table)
    worksheet = spreadsheet.get_worksheet(0)
    items = worksheet.get_all_values()
    return items


if __name__ == '__main__':
    from login import LoginPage
    app = QApplication([])
    window = LoginPage()
    window.show()
    app.exec()

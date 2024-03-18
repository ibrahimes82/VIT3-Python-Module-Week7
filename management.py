from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QIcon
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import pickle
import os.path

from management_ui import Ui_Form

# Google Calendar API'deki yetkilendirme kapsamları
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.events.readonly',
          'https://www.googleapis.com/auth/calendar']


class ManagementMenuPage(QWidget, Ui_Form):
    def __init__(self, current_user):
        super().__init__()
        self.setupUi(self)
        self.current_user = current_user

        self.menu_user = None
        self.menu_admin = None

        self.setWindowIcon(QIcon("pictures/werhere_icon.png"))
        self.pushButton_mam_exit.clicked.connect(self.close)
        self.pushButton_mam_event_control.clicked.connect(self.get_calendar_events)
        self.pushButton_mam_send_mail.clicked.connect(self.send_invitations)

    def get_calendar_events(self):
        creds = self.get_credentials()

        # Google Calendar API ile etkileşim için hizmet oluştur
        service = build('calendar', 'v3', credentials=creds)

        # Bugünün tarihini al
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' işareti UTC zamanını belirtir

        # Takvim etkinliklerini al
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        self.events = events_result.get('items', [])  # events'i sınıf seviyesinde bir değişken olarak sakla

        # Etkinlikleri tabloya yerleştir
        self.tableWidget.setRowCount(0)  # Önceki verileri temizle
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_start = self.format_datetime(start)  # Tarih/saat formatlamasını yap
            attendees = event.get('attendees', [])
            participant_emails = ", ".join([attendee['email'] for attendee in attendees if attendee.get('email')])
            organizer_email = event['organizer'].get('email') if event.get('organizer') else 'Unknown'

            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                     QTableWidgetItem(event.get('summary', 'No Name')))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(formatted_start))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(participant_emails))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(organizer_email))

    def format_datetime(self, datetime_str):
        # Tarih ve saat değerini ISO formatından dönüştür
        datetime_obj = datetime.datetime.fromisoformat(datetime_str)
        # "gün-ay-yıl saat:dakika" formatında dönüştür
        formatted_datetime = datetime_obj.strftime("%d-%m-%Y %H:%M")
        return formatted_datetime

    def get_credentials(self):
        creds = None
        # Token dosyasını kontrol et
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Yetkilendirme yoksa veya geçersizse yeniden yetkilendirme yap
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Yeni yetkilendirme bilgilerini kaydet
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def send_invitations(self):
        creds = self.get_credentials()
        # Google Calendar API ile etkileşim için hizmet oluştur
        service = build('calendar', 'v3', credentials=creds)

        # Etkinlikler üzerinde döngü
        for event in self.events:
            # Katılımcıları alma
            attendees = event.get('attendees', [])
            participant_emails = [attendee['email'] for attendee in attendees if attendee.get('email')]
            # Etkinlik ID'sini alma
            event_id = event['id']
            # Organizer'ın e-posta adresini alma
            organizer_email = event['organizer'].get('email')
            # Davet e-postaları gönderme
            for email in participant_emails:
                try:
                    # Davet gönderme işlemi
                    updated_event = service.events().patch(calendarId='primary', eventId=event_id, sendUpdates='all',
                                                           body={'attendees': [{'email': email,
                                                                                'responseStatus': 'needsAction'}]}).execute()
                    print(f"Davet gönderildi: {email}")
                except Exception as e:
                    print(f"Davet gönderilemedi: {email}. Hata: {e}")

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


if __name__ == "__main__":
    app = QApplication([])
    main_window = ManagementMenuPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

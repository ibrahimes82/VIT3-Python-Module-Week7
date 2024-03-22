from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import pickle
import os.path

from UI_Files.management_ui import Ui_FormManagement

# Google Calendar API'deki yetkilendirme kapsamları
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/calendar.events.readonly',
          'https://www.googleapis.com/auth/calendar']


class ManagementPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.form_management = Ui_FormManagement()
        self.form_management.setupUi(self)

        self.events = None

        self.menu_user = None
        self.menu_admin = None

        self.form_management.pushButtonGetAllEvents.clicked.connect(self.get_calendar_events)
        self.form_management.pushButtonSendEmail.clicked.connect(self.send_invitations)
        self.form_management.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_management.pushButtonExit.clicked.connect(self.close)

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
        self.form_management.tableWidget.setRowCount(0)  # Önceki verileri temizle
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_start = self.format_datetime(start)  # Tarih/saat formatlamasını yap
            attendees = event.get('attendees', [])

            participant_emails = ", ".join([attendee['email'] for attendee in attendees if attendee.get('email')])
            organizer_email = event['organizer'].get('email') if event.get('organizer') else 'Unknown'

            self.form_management.tableWidget.insertRow(self.form_management.tableWidget.rowCount())
            self.form_management.tableWidget.setItem(self.form_management.tableWidget.rowCount() - 1, 0,
                                                     QTableWidgetItem(event.get('summary', 'No Name')))
            self.form_management.tableWidget.setItem(self.form_management.tableWidget.rowCount() - 1, 1,
                                                     QTableWidgetItem(formatted_start))
            self.form_management.tableWidget.setItem(self.form_management.tableWidget.rowCount() - 1, 2,
                                                     QTableWidgetItem(participant_emails))
            self.form_management.tableWidget.setItem(self.form_management.tableWidget.rowCount() - 1, 3,
                                                     QTableWidgetItem(organizer_email))

    def format_datetime(self, datetime_str):
        # Tarih ve saat değerini ISO formatından dönüştür
        datetime_obj = datetime.datetime.fromisoformat(datetime_str)
        # "gün-ay-yıl saat:dakika" formatında dönüştür
        formatted_datetime = datetime_obj.strftime("%d-%m-%Y %H:%M")
        return formatted_datetime

    def get_credentials(self):
        creds = None
        # Token dosyasını kontrol et
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Yetkilendirme yoksa veya geçersizse yeniden yetkilendirme yap
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Yeni yetkilendirme bilgilerini kaydet
            with open('credentials/token.pickle', 'wb') as token:
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
            self.form_management.menu_admin = AdminMenuPage(self.current_user)
            self.form_management.menu_admin.show()
        else:
            from user_menu import UserMenuPage
            self.hide()
            self.form_management.menu_user = UserMenuPage(self.current_user)
            self.form_management.menu_user.show()


if __name__ == "__main__":
    app = QApplication([])
    main_window = ManagementPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()

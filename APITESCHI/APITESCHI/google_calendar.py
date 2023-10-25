# settings/google_calendar.py

from google.oauth2 import service_account
from django.conf import settings
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = service_account.Credentials.from_service_account_file(os.path.join(settings.BASE_DIR, './APITESCHI/credentials.json'), scopes=SCOPES)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json

def gdrvclean(status):
    if "error" in status:
        scope = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('token.json', scope)
        service = build('drive', 'v3', credentials=creds)
        page_token = None
        results = service.files().list(q="name contains 'YoteShin'",
                                        spaces='drive',
                                        fields='nextPageToken, '
                                               'files(id, name)',
                                        pageToken=page_token).execute()
        ytsn_info = results.get('files', [])
        for a in ytsn_info:
            ytsn_id = u'{0}'.format(a['id'])
        service.files().delete(fileId=ytsn_id).execute()
            

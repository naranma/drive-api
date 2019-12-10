import os
import pprint
import uuid
import pickle

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

pp = pprint.PrettyPrinter(indent=2)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This access scope grants read-only access to the authenticated user's Drive
# account.

#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


#STORAGE = Storage('storage.json')
#credentials = STORAGE.get()
CREDENTIALS_PICKLE = 'token.pickle'

def get_authenticated_service2():
  
  credentials = None

  if os.path.exists(CREDENTIALS_PICKLE):
    with open(CREDENTIALS_PICKLE, 'rb') as token:
      credentials = pickle.load(token)

  # If there are no (valid) credentials available, let the user log in.
  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
      #credentials = flow.run_local_server(port=0)
      credentials = flow.run_console()

    # Save the credentials for the next run
    with open(CREDENTIALS_PICKLE, 'wb') as token:
      pickle.dump(credentials, token)

  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_drive_files(service, **kwargs):
  results = service.files().list(
    **kwargs
  ).execute()

  pp.pprint(results)

def list_drive_files2(service, **kwargs):
  request = service.files().list(
    **kwargs
  )

  while request is not None:
    response = request.execute()
    
    pp.pprint(response)

    request = service.drives().list_next(previous_request=request,previous_response=response)

def create_teamdrive(service, td_name):
  request_id = str(uuid.uuid4()) # random unique UUID string
  body = {'name': td_name}
  return service.teamdrives().create(body=body,
          requestId=request_id, fields='id').execute().get('id')

def list_teamdrive(service):
  results = service.drives().list(pageSize=100).execute()  # pageSize=None return 10 items. Max = 100
  return results.get('drives')

def list_teamdrive2(service):
  results = []
  request = service.drives().list(pageSize=100) # pageSize=None return 10 items. Max = 100

  while request is not None:
    response = request.execute()

    results = results + response.get('drives')
    #pp.pprint(response)

    request = service.drives().list_next(previous_request=request,previous_response=response)
    
  return results

def update_teamdrive(service, td_id, td_name):
  body = {'name': td_name}
  return service.teamdrives().update(body=body,
          teamDriveId=td_id, fields='id').execute().get('id')

def get_teamdrive(service, td_id):
  return service.teamdrives().get(
          teamDriveId=td_id, fields='*').execute()

def add_user(service, td_id, user, role='organizer'):
  body = {'type': 'user', 'role': role, 'emailAddress': user}
  return service.permissions().create(body=body, fileId=td_id, sendNotificationEmail=False,
          supportsTeamDrives=True, fields='id').execute().get('id')

def add_group(service, td_id, group, role='organizer'):
  body = {'type': 'group', 'role': role, 'emailAddress': group}
  return service.permissions().create(body=body, fileId=td_id, sendNotificationEmail=False,
          supportsTeamDrives=True, fields='id').execute().get('id')
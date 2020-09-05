import os
import base64
import pickle

from file_utils import *

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.modify'
]

MESSAGE_VIEW = {True: 'messages', False: 'threads'}

TOKEN = 'token.pickle'

USER_ID = 'me'

LABELS = 'INBOX'

DIRECTORY_TO_STORE = read_json()[0]


def get_creds(creds=None):

    if os.path.exists(TOKEN):

        with open(TOKEN, 'rb') as token:
            return pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:

            if os.path.exists('credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                print(
                    """Please get Credetials from Gmail and store them as 'credentials.json' from : https://developers.google.com/gmail/api/quickstart/js""")
                exit(0)

        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_service():

    return build('gmail', 'v1', credentials=get_creds()).users()


def get_messages_or_threads(view='', mail_id="", attach_id="") -> str:
    mail_string = "get_service().{0}()".format(view)
    exe_string = ".execute()"

    if mail_id:

        if attach_id:

            attach_string = ".attachments().get(userId='{0}', messageId='{1}', id='{2}')".format(
                USER_ID, mail_id, attach_id)

            return mail_string + attach_string + exe_string

        item_String = ".get(userId='{0}', id='{1}')".format(
            USER_ID, mail_id)

        return mail_string + item_String + exe_string

    list_string = ".list(userId='{1}', labelIds='{3}'){2}.get('{0}', [])".format(
        view, USER_ID, exe_string, LABELS)

    return mail_string + list_string


def get_attachments(as_message=True):
    attachment_id = 'attachmentId'

    for each_mail in eval(get_messages_or_threads(view=MESSAGE_VIEW[as_message])):

        mail_id = each_mail['id']

        each_mail = eval(get_messages_or_threads(
            view=MESSAGE_VIEW[as_message], mail_id=mail_id))

        if 'parts' in each_mail['payload']:

            for part in each_mail['payload']['parts']:

                if attachment_id in part['body']:

                    attachment = eval(get_messages_or_threads(
                        view=MESSAGE_VIEW[as_message], mail_id=mail_id, attach_id=part['body'][attachment_id]))

                    data = attachment['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

                    if part['filename'] and part['filename'].endswith('.pdf'):

                        file_path = os.path.join(
                            DIRECTORY_TO_STORE, part['filename'])

                        if not os.path.exists(file_path):

                            with open(file_path, 'wb') as fp:
                                fp.write(file_data)

                        else:

                            print("All new attachments downloaded!")
                            return True

    return True


def main():

    return get_attachments()


if __name__ == "__main__":

    main()

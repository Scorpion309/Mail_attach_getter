import os

from dotenv import load_dotenv

EMAIL_INBOX_FOLDER = 'INBOX'
MESSAGE_SUBJECT = 'Отчет'
MESSAGE_SENDER = 'Tustin@tut.by'
ATTACHMENT_FORMAT = '.xlsx'


def read_credentials():
    load_dotenv()

    user_email = os.getenv("USER_EMAIL")
    user_password = os.getenv("USER_PASSWORD")
    imap_server = os.getenv("IMAP")

    if user_email and user_password and imap_server:
        return user_email, user_password, imap_server
    else:
        raise ValueError('Please add a .env file and write the credentials!')

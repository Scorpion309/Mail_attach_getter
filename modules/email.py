import logging
from email import message_from_bytes
from imaplib import IMAP4_SSL

from settings import MESSAGE_SUBJECT, MESSAGE_SENDER, EMAIL_INBOX_FOLDER


def filtering_emails(connection):
    subject = MESSAGE_SUBJECT.encode('utf-8')
    connection.list()
    connection.select(EMAIL_INBOX_FOLDER)
    connection.literal = subject
    return connection.search("utf-8", f'(FROM {MESSAGE_SENDER})', "SUBJECT")


def get_message(messages, connection):
    messages_ids = messages[0].split()[::-1]
    for index, message_id in enumerate(messages_ids):
        typ, data = connection.fetch(message_id, '(RFC822)')
        message = message_from_bytes(data[0][1])
        connection.store(message_id, '+FLAGS', '\\Seen')
        yield message


def get_last_message(code, messages, mail_connection):
    logging.info('Получаю последнее сообщение...')
    if code == 'OK' and messages[0]:
        return next(get_message(messages, mail_connection))
    logging.warning('Сообщения соответствующие фильтру не найдены!')


def get_last_filtered_message(email_address, password, imap_server):
    logging.info('Подключаюсь к серверу...')
    with IMAP4_SSL(imap_server) as mail_connection:
        mail_connection.login(email_address, password)
        code, messages = filtering_emails(mail_connection)
        return get_last_message(code, messages, mail_connection)


def get_mail_attachments(message, condition_check):
    logging.info('Получаю вложенные файлы...')
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if not part.get('Content-Disposition'):
            continue
        file_name = part.get_filename()
        if condition_check(file_name):
            yield part.get_filename(), part.get_payload(decode=1)


def get_attachments(message, attachment_format):
    return [(filename, byte_file) for filename, byte_file in
            get_mail_attachments(message, lambda x: x.endswith(attachment_format))]

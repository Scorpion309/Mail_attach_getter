import logging

from modules.email import get_attachments, get_last_filtered_message
from modules.excel import load_workbook_and_save_to_file
from settings import read_credentials, ATTACHMENT_FORMAT

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    email, password, imap_server = read_credentials()
    message = get_last_filtered_message(email, password, imap_server)
    if message:
        attachments = get_attachments(message, ATTACHMENT_FORMAT)
        if attachments:
            for file_name, byte_file in attachments:
                load_workbook_and_save_to_file(file_name, byte_file)
        else:
            logging.warning('Вложенных файлов указанного формата не найдено!')
    else:
        logging.warning('Не обработано ни одного сообщения!')

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

class Message:
    def __init__(self, from_name: str, to_name: str, subject: str):
        self.msg = MIMEMultipart()
        self.msg['Subject'] = Header(subject, 'utf-8')
        self.msg['From'] = Header(from_name)
        self.msg['To'] = Header(to_name)

    def add_text(self, text: str):
        self.msg.attach(MIMEText(text + '\n', 'plain', 'utf-8'))

    def add_image(self, path: str, name: str = None):
        with open(path, 'rb') as f:
            img = MIMEImage(f.read(), name=name if name is not None else os.path.basename(path))
        self.msg.attach(img)

    def add_attachment(self, path: str, name: str = None):
        with open(path, 'rb') as f:
            attachment = MIMEApplication(f.read(), name=name if name is not None else os.path.basename(path))
        attachment['Content-Disposition'] = f'attachment; filename={name if name is not None else os.path.basename(path)}'
        self.msg.attach(attachment)


    def get_message(self):
        return self.msg.as_string()

import time
from smtplib import SMTP_SSL
from typing import Union
from mail_mojo.message import Message
import webbrowser
from imaplib import IMAP4_SSL
import email
import re
import base64
from .recieved_email import Email


class Mail:
    def __init__(self, address: str, pwd: str, server: str, port: Union[int, None], tls: bool = False):
        """
        DO NOT INSTANTIATE THIS CLASS UNLESS YOU KNOW YOUR SERVER ADDRESS AND PORT
        :param address: email address
        :param pwd: password or access token
        :param server: server address
        :param port: server port
        :param tls: use tls?
        """
        self.address = address
        self.password = pwd
        self.server = server
        self.port = port
        self.new_mail_queue = []
        self._mail_list = []
        self.smtp = SMTP_SSL(server, port)
        self.messages = None
        if tls:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()
        self.smtp.login(address, pwd)

    def init_imap(self, server: str, port: int = None):
        if port is None:
            self.imap = IMAP4_SSL(server)
        else:
            self.imap = IMAP4_SSL(server, port)
        self.imap.login(self.address, self.password)
        self.select()

    def select(self):
        result , _ = self.imap.select()
        if result.lower() == 'no':
            if self.server == 'imap.163.com':
                webbrowser.open(f'http://config.mail.163.com/settings/imap/login.jsp?uid={self.address}')
                print('请先在浏览器中登录来允许imap收信，然后重启程序')
                exit()
            else:
                raise ConnectionError(f'Fail selecting inbox: {_}')

    def list_mails(self):
        return self.imap.search(None, 'ALL')[1][0].split()

    def _diff(self, old_list: list, new_list: list):
        result = [*new_list]
        for i in old_list:
            try:
                result.remove(i)
            except:
                pass
        return result

    def init_wait(self):
        """
        call this method before using wait_for_new_mail
        :return: None
        """
        self._mail_list = [*self.list_mails()]
        return

    def wait_for_new_mail(self, recv_interval: int = 3) -> Union[None, Email]:
        """
        stuck until new mail arrived
        :param recv_interval: check frequency in second
        :return: mail
        """
        while True:
            if len(self.new_mail_queue) != 0:
                message = self.new_mail_queue[0]
                self.new_mail_queue.remove(message)
                return self.imap_get_mail(message)
            else:
                new_mail_list = self.list_mails()
                new = self._diff(self._mail_list, new_mail_list)
                self._mail_list = new_mail_list
                self.new_mail_queue.extend(new)
            time.sleep(recv_interval)

    def _process_header(self, header: str, charset: str):
        pattern = re.compile(r'^\"?=\?' + charset +'\?[Bb]\?([A-Za-z+=0-9/]*)(?=\?=)')
        match = pattern.match(header)
        if match is not None:
            return base64.b64decode(match.group(1)).decode(charset)
        else:
            return header

    def imap_get_mail(self, mail_num: bytes):
        if self.imap is None:
            raise NotImplementedError('IMAP is not initiated')

        mail_num = mail_num.decode()
        result, email_message = self.imap.fetch(f'{mail_num}:{mail_num}', '(RFC822)')

        email_message = email.message_from_bytes(email_message[0][1])

        payload: email.message.Message = email_message.get_payload()[0]

        pattern = re.compile(r'^Content-Type: text/plain;\s*charset=\"?([A-z0-9-]*)\"?', re.RegexFlag.MULTILINE)
        charset_match = pattern.match(payload.as_string())
        if charset_match is None:
            print('Warning: failed to get charset, skipping this mail')
            return
        charset = charset_match.group(1)

        from_address = self._process_header(email_message['From'], charset)
        to_address = self._process_header(email_message['To'], charset)
        subject = self._process_header(email_message['Subject'], charset)

        str_payload = payload.as_string()
        encoding = payload['Content-Transfer-Encoding'] if payload['Content-Transfer-Encoding'] is not None else 'ascii'
        pattern = re.compile(r'Content-Type:\stext/plain;[\s]*charset=\"?[A-Za-z-: 0-9;\n]*\"?\s?(Content-Transfer-Encoding: base64\s*)?\s*(^[A-Za-z+=0-9]*)', flags=re.RegexFlag.MULTILINE)
        str_payload = pattern.match(str_payload)
        try:
            str_payload = str_payload.group(2)
        except Exception:
            str_payload = ''
        if encoding == 'base64':
            str_payload = base64.b64decode(str_payload).decode(charset)
        return Email(from_address, to_address, subject, str_payload)

    def restart_smtp(self):
        self.smtp.quit()
        self.smtp = SMTP_SSL(self.server, self.port)
        self.smtp.login(self.address, self.password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp.quit()

    def send(self, to_address: Union[list, str], msg: Message):
        self.smtp.sendmail(self.address, to_address, msg.get_message())

    def close(self):
        self.smtp.quit()

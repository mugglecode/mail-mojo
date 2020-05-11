from .mail import Mail


class SinaMail(Mail):
    def __init__(self, address: str, pwd: str):
        super().__init__(address, pwd, 'smtp.sina.com', None, True)

    def init_imap(self):
        super().init_imap('imap.sina.com')

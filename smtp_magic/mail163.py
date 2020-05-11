from smtp_magic.mail import Mail


class Mail163(Mail):
    def __init__(self, address: str, pwd: str):
        super().__init__(address, pwd, 'smtp.163.com', 465)

    def init_imap(self, **kwargs):
        super().init_imap('imap.163.com')

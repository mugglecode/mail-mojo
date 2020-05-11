from smtp_magic.mail import Mail


class QQMail(Mail):
    def __init__(self, address: str, pwd: str):
        super().__init__(address, pwd, 'smtp.qq.com', 465)

    def init_imap(self, **kwargs):
        super(QQMail, self).init_imap('imap.qq.com')

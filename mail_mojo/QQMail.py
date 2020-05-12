from mail_mojo.mail import Mail


class QQMail(Mail):
    def __init__(self, address: str, access_token: str):
        """
        Init QQ Mail
        :param address: email address
        :param access_token: access token not password
        """
        super().__init__(address, access_token, 'smtp.qq.com', 465)

    def init_imap(self, **kwargs):
        super(QQMail, self).init_imap('imap.qq.com')

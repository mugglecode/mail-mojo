from mail_mojo.mail import Mail


class SinaMail(Mail):
    def __init__(self, address: str, access_token: str):
        """
        init Sina Mail box
        :param address: email address
        :param access_token: access token not password
        """
        super().__init__(address, access_token, 'smtp.sina.com', None, True)

    def init_imap(self, **kwargs):
        super().init_imap('imap.sina.com')

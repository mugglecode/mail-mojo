from mail_mojo.mail import Mail


class Mail163(Mail):
    def __init__(self, address: str, access_token: str):
        """
        Init 163 Mailbox
        :param address: email address
        :param access_token: access token not password
        """
        super().__init__(address, access_token, 'smtp.163.com', 465)

    def init_imap(self, **kwargs):
        super().init_imap('imap.163.com')

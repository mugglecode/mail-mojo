from exchangelib import Credentials, Account, Message


class OutlookMail():
    def __init__(self, address: str, pwd: str):
        self.credential = Credentials(address, pwd)
        self.account = Account(address, credentials=self.credential, autodiscover=True)

    def send(self, subject: str, content: str, to: str):
        message = Message(account=self.account,
                          subject=subject,
                          body=content,
                          to=to)
        message.send()


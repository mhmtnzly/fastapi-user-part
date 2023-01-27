from azure.communication.email import (EmailClient, EmailContent,
                                       EmailAddress, EmailMessage,
                                       EmailRecipients)
from decouple import config

CONNECTION_STRING = config("CONNECTION_STRING")


class Email:
    def __init__(self, connection_string):

        self.CONNECTION_STRING = connection_string
        self.client = EmailClient.from_connection_string(
            self.CONNECTION_STRING)
        self.sender = config("SENDER")

    def confirmationMail(self, to, body, userName):
        subject_ = f"Confirmation of {userName}"
        content = EmailContent(
            subject=subject_,
            plain_text="This is the body",
            html=f"<html><h5>Cofirmation token: {body}</h5></html>",
        )
        address = EmailAddress(
            email=to, display_name=userName)
        message = EmailMessage(
            sender=self.sender,
            content=content,
            recipients=EmailRecipients(to=[address])
        )
        response = self.client.send(message)
        return response

    def passwordforgetMail(self, to, body, userName):
        subject_ = f"Forget Password of {userName}"
        content = EmailContent(
            subject=subject_,
            plain_text="This is the body",
            html=f"<html><h5>Forget token: {body}</h5></html>",
        )
        address = EmailAddress(
            email=to, display_name=userName)
        message = EmailMessage(
            sender=self.sender,
            content=content,
            recipients=EmailRecipients(to=[address])
        )
        response = self.client.send(message)
        return response


email = Email(connection_string=CONNECTION_STRING)

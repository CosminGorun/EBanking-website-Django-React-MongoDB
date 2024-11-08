import smtplib
import ssl
from email.message import EmailMessage


class EmailSender:
    def __init__(self):
        self.email_sender='gorun.cosmin003@gmail.com'
        self.email_password='ikhw jker pbkl omvi'

    def sendMail(self,receiver,subject,body):

        em = EmailMessage()
        em['From'] = "python"
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, receiver, em.as_string())
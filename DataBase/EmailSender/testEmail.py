import smtplib
import ssl
from email.message import EmailMessage
# from lib2to3.fixes.fix_input import context

email_sender='<EMAIL>'
email_to='<EMAIL>'
email_password='<PASSWORD>'

subject='test'
body="mesaj"

em=EmailMessage()
em['From']=email_sender
em['To']=email_to
em['Subject']=subject
em.set_content(body)

context= ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_to, em.as_string())
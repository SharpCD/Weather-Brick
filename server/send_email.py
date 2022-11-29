import smtplib
from email.mime.text import MIMEText
import random

class SendEmail(object):
    def __init__(self, email):
        self.recipients = email
    def send_email(self):
        sender = "weather.brick@mail.ru"
        password =''
        server = smtplib.SMTP_SSL("smtp.mail.ru",  465)
        code = str(random.randint(1000, 9999))
        message =f'Код для регистрации: \n{code}'
        try:
            server.login(sender, password)
            msg = MIMEText(message)
            msg["Subject"] = "Код для регистрации"
            server.sendmail(sender, self.recipients, msg.as_string())
            return code
        except Exception as ex:
            return f"{ex}\nПочта не найдена"



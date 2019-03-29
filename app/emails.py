import os
from threading import Thread
from flask_mail import Message

from app import app, mail


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def mail_send(subject, recipients, text_body):
    msg = Message(subject, 
                  sender=os.getenv('MAIL_DEFAULT_SENDER'), 
                  recipients=recipients)
    msg.body = text_body
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()

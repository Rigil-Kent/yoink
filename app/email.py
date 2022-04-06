import threading

from flask import current_app, render_template
from flask_mail import Message

from app import mail, config


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(
        
        current_app.config['MAIL_PREFIX'] + subject,
        sender=current_app.config['MAIL_SENDER'], recipients=to)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    mail_thread = threading.Thread(target=send_async_email, args=[current_app._get_current_object(), msg])
    mail_thread.start()
    return mail_thread

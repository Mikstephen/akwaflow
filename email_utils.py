from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email(subject, recipient, body, html_body=None):
    msg = Message(
        subject=subject,
        recipients=[recipient],
        body=body,
        html=html_body,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
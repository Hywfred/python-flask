from threading import Thread
from flask.app import Flask
from flask.templating import render_template
from app.models import User
from email.mime import text
from flask_mail import Message
from app import mail, app


def send_async_email(app: Flask, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email(
        "[Blog] Reset your password",
        sender=app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )

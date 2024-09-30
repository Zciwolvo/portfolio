from flask import Blueprint, render_template, request, redirect, current_app
from flask_mail import Message
import os

from . import portfolio

@portfolio.route("/")
def home():
    return render_template("index.html")

@portfolio.route("/send-email", methods=["POST"])
def send_email():
    mail = current_app.extensions['mail']
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    msg = Message(
        "New Contact Form Submission", sender=email, recipients=[os.getenv("MAIL")]
    )
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)

    print("Email sent!")
    return redirect("/#contact")
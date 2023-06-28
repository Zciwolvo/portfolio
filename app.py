from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL")
app.config["MAIL_PASSWORD"] = os.getenv("PASS")
mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send-email", methods=["POST"])
def send_email():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    msg = Message(
        "New Contact Form Submission", sender=email, recipients=[os.getenv("MAIL")]
    )
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)

    print("Email sent!")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

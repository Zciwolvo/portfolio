from flask import request, jsonify, send_from_directory, json, Blueprint, current_app
from flask_cors import CORS
from email.message import EmailMessage
import smtplib
import stripe
from . import dipoe



CORS(dipoe, origins='https://www.dipoe.pl', supports_credentials=True)

@dipoe.before_request
def setup_stripe_api_key():
    stripe.api_key = current_app.config['DIPOE_SECRET']

@dipoe.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = json.loads(request.data)
        price = int(data['price'])
        payment_intent = stripe.PaymentIntent.create(
            amount=price,
            currency='pln',
            payment_method_types=['card', 'blik']
        )
        return jsonify(clientSecret=payment_intent.client_secret), 200
    except Exception as e:
        return jsonify(error=str(e)), 403

@dipoe.route('/send_mail_to_receiver', methods=['POST'])
def send_mail_to_receiver():
    receiver = request.json['receiver']

    msg = EmailMessage()
    msg['From'] = current_app.config['DIPOE_USER']
    msg['To'] = receiver
    msg['Subject'] = 'Zakup płyty DIPOE'

    msg.set_content('''
            Dziękujemy!
            Twój zakup został przez nas odebrany.
            Proszę oczekiwać dalszego kontaktu na numer telefonu lub adres email podane w formularzu.
            Ekipa DIPOE
    ''', subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(current_app.config['DIPOE_USER'], current_app.config['DIPOE_PASSWORD'])
            smtp.send_message(msg)

        return jsonify('Mail sent to receiver!'), 200
    except Exception as e:
        return jsonify(error=str(e)), 403

@dipoe.route('/send_mail_to_sender', methods=['POST'])
def send_mail_to_sender():
    topic = request.json['topic']
    receiver = request.json['receiver']
    name = request.json['Name']
    surname = request.json['Surname']
    city = request.json['City']
    phone = request.json['Phone']
    postal = request.json['Postal']
    address1 = request.json['Address1']
    address2 = request.json['Address2']

    msg = EmailMessage()
    msg['From'] = current_app.config['DIPOE_USER']
    msg['To'] = 'dipoeone@gmail.com'
    msg['Subject'] = topic

    msg.set_content(f'''\
        Dane klienta:
        Imie nazwisko: {name} {surname}
        Numer telefonu: {phone}
        Adres email: {receiver}
        Dane do wysyłki
        {city}, {postal}, {address1}/{address2}
    ''')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(current_app.config['DIPOE_USER'], current_app.config['DIPOE_PASSWORD'])
        smtp.send_message(msg)

    return jsonify('Mail sent to receiver!'), 200


@dipoe.route('/substract_cd', methods=['POST'])
def substract_cd():
    return {'cd_number': 1}


@dipoe.route('/', defaults={'path': ''})
@dipoe.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./build', 'index.html')



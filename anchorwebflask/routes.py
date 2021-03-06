import os
import smtplib
from email.message import EmailMessage

from flask import render_template, redirect, request, flash

from anchorwebflask import application

EMAIL_USER = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SECRET_KEY = os.environ.get('SESSION_KEY')

application.secret_key = SECRET_KEY


@application.route('/', methods=['GET'])
@application.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@application.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="About")


@application.route('/skilled-nursing-services', methods=['GET'])
def nursing():
    return render_template('skillednursingservices.html', title="Skills")


@application.route('/companion-services', methods=['GET'])
def companion():
    return render_template('companionservices.html', title="Skills")


@application.route('/homemaker-services', methods=['GET'])
def homemaker():
    return render_template('homemakerservices.html', title="Skills")


@application.route('/supported-living-services', methods=['GET'])
def supported():
    return render_template('supportedliving.html', title="Skills")


@application.route('/respite-services', methods=['GET'])
def respite():
    return render_template('respiteservices.html', title="Skills")


@application.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html', title="Resources")


@application.route('/locations', methods=['GET'])
def locations():
    return render_template('locations.html', title="Locations")


@application.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        pass

    return render_template('apply.html', title="Apply")


@application.route('/contact-form', methods=['POST', 'GET'])
def contactform():
    form = request.form
    missing = list()

    if request.method == "POST":

        for k, v in form.items():
            if v == "":
                missing.append(k)

        if missing:
            flash("This form is incomplete.", "warning")
            return redirect("/contact-form")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            msg = EmailMessage()
            msg['Subject'] = form.get('about')
            msg['From'] = form.get('email')
            msg['To'] = [
                "osagie@myanchorhouse.com",
                "tola@myanchorhouse.com"
            ]
            msg.set_content(form.get('message'))
            smtp.send_message(msg)
            flash("Message Sent!", "success")
            return render_template("contact.html", title="Contact us")

    return render_template('contact.html', title="Contact Us")

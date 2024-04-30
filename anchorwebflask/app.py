import os
import smtplib
from email.message import EmailMessage

from flask import Flask, flash, redirect, render_template, request
from flask_cachebuster import CacheBuster

EMAIL_USER = os.environ.get("EMAIL_ADDRESS", default="")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", default="")
SECRET_KEY = os.environ.get("SESSION_KEY", default="")

app = Flask(__name__)
app.secret_key = SECRET_KEY

config = {"extensions": [".js", ".css", ".png", ".jpg"], "hash_size": 10}

cache_buster = CacheBuster(config=config)

cache_buster.init_app(app)


@app.get("/")
@app.get("/home")
def home():
    return render_template("home.html")


@app.get("/about")
def about():
    return render_template("about.html", title="About")


@app.get("/basic-support-services")
def basic_support_services():
    return render_template("basic_support_services.html", title="Support Services")


@app.get("/in-home-support-services")
def in_home_support_services():
    return render_template(
        "in_home_support_services.html", title="In-Home Support Services"
    )


@app.get("/employment-services")
def employment_services():
    return render_template("employment_services.html", title="Employment Services")


@app.get("/skilled-nursing-services")
def nursing():
    return render_template("skillednursingservices.html", title="Skills")


@app.get("/companion-services")
def companion():
    return render_template("companionservices.html", title="Skills")


@app.get("/homemaker-services")
def homemaker():
    return render_template("homemakerservices.html", title="Skills")


@app.get("/supported-living-services")
def supported():
    return render_template("supportedliving.html", title="Skills")


@app.get("/respite-services")
def respite():
    return render_template("respiteservices.html", title="Skills")


@app.get("/resources")
def resources():
    return render_template("resources.html", title="Resources")


@app.get("/locations")
def locations():
    return render_template("locations.html", title="Locations")


@app.get("/apply")
@app.post("/apply")
def apply():
    if request.method == "POST":
        pass

    return render_template("apply.html", title="Apply")


@app.get("/contact-form")
@app.post("/contact-form")
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

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            msg = EmailMessage()
            msg["Subject"] = form.get("about")
            msg["From"] = form.get("email")
            msg["To"] = ["osagie@myanchorhouse.com", "tola@myanchorhouse.com"]
            msg.set_content(form.get("message"))
            smtp.send_message(msg)
            flash("Message Sent!", "success")
            return render_template("contact.html", title="Contact us")

    return render_template("contact.html", title="Contact Us")

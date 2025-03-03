from flask import Flask,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os

import smtplib
""" email data """

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASS")


""" Flask Setup """


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

""" Contact form """
class ContactForm(FlaskForm):
    name = StringField(label="Full name",validators=[DataRequired()])
    email = StringField(label="Email",validators=[DataRequired(),Email()])
    message = TextAreaField(label="Enter your message",validators=[DataRequired()],render_kw={"style":"height:10ch"})
    submit = SubmitField(label="Submit")

""" Pages """

@app.route("/")
def home():
    return render_template("index.html")




@app.route("/contact",methods=["GET","POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        mail_sending(form.name.data,form.email.data,form.message.data)

        return render_template("contact.html", msg_sent = True)

    return render_template("contact.html",form = form , msg_sent=False)



@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")


""" email connection """

def mail_sending(name,email,message):
    email_msg = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(EMAIL,PASSWORD)
        connection.sendmail(EMAIL,EMAIL,email_msg)



""" running the app """
app.run(debug=True,port=2024)


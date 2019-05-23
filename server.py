#!/usr/bin/env python2.7


import os
import re
from flask import Flask, request, render_template, g, redirect, Response, url_for, Blueprint, flash

from Form import query_Form
import time
import serverfunction as sf
import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime
from validate_email import validate_email
from emailahoy import VerifyEmail

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config['SECRET_KEY'] = 'secretkey'

model=sf.rf()
model2 = sf.lg()

__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

def connect_type(word_list):
    """This function takes a list of words, then, depending which key word, returns the corresponding internet connection type as a string. ie) 'ethernet'."""

    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type


# CHANGE TO YOUR ACCOUNT INFORMATION
# Account Information
gmail_user = 'username@someemail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'some_password' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server


@app.route('/')
def index():
    print request.args

    return render_template("index.html")


@app.route('/query', methods=['GET', 'POST'])
def query():
    flag_exist = False
    form = query_Form()
    test=sf.getdata()
    result=model.predict(test)[0]
    result2 = model2.predict(test)

     
    if form.validate_on_submit():
         to = form.email.data 
         flag_exist = True
         test=sf.getdata()
         result=model.predict(test)[0]
         result2 = model2.predict(test)+0.5
         final = int(result2)

         if result == True:
              out = 'It is too crowded'
         else:
              out = 'Still available'
         
         e = VerifyEmail()
         status = e.verify_email_smtp(
                    email=to,
                    from_host='mydomain.com',
                    from_email='verify@mydomain.com'
                     )

         if e.was_found(status):
              temp = 'Mudd1214: %s' % (final)
              msg = MIMEText(temp+ "\n\n"+out)
              msg['Subject'] = 'Room Capacity'
              msg['From'] = gmail_user
              msg['To'] = to
              smtpserver.sendmail(gmail_user, [to], msg.as_string())
              return render_template("query.html",form = form,flag_exist=flag_exist,final=final,out = out)
         else:
              return render_template("query.html",form = form,flag_exist=flag_exist,final=final,out = out)
    return render_template("query.html",form=form,flag_exist=flag_exist)




if __name__ == "__main__":
    import click
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8010, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()

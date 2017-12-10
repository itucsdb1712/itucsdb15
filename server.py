import datetime
import os
import json
import re

from database import *
from forms import *
from flask import Flask, flash, redirect, url_for, session, Blueprint
from flask import render_template
from company_view import *

app = Flask(__name__)
app.register_blueprint(company_app)
app.config['SECRET_KEY'] = "verysecretkeyofthewebsite"

def get_elephantsql_dsn(vcap_services):
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} 
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn
@app.route('/', methods=['GET', 'POST'])
def home_page():
    global logged_user_global
    logged_user_global = None
    session['logged_in'] = False
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hash = getUserPwHash(username)
        if hash[0][0] == password:
            session['logged_in'] = True
            flash('You have logged in successfully.')
            logged_user_global = username
        else:
            flash('You have entered wrong username or password.')
            logged_user_global = None
    return render_template('home.html', form = form, username = logged_user_global)
@app.route('/adminpage')
def admin_page():
    if not session.get('logged_in'):
        flash("You have no authority!")
        return redirect(url_for('home_page'))
    else:
        return render_template('adminpage.html')
        


@app.route('/logout')
def logout():
    session['logged_in'] = False
    logged_user_global = None
    flash('You have been logged out successfully.')
    return redirect(url_for('home_page'))
    

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), True
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        dsn = app.config['dsn'] = """user='postgres' password='itucsdb1712'
                                        host='localhost' port=5432 dbname='itucsdb'"""
    initdb(app.config['dsn'])
    app.run(host='0.0.0.0', port=port, debug=debug)


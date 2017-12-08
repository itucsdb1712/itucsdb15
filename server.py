import datetime
import os
import json
import re

from database import *
from forms import AddCompanyForm, SelectCompanyForm
from flask import Flask, flash, redirect, url_for
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecretkeyofthewebsite"

def get_elephantsql_dsn(vcap_services):
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} 
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn
@app.route
@app.route('/')
def home_page():
    return render_template('home.html')
@app.route('/adminpage')
def admin_page():
	 return render_template('adminpage.html')
@app.route('/addcompany', methods=['GET', 'POST'])
def add_company():
    form = AddCompanyForm()
    if form.validate_on_submit(): 
        company_name = form.company_name.data
        number_of_employees = form.number_of_employees.data
        addCompanyToDb(company_name, number_of_employees)
        flash('Company added successfully.')
        return render_template('adminpage.html', form=form)
    return render_template('addcompany.html', form=form)
@app.route('/listcompanies', methods=['GET'])
def list_companies():
    information = listCompanies()
    return render_template('listCompanies.html', informations = information)
@app.route('/selectcompany', methods=['GET', 'POST'])
def select_company():
    form = SelectCompanyForm()
    if form.validate_on_submit():
        global company_name_global
        company_name_global = form.company_name.data
        if form.submitUpdate.data is True:
            return redirect(url_for('update_company'))
        if form.submitDelete.data is True:
            return redirect(url_for('delete_company'))
        return render_template('selectcompany.html', form = form)
    return render_template('selectcompany.html', form = form)
@app.route('/updatecompany', methods=['GET', 'POST'])
def update_company():
    information = returnCompany(company_name_global)
    form = AddCompanyForm(company_name=information[0][1], number_of_employees=information[0][2])
    company_id = information[0][0]
    if form.submit.data is True:
        if form.validate_on_submit():
            name = form.company_name.data
            number_of_employees = form.number_of_employees.data
            print(name)
            print(number_of_employees)
            updateCompany(company_id, name, number_of_employees)
            flash('Company updated successfully.')
            return render_template('adminpage.html')
    return render_template('updatecompany.html', form = form)

@app.route('/deletecompany', methods=['GET', 'POST'])
def delete_company():
    information = returnCompany(company_name_global)
    company_id = information[0][0]
    deleteCompany(company_id)
    flash('Company deleted successfully.')
    return render_template('adminpage.html')

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


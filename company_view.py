from flask import Flask, flash, redirect, url_for, session, Blueprint,render_template
from forms import *
from database import *
from flask import flash

company_app = Blueprint('company_app', __name__)

@company_app.route('/addcompany', methods=['GET', 'POST'])
def add_company():
    form = AddCompanyForm()
    if form.validate_on_submit(): 
        company_name = form.company_name.data
        number_of_employees = form.number_of_employees.data
        addCompanyToDb(company_name, number_of_employees)
        flash('Company added successfully.')
        return render_template('adminpage.html', form=form)
    return render_template('addcompany.html', form=form)
@company_app.route('/listcompanies', methods=['GET'])
def list_companies():
    information = listCompanies()
    return render_template('listcompanies.html', informations = information)
@company_app.route('/selectcompany', methods=['GET', 'POST'])
def select_company():
    form = SelectCompanyForm()
    if form.validate_on_submit():
        global company_name_global
        company_name_global = form.company_name.data
        if form.submitUpdate.data is True:
            return redirect(url_for('company_app.update_company'))
        if form.submitDelete.data is True:
            return redirect(url_for('company_app.delete_company'))
        return render_template('selectcompany.html', form = form)
    return render_template('selectcompany.html', form = form)
@company_app.route('/updatecompany', methods=['GET', 'POST'])
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

@company_app.route('/deletecompany', methods=['GET', 'POST'])
def delete_company():
    information = returnCompany(company_name_global)
    company_id = information[0][0]
    deleteCompany(company_id)
    flash('Company deleted successfully.')
    return render_template('adminpage.html')
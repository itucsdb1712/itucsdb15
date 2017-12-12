from flask import Flask, flash, redirect, url_for, session, Blueprint,render_template,request
from forms import *
from database import *
from flask import flash

employee_app = Blueprint('employee_app', __name__)

@employee_app.route('/addemployee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    information = returnAllProjects(session.get('company_number', None))
    form.project.choices = information
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        password = form.password.data
        project = form.project.data
        addEmployeeToDb(name, surname, session.get('company_number', None))
        employee_id = returnEmployeeId(name)
        createProjectEmployeeRelation(employee_id, project)
        user_type = 3
        addUserToDb(name, password, user_type)
        flash('Employee has been added successfully.')
        return render_template('homepage_company.html', username = session.get('username', None))
    return render_template('addemployee.html', form = form, username = session.get('username', None))

@employee_app.route('/listemployee', methods=['GET', 'POST'])
def list_employee():
    form = EmployeeForm(request.form)
    information = returnAllProjects(session.get('company_number', None))
    form.project.choices = information
    tasks = getEmployeeFromDb(session.get('company_number', None))
    return render_template('listemployee.html', tasks = tasks, form = form, username = session.get('username', None))

@employee_app.route('/deleteemployee/<employee_id>', methods=['GET', 'POST'])
def delete_empoloyee(employee_id):
    deleteEmployeeFromDb(employee_id)
    return redirect(url_for('employee_app.list_employee'))

@employee_app.route('/updateemployee/<employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    form = EmployeeForm(request.form)
    information = returnAllProjects(session.get('company_number', None))
    form.project.choices = information
    name = form.name.data
    surname = form.surname.data
    project = form.project.data
    form.name.data = ''
    form.surname.data = ''
    form.project.data = ''
    updateEmployeeInDb(name, surname ,employee_id)
    createProjectEmployeeRelation(employee_id, project)
    return redirect(url_for('employee_app.list_employee'))

@employee_app.route('/listemployeetask', methods=['GET', 'POST'])
def list_employee_task():
    information = returnAllTasks(session.get('username', None))
    form = EmployeeForm()
    return render_template('listemployeetask.html', tasks = information, form = form,
                           username = session.get('username', None))













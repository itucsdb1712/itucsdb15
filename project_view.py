from flask import Flask, flash, redirect, url_for, session, Blueprint,render_template, request
from forms import *
from database import *
from flask import flash

project_app = Blueprint('project_app', __name__)

@project_app.route('/addproject', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        name = form.name.data
        addProjectToDb(name, session.get('company_number', None))
        flash('Project is created successfully.')
        return render_template('homepage_company.html')
    return render_template('addproject.html', form = form, username = session.get('username', None))

@project_app.route('/listproject', methods=['GET', 'POST'])
def list_project():
    form = ProjectForm(request.form)
    tasks = getProjectsFromDb(session.get('company_number', None))
    print(tasks)
    return render_template('listprojects.html', tasks = tasks, form = form, username = session.get('username', None))

@project_app.route('/deleteproject/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    deleteProjectFromDb(project_id)
    return redirect(url_for('project_app.list_project'))

@project_app.route('/updateproject/<project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    form = TaskForm(request.form)
    name = form.name.data
    form.name.data = ''
    updateProjectInDb(name, project_id)
    return redirect(url_for('project_app.list_project'))


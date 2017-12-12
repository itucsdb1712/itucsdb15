from flask import Flask, flash, redirect, url_for, session, Blueprint,render_template,request
from forms import *
from database import *
from flask import flash

task_app = Blueprint('task_app', __name__)

@task_app.route('/addTask', methods=['GET', 'POST'])
def add_task():
    form = TaskForm(request.form)
    information = returnAllProjects(session.get('company_number', None))
    form.projects.choices = information
    if form.validate_on_submit():
        name = form.name.data
        priority = form.priority.data
        project = form.projects.data
        form.name.data = ''
        form.priority.data = ''
        form.projects.data = ''
        addTaskToDb(name, priority, project)
        flash('Task has been created')
    return render_template('add_task.html', form=form, username = session.get('username', None))

@task_app.route('/listTask', methods=['GET', 'POST'])
def list_task():
    form = TaskForm(request.form)
    information = returnAllProjects(session.get('company_number', None))
    form.projects.choices = information
    tasks = getTasksFromDb(session.get('company_number', None)) #returns a table
    return render_template('list_task.html', tasks = tasks, form = form, username = session.get('username', None))

@task_app.route('/deleteTask/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    deleteTaskFromDb(task_id)
    return redirect(url_for('task_app.list_task'))

@task_app.route('/updateTask/<task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    form = TaskForm(request.form)
    name = form.name.data
    priority = form.priority.data
    project = form.projects.data
    form.name.data = ''
    form.priority.data = ''
    form.projects.data = ''
    updateTaskInDb(task_id, name, priority, project)
    return redirect(url_for('task_app.list_task'))
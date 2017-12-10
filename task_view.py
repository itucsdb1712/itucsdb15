from flask import Flask, flash, redirect, url_for, session, Blueprint,render_template,request
from forms import *
from database import *
from flask import flash

task_app = Blueprint('task_app', __name__)

@task_app.route('/addTask', methods=['GET', 'POST'])
def add_task():
    form = TaskForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        priority = form.priority.data
        form.name.data = ''
        form.priority.data = ''
        addTaskToDb(name, priority)
        flash('Task has been created')
    return render_template('add_task.html', form=form)

@task_app.route('/listTask', methods=['GET', 'POST'])
def list_task():
    tasks = [['sdfs', '3'], ['asda', '6']]
    return render_template('list_task.html', tasks = tasks)
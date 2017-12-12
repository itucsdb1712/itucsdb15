from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange


class AddCompanyForm(FlaskForm):
    company_name = StringField('Company Name: ', validators=[DataRequired()])
    number_of_employees = IntegerField('Number of employees: ', 
                                       validators=[DataRequired()])
    company_account_pw = StringField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SelectCompanyForm(FlaskForm):
    company_name = StringField('Company Name: ', validators=[DataRequired()])
    submitUpdate = SubmitField('Update')
    submitDelete = SubmitField('Delete')
    
class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = StringField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    name = StringField('Task name', validators=[DataRequired()])
    priority = IntegerField('priority[1-10]', validators=[DataRequired()])
    projects = SelectField('project', coerce=int)
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    surname = StringField('Surname: ', validators=[DataRequired()])
    project = SelectField('project', coerce=int)
    password = StringField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')



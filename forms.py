from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
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
    priority = IntegerField('priority[1,2,3] ', validators=[DataRequired()])
    submit = SubmitField('Submit')
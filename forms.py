from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddCompanyForm(FlaskForm):
    company_name = StringField('Company Name: ', validators=[DataRequired()])
    number_of_employees = IntegerField('Number of employees: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

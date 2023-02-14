from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Employee, Company


def choice_query():
    return Company.query

class AddEmployeeForm(FlaskForm):
    name = StringField("Employee name", [DataRequired(), Length(1, 50)])
    position = StringField("Position", [DataRequired(), Length(2, 50)])
    phone = StringField("Phone", [Length(9, 16)])
    email = StringField("Email", [DataRequired(), Length(4, 50)])
    birthday = DateField("Birthday")
    company_id = QuerySelectField("Company", query_factory=choice_query, allow_blank=False, get_label='title')
    submit = SubmitField("Create")
    
    def validate_email(form, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('This email is taken.')
    
class EmployeeForm(FlaskForm):
    name = StringField("Employee name", [DataRequired(), Length(1, 50)])
    position = StringField("Position", [DataRequired(), Length(2, 50)])
    phone = StringField("Phone", [Length(9, 16)])
    email = StringField("Email", [DataRequired(), Length(4, 50)])
    birthday = DateField("Birthday")
    company_id = QuerySelectField("Company", query_factory=choice_query, allow_blank=False, get_label='title')
    submit = SubmitField("Save")
    
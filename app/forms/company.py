from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Company


class CompanyCreationForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=4, max=100)])
    location = StringField('Location', [DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Create")

    def validate_title(form, field):
        if Company.query.filter_by(title=field.data).first():
            raise ValidationError('This title is taken.')


class CompanyForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=4, max=100)])
    location = StringField('Location', [DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Save")
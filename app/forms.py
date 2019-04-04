from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    # Login information
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    # PERSONAL INFORMATION
    # NAME
    f_name = StringField('First Name', validators=[DataRequired()])
    m_name = StringField('Middle Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    # Other
    sin    = IntegerField("SIN/SSN", validators=[DataRequired()])


    # CONTACT INFORMATION
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    phone1 = StringField('Phone Number 1', validators=[DataRequired()])
    phone2 = StringField('Phone Number 2')
    phone3 = StringField('Phone Number 3')

    # ADDRESS INFO
    country = SelectField("Country", choices=[("us", "US"), ('CAD', "Canada")], validators=[DataRequired()])
    state = StringField("State/Province", validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street_num = IntegerField("Street Number", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])

    zip = StringField('ZIP/Postal Code', validators=[DataRequired()])
    
    submit = SubmitField('Register')

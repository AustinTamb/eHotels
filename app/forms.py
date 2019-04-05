from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

class EditUserForm(FlaskForm):
    # PERSONAL INFORMATION
    # NAME
    f_name = StringField('First Name', validators=[DataRequired()])
    m_name = StringField('Middle Name', validators=[])
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

    submit = SubmitField('Update Profile')

class RegistrationForm(FlaskForm):
    # Login information
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    # PERSONAL INFORMATION
    # NAME
    f_name = StringField('First Name', validators=[DataRequired()])
    m_name = StringField('Middle Name', validators=[])
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

class AddChainForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    hotels_owned = IntegerField("Hotels Owned", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
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

    submit = SubmitField('Add Hotel Chain')

    def validate_hotels_owned(self, hotels_owned):
        if hotels_owned.data < 0:
            raise ValidationError("A Chain cannot own less than 0 Hotels.")

    def validate_rating(self, rating):
        if rating.data < 0 or rating.data > 5:
            raise ValidationError("Invalid rating range!")

class AddHotelForm(FlaskForm):
    rooms_amt = IntegerField("Rooms Owned", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    # CONTACT INFORMATION
    email = StringField('Email', validators=[DataRequired(), Email()])
    manager = IntegerField("Manager ID", validators=[DataRequired()])
    owned_by = IntegerField("Hotel Chain ID", validators=[DataRequired()])

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

    submit = SubmitField('Add Hotel Chain')

    def validate_hotels_owned(self, hotels_owned):
        if hotels_owned.data < 0:
            raise ValidationError("A Chain cannot own less than 0 Hotels.")

    def validate_rating(self, rating):
        if rating.data < 0 or rating.data > 5:
            raise ValidationError("Invalid rating range!")


class AddUserForm(FlaskForm):
    # Login information
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    priv = IntegerField("Privilege", validators=[DataRequired()])
    # PERSONAL INFORMATION
    # NAME
    f_name = StringField('First Name', validators=[DataRequired()])
    m_name = StringField('Middle Name', validators=[])
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
    
    submit = SubmitField('Add User')

    def validate_priv(self, priv):
        if priv.data > 3 or priv.data < 0:
            raise ValidationError("Invlid privilege level!")
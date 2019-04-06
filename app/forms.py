from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FloatField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from app.models import User, Hotel, Chain, Addr, Room
from app import db

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

    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first() is not None:
            raise ValidationError("Username already in use!")

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

    def validate_username(self, username):
        if User.query.filter_by(username = username.data).first() is not None:
            raise ValidationError("Username already in use!")

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

class EditChainForm(FlaskForm):
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

    submit = SubmitField('Update Hotel Chain')

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

    submit = SubmitField('Add Hotel')

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
            raise ValidationError("Invalid privilege level!")

class AddRoomForm(FlaskForm):
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    condition = StringField("Condition", validators=[DataRequired()])
    view = StringField("View", validators=[DataRequired()])
    amenities = StringField("Amenities", validators=[DataRequired()])
    extendable = SelectField("Extendable", choices=[("Yes", "Yes"), ("No", "No")], validators=[DataRequired()])
    hotel = IntegerField("Hotel ID", validators=[DataRequired()])

    submit = SubmitField('Add Room')

    def validate_hotel(self, hotel):
        h_id = hotel.data
        if Hotel.query.filter_by(id = h_id).first() is None:
            raise ValidationError("No Hotel with this ID exists.")


class SearchRoomForm(FlaskForm):
    from_date = DateField("From", validators=[DataRequired()])
    to_date = DateField("To", validators=[DataRequired()])
    city_opt = db.session.execute("SELECT Addr.city FROM Hotel, Addr WHERE Hotel.address = Addr.id").fetchall()
    cities = set()
    cities.add(("Any", "Any"))
    for c in city_opt:
        cities.add((c[0], c[0]))
    del city_opt
    city = SelectField("City", choices=cities, validators=[])

    chains = Chain.query.all()
    chain_names = [('0', "Any")]
    for c in chains:
        chain_names.append((str(c.id), c.name))
    chain = SelectField("Hotel Chain Name", choices=chain_names, validators=[])

    ratings = [("0", "Any")]
    for i in range(1, 6):
        ratings.append(
            (str(i), str(i) + " stars")
        )
    rating = SelectField("Category", choices=ratings)

    size_c = [("0", "Any")]
    for c in range(1,6):
        size_c.append((str(c), c))
    capacity = SelectField("Room Capacity", choices=size_c)

    submit = SubmitField('Search')

    def validate_from_date(self, from_date):
        if self.to_date.data and from_date:
            if from_date.data > self.to_date.data:
                raise ValidationError("From date must be smaller than the to date!")

    def validate_to_date(self, to_date):
        if self.from_date.data and to_date:
            if self.from_date.data > to_date.data:
                raise ValidationError("To date must be larger than the from date!")

class EditHotelForm(FlaskForm):
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

    submit = SubmitField('Update Hotel')

    def validate_hotels_owned(self, hotels_owned):
        if hotels_owned.data < 0:
            raise ValidationError("A Chain cannot own less than 0 Hotels.")

    def validate_rating(self, rating):
        if rating.data < 0 or rating.data > 5:
            raise ValidationError("Invalid rating range!")

    def validate_manager(self, manager):
        if User.query.get(int(manager.data)).first() == []:
            raise ValidationError("Manager does not exist!")


class EditRoomForm(FlaskForm):
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    condition = StringField("Condition", validators=[DataRequired()])
    view = StringField("View", validators=[DataRequired()])
    amenities = StringField("Amenities", validators=[DataRequired()])
    extendable = SelectField("Extendable", choices=[("Yes", "Yes"), ("No", "No")], validators=[DataRequired()])
    hotel = IntegerField("Hotel ID", validators=[DataRequired()])

    submit = SubmitField('Update Room')

    def validate_hotel(self, hotel):
        h_id = hotel.data
        if Hotel.query.filter_by(id = h_id).first() is None:
            raise ValidationError("No Hotel with this ID exists.")


class SearchBookingForm(FlaskForm):
    booking_id = IntegerField("Booking ID", validators=[Optional()])
    from_date = DateField("From", validators=[Optional()])
    city_opt = db.session.execute("SELECT Addr.city FROM Hotel, Addr WHERE Hotel.address = Addr.id").fetchall()
    cities = set()
    cities.add(("Any", "Any"))
    for c in city_opt:
        cities.add((c[0], c[0]))
    del city_opt
    city = SelectField("City", choices=cities)

    hotel = IntegerField("Hotel ID", validators=[Optional()])
    room = IntegerField("Room ID", validators=[Optional()])

    submit = SubmitField('Search')

class EditBookingForm(FlaskForm):
    checked_in = BooleanField("Customer Checked In")
    from_date = DateField("From", validators=[DataRequired()])
    to_date = DateField("To", validators=[DataRequired()])

    room = IntegerField("Room ID", validators=[DataRequired()])
    user = IntegerField("User ID", validators=[DataRequired()])

    submit = SubmitField('Update Booking')

    def validate_from_date(self, from_date):
        if self.to_date.data and from_date:
            if from_date.data > self.to_date.data:
                raise ValidationError("To date must be larger than the from date!")

    def validate_to_date(self, to_date):
        if self.from_date.data and to_date:
            if self.from_date.data > to_date.data:
                raise ValidationError("From date must be smaller than the to date!")

    def validate_user(self, user):
        if not User.query.get(user.data):
            raise ValidationError("User ID does not exist!")
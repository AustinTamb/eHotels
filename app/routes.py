from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Addr, Phone, Chain, Hotel, Room, Booking, Archive, Customer
from werkzeug.urls import url_parse
import datetime

@app.route("/")
@app.route("/index")
def index():
    user = {"username":"test"}
    return render_template(
        "index.html",
        title = "Home"
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/book_room/<int:room_id>")
@login_required
def book_room(room_id):
    print(f"ROOM ID: {room_id}")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():

        addr = Addr(
            country = form.country.data,
            state = form.state.data,
            city = form.city.data,
            street_number = form.street_num.data,
            street = form.street.data,
            zip = form.zip.data
        )
        db.session.add(addr)

        
        phone = Phone(
            phone_1 = form.phone1.data,
            phone_2 = form.phone2.data,
            phone_3 = form.phone3.data
        )
        db.session.add(phone)

        addrs = addr.id
        phone_nums = phone.id

        user = User(
            username = form.username.data,
            sin = form.sin.data,
            first_name = form.f_name.data,
            middle_name = form.m_name.data,
            last_name = form.l_name.data,
            email = form.email.data,
            address = addrs,
            phone = phone_nums
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/user/<username>")
@app.route("/user/<username>/")
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    customer = Customer.query.filter_by(user_id = user.id).first()
    bookings = None
    if customer is not None:
        bookings = Booking.query.filter_by(customer = customer.id)
        for b in bookings:
            b.image = Room.query.filter_by(id = b.room).image_url
    
    return render_template(
        'user.html', 
        user = user, 
        booking = bookings,
        c_date = datetime.datetime.utcnow()
    )

@app.route("/update_profile/<user>")
@app.route("/update_profile/<user>/")
@login_required
def update_profile(user):
    pass

@app.route("/cancel_booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    print(f"Request to cancel booking: {booking_id}")

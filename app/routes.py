from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditUserForm, AddChainForm, AddHotelForm, AddUserForm, EditChainForm
from app.models import User, Addr, Phone, Chain, Hotel, Room, Booking, Archive
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
        db.session.commit()

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
            phone = phone_nums,
            priv = 0
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/user/<username>")
@app.route("/user/<username>/")
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    bookings = Booking.query.filter_by(user = user.id)
    for b in bookings:
        b.image = Room.query.filter_by(id = b.room).image_url
    
    if bookings is None:
        bookings = {}

    return render_template(
        'user.html', 
        user = user, 
        booking = bookings,
        c_date = datetime.datetime.utcnow()
    )

@app.route("/edit_user/<username>", methods=["GET", "POST"])
@login_required
def edit_user(username):
    if current_user.priv > 1 or current_user.username == username:
        user = User.query.filter_by(username = username).first_or_404()
        addr = Addr.query.filter_by(id = user.address).first_or_404()
        ph = Phone.query.filter_by(id = user.phone).first_or_404()
        
        form = EditUserForm()
        if form.validate_on_submit():
            # Address
            edit_addr(form, addr)
            # Phone
            edit_phone(form, ph)
            
            # User Info
            user.first_name = form.f_name.data
            user.middle_name = form.m_name.data
            user.last_name = form.l_name.data
            user.email = form.email.data
            user.sin = form.sin.data
            db.session.commit()

            flash("Modifications have been saved!")
            return redirect(url_for('user', username=username))
        elif request.method == "GET":
            form.f_name.data = user.first_name
            form.m_name.data = user.middle_name
            form.l_name.data = user.last_name
            form.email.data = user.email,
            form.sin.data = user.sin

            # Address
            fill_addr_form(form, addr)
            # Phone
            fill_phone_form(form, ph)

        return render_template("/edit_type/user.html", title="Edit User", form=form, username=username)
    else:
        return redirect(url_for('user', username = username))

def edit_addr(form, addr):
    # Address
    addr.country = form.country.data
    addr.state = form.state.data
    addr.city = form.city.data
    addr.street_number = form.street_num.data
    addr.street = form.street.data
    addr.zip = form.zip.data
    db.session.commit()
    return addr.id

def fill_addr_form(form, addr):
    # Address
    form.country.data = addr.country
    form.state.data = addr.state
    form.city.data = addr.city
    form.street_num.data = addr.street_number
    form.street.data = addr.street
    form.zip.data = addr.zip

def edit_phone(form, phone):
    # Phone
    phone.phone_1 = form.phone1.data
    phone.phone_2 = form.phone2.data
    phone.phone_3 = form.phone3.data
    db.session.commit()

def fill_phone_form(form, phone):
    # Contact
    form.phone1.data = phone.phone_1
    form.phone2.data = phone.phone_2
    form.phone3.data = phone.phone_3

@app.route("/view_users")
@login_required
def view_users():
    users = User.query.all()
    return render_template("view_users.html", users = users)

@app.route("/add_room/<chain_id>/<hotel_id>", methods = ["GET", "POST"])
def add_room(chain, hotel):
    chain = Chain.query.filter_by(id = chain).first_or_404()
    hotel = Hotel.query.filter_by(id = hotel).first_or_404()
    
@app.route("/view_chains")
def view_chains():
    chains = Chain.query.all()
    return render_template("view_chains.html", chains= chains)

@app.route("/view_hotels")
def view_hotels():
    hotels = Hotel.query.all()
    return render_template("view_hotels.html", hotels = hotels)

@app.route("/add_chain", methods = ["GET", "POST"])
@login_required
def add_chain():
    form = AddChainForm()
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
        db.session.commit()

        addrs = addr.id
        phone_nums = phone.id
        
        chain = Chain(
            name = form.name.data,
            hotels_owned = form.hotels_owned.data,
            email = form.email.data,
            rating = form.rating.data,
            address = addrs,
            phone = phone_nums
        )
        db.session.add(chain)
        db.session.commit()

        flash('New Chain Added!')
        return redirect(url_for('view_chains'))
    return render_template('add_chain.html', title='Add Chain', form=form)

@app.route("/add_hotel", methods = ["GET", "POST"])
@login_required
def add_hotel():
    form = AddHotelForm()
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
        db.session.commit()

        addrs = addr.id
        phone_nums = phone.id
        
        hotel = Hotel(
            rooms_amt = form.rooms_amt.data,
            email = form.email.data,
            owned_by = form.owned_by.data,
            rating = form.rating.data,
            manager = form.manager.data,
            address = addrs,
            phone = phone_nums
        )
        db.session.add(hotel)
        db.session.commit()

        flash('New Hotel Added!')
        return redirect(url_for('view_hotels'))
    return render_template('add_hotel.html', title='Add Hotel', form=form)

@app.route("/add_user", methods = ["GET", "POST"])
@login_required
def add_user():
    form = AddUserForm()
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
        db.session.commit()

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
            phone = phone_nums,
            priv = form.priv.data
        )

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('New User Added!')
        return redirect(url_for('view_users.html'))
    return render_template('add_user.html', title='Add User', form=form)

@app.route("/edit_chain/<chain_id>", methods = ["GET", "POST"])
@login_required
def edit_chain(chain_id):
    chains = Chain.query.all()
    if current_user.priv > 1:
        chain = Chain.query.filter_by(id = chain_id).first_or_404()
        addr = Addr.query.filter_by(id = chain.address).first_or_404()
        ph = Phone.query.filter_by(id = chain.phone).first_or_404()
        
        form = EditChainForm()
        print(form.errors)
        if form.validate_on_submit():
            print("EDIT")
            # Address
            edit_addr(form, addr)
            # Phone
            edit_phone(form, ph)
            
            # User Info
            chain.name = form.name.data
            chain.hotels_owned = form.hotels_owned.data
            chain.rating = form.rating.data
            chain.email = form.email.data
            db.session.commit()

            flash("Modifications have been saved!")
            return redirect(url_for('view_chains'))
        elif request.method == "GET":
            form.name.data = chain.name
            form.hotels_owned.data = chain.hotels_owned
            form.rating.data = chain.rating
            form.email.data = chain.email

            # Address
            fill_addr_form(form, addr)
            # Phone
            fill_phone_form(form, ph)

        return render_template("add_chain.html", title="Edit Chain", form=form, chain_id = chain_id)
    else:
        return redirect(url_for('view_chains'))

@app.route("/delete_chain/<chain_id>")
@login_required
def delete_chain(chain_id):
    Chain.query.filter_by(id=chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_hotel/<hotel_id>")
@login_required
def delete_hotel(chain_id):
    Chain.query.filter_by(id=chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_user/<user_id>")
@login_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for("view_users"))


@app.route("/cancel_booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    print(f"Request to cancel booking: {booking_id}")

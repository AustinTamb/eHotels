from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditUserForm, AddChainForm, AddHotelForm, AddUserForm, EditChainForm, AddRoomForm, SearchRoomForm
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
        addr = Addr.query.get(user.address)
        ph = Phone.query.get(user.phone)
        
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
        return redirect(url_for('view_users'))
    return render_template('add_user.html', title='Add User', form=form)

@app.route("/edit_chain/<chain_id>", methods = ["GET", "POST"])
@login_required
def edit_chain(chain_id):
    chains = Chain.query.all()
    if current_user.priv > 1:
        chain = Chain.query.get(chain_id)
        addr = Addr.query.get(chain.address)
        ph = Phone.query.get(chain.phone)
        
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
    Chain.query.get(chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_hotel/<hotel_id>")
@login_required
def delete_hotel(chain_id):
    Chain.query.get(chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_user/<user_id>")
@login_required
def delete_user(user_id):
    User.query.get(user_id).delete()
    db.session.commit()
    return redirect(url_for("view_users"))

@app.route("/add_room", methods = ["GET", "POST"])
@login_required
def add_room():
    form = AddRoomForm()
    if form.validate_on_submit():
        hotel = Hotel.query.get(form.hotel.data)
        room = Room(
            capacity = form.capacity.data,
            price = form.price.data,
            condition = form.condition.data,
            view = form.view.data,
            amenities = form.amenities.data,
            extendable = form.extendable.data == "Yes",
            hotel_id = form.hotel.data
        )
        db.session.add(room)
        hotel.rooms_amt += 1
        db.session.commit()

        flash('New Room Added!')
        return redirect(url_for('view_rooms'))
    return render_template('add_type/room.html', title='Add Room', form=form)

@app.route("/view_rooms")
@login_required
def view_rooms():
    rooms = Room.query.all()
    return render_template("view_rooms.html", rooms=rooms, title="View Rooms")

@app.route("/delete_room/<room_id>")
@login_required
def delete_room(room_id):
    Room.query.get(room_id).delete()
    db.session.commit()
    return redirect(url_for('view_rooms'))

@app.route("/browse_rooms", methods=["GET", "POST"])
@login_required
def browse_rooms():
    form = SearchRoomForm()
    if request.method == "POST":
        rooms = []
        if (form.chain.data != -1):
            f_rooms = db.session.execute(
                "SELECT Room.id FROM Room, Hotel WHERE Room.hotel_id = Hotel.id AND Hotel.owned_by=:param", 
                {"param":form.chain.data}
            ).fetchall()

            rooms = [Room.query.get(i) for i in f_rooms]
        if (form.chain.data == -1):
            rooms = Room.query.all()

        return render_template("browse_rooms.html", form=form, result = rooms)
    elif request.method == "GET":
        pass
    return render_template("browse_rooms.html", form=form)
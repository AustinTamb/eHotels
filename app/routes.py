from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import *
from app.models import *
from werkzeug.urls import url_parse
import datetime

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        form = SearchRoomForm()
    else:
        form = RegistrationForm()
    return render_template(
            "index.html",
            title = "Home",
            form = form
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
    booking_slots = Booking.query.filter_by(user = user.id)
    
    if booking_slots is None:
        booking_slots = {}
    else:
        booking_slots = [get_booking_info(b) for b in booking_slots]
        print(booking_slots)
    return render_template(
        'user.html', 
        user = user,
        booking = booking_slots,
        c_date = datetime.date.today()
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
            form.email.data = str(user.email),
            form.email.data = form.email.data[0]
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
    if current_user.priv > 1:
        chain = Chain.query.get(chain_id)
        addr = Addr.query.get(chain.address)
        ph = Phone.query.get(chain.phone)
        
        form = EditChainForm()
        if form.validate_on_submit():
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

@app.route("/edit_hotel/<hotel_id>", methods = ["GET", "POST"])
@login_required
def edit_hotel(hotel_id):
    if current_user.priv > 1:
        hotel = Hotel.query.get(hotel_id)
        addr = Addr.query.get(hotel.address)
        ph = Phone.query.get(hotel.phone)
        
        form = EditHotelForm()
        if form.validate_on_submit():
            # Address
            edit_addr(form, addr)
            # Phone
            edit_phone(form, ph)
            
            # User Info
            hotel.rooms_amt = form.rooms_amt.data
            chain.manager = form.manager.data
            chain.rating = form.rating.data
            chain.email = form.email.data
            chain.owned_by = form.owned_by.data
            db.session.commit()

            flash("Modifications have been saved!")
            return redirect(url_for('view_hotels'))
        elif request.method == "GET":
            form.rooms_amt.data = hotel.rooms_amt
            form.manager.data = hotel.manager
            form.rating.data = hotel.rating
            form.email.data = hotel.email
            form.owned_by.data = hotel.owned_by

            # Address
            fill_addr_form(form, addr)
            # Phone
            fill_phone_form(form, ph)

        return render_template("add_hotel.html", title="Edit Hotel", form=form, hotel_id = hotel_id)
    else:
        return redirect(url_for('view_hotels'))

@app.route("/edit_room/<room_id>", methods = ["GET", "POST"])
@login_required
def edit_room(room_id):
    if current_user.priv > 1:
        room = Room.query.get(room_id)
        
        form = EditRoomForm()
        if form.validate_on_submit():
            
            # User Info
            room.capacity = form.capacity.data
            room.price = 100 * form.price.data
            room.condition = form.condition.data
            room.view = form.view.data
            room.amenities = form.amenities.data
            room.extendable = form.extendable.data == "Yes"
            room.hotel_id = form.hotel.data
            db.session.commit()

            flash("Modifications have been saved!")
            return redirect(url_for('view_rooms'))
        elif request.method == "GET":
            form.capacity.data = room.capacity
            form.price.data = int(room.price) / 100.00
            form.condition.data = room.condition
            form.view.data = room.view
            form.amenities.data = room.amenities
            form.extendable.data = "Yes" if room.extendable else "No"
            form.hotel.data = room.hotel_id

        return render_template("add_type/room.html", title="Edit Room", form=form, room_id = room_id)
    else:
        return redirect(url_for('view_rooms'))

@app.route("/delete_chain/<chain_id>")
@login_required
def delete_chain(chain_id):
    db.session.delete(Chain.query.get(chain_id))
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_hotel/<hotel_id>")
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    chain = Chain.query.get(hotel.owned_by)
    chain.hotels_owned -= 1
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_user/<user_id>")
@login_required
def delete_user(user_id):
    db.session.delete(User.query.get(user_id))
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
            price = int(form.price.data * 100),
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

def get_booking_info(booking):
    room = Room.query.get(booking.room)
    booking.room_info = get_room_info(room)
    return booking

def get_room_info(room):
    hotel = Hotel.query.get(room.hotel_id)
    chain = Chain.query.get(hotel.owned_by)
    room.room_addr = str(Addr.query.get(hotel.address))
    room.chain_info = chain
    return room

@app.route("/view_rooms")
@login_required
def view_rooms():
    rooms = Room.query.all()
    return render_template("view_rooms.html", rooms=rooms, title="View Rooms")

@app.route("/delete_room/<room_id>")
@login_required
def delete_room(room_id):
    room = Room.query.get(room_id)
    hotel = Hotel.query.get(room.hotel_id)
    hotel.rooms_amt -= 1
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('view_rooms'))

@app.route("/browse_rooms", methods=["GET", "POST"])
def browse_rooms():
    form = SearchRoomForm()
    if form.validate_on_submit():
        filter_applied = False
        q = db.session.query(Room, Hotel, Chain, Addr)
        
        city = str(form.city.data)
        if city != "Any":
            q = q.filter(
                Hotel.id == Room.hotel_id, 
                Hotel.address == Addr.id, 
                Addr.city == city
            )
            filter_applied = True
    
        hotel_chain = int(form.chain.data)
        if hotel_chain != 0:
            q = q.filter(
                Room.hotel_id == Hotel.id, 
                Hotel.owned_by == hotel_chain
            )
            filter_applied = True

        rating = int(form.rating.data)
        if rating != 0:
            q = q.filter(Hotel.rating == rating)
            filter_applied = True

        capacity = int(form.capacity.data)
        if capacity != 0:
            q = q.filter(Room.capacity == capacity)
            filter_applied = True

        if filter_applied:
            rooms = set([r[0] for r in q.all()])
        else:
            rooms = set(Room.query.all())

        if BookingSlot.query.all() != []:
            c = db.session.query(Room, BookingSlot)\
            .filter(Room.id == BookingSlot.room)\
            .filter(BookingSlot.date.between(form.from_date.data, form.to_date.data))
            c = set([r[0] for r in c.all()])
            # Remove already booked rooms
            rooms -= c
            del c

        rooms = [get_room_info(r) for r in rooms]
        return render_template("browse_rooms.html", form=form, result = set(rooms))
    return render_template("browse_rooms.html", form=form)


@app.route("/book_room/<room_id>/<from_date>/<to_date>")
@login_required
def book_room(room_id, from_date, to_date):
    start = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    booking = Booking(
        checked_in = False,
        from_date = start,
        to_date = end,
        room = room_id,
        user = current_user.id
    )
    db.session.add(booking)

    for date in date_generated:
        tmp_booking = BookingSlot(
            room = room_id,
            date = date
        )
        db.session.add(tmp_booking)
    
    db.session.commit()
    form = SearchRoomForm()
    flash(f"Your booking for the room has be registered. Your booking id is: {booking.id}.")
    return render_template("browse_rooms.html", form=form)

@app.route("/cancel_booking/<booking_id>")
@login_required
def cancel_booking(booking_id):
    # Get the Booking
    booking = Booking.query.get(booking_id)
    # Create the archive
    arch = Archive(
        checked_in = booking.checked_in,
        from_date = booking.from_date,
        to_date = booking.to_date,
        room= booking.room,
        user = booking.user
    )

    # Get the range of the dates reserved for that booking
    start = arch.from_date
    end = arch.to_date
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for date in date_generated:
        # Delete all the BookingSlot
        BookingSlot.query.filter_by(
            room = booking.room,
            date = date
        ).delete()

    # Delete the booking
    db.session.delete(booking)
    # Add the archive to db
    db.session.add(arch)
    # Commit all changes from above
    db.session.commit()
    # Get the user
    user = User.query.get(arch.user)
    # RE-generate user page
    return redirect(url_for('user', username = user.username))


@app.route("/browse_bookings", methods = ["GET", "POST"])
@login_required
def browse_bookings():
    form = SearchBookingForm()
    if form.validate_on_submit():
        # Get dates
        # Get all rooms not booked between date range
        if form.booking_id.data:
            booking = Booking.query.get(form.booking_id.data)
            if booking:
                return render_template("browse_bookings.html", form=form, c_date = datetime.date.today(), booking = [get_booking_info(booking)])
        
        q = db.session.query(Booking, Room, Hotel, Addr)

        filter_applied = False

        from_date = form.from_date.data
        if from_date:
            q = q.filter(Booking.from_date == from_date)
            filter_applied = True

        room_id = form.room.data
        if room_id:
            q = q.filter(Booking.room == room_id)
            filter_applied = True

        hotel_id = form.hotel.data
        if hotel_id:
            # Filter on rooms with the hotel_id field being the one passed and the 
            # Bookings with that room id in it
            q = q.filter(
                Room.hotel_id == hotel_id, 
                Booking.room == Room.id
            )
            filter_applied = True

        city = form.city.data
        if city != "Any":
            q = q.filter(
                Booking.room == Room.id,
                Hotel.id == Room.hotel_id,
                Addr.id == Hotel.address,
                Addr.city == city
            )
            filter_applied = True

        if filter_applied:
            bookings = [b[0] for b in q.all()]
        else:
            bookings = Booking.query.all()

        bookings = [get_booking_info(b) for b in bookings]
        return render_template("browse_bookings.html", form=form, c_date = datetime.date.today(), booking = bookings)
    return render_template("browse_bookings.html", form=form)


@app.route("/edit_booking/<booking_id>", methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    if current_user.priv > 0:
        booking = Booking.query.get(booking_id)
        
        form = EditBookingForm()
        if form.validate_on_submit():
            
            # User Info
            booking.checked_in = form.checked_in.data
            booking.from_date = form.from_date.data
            booking.to_date = form.to_date.data
            booking.room = form.room.data
            booking.user = form.user.data

            db.session.commit()

            flash("Modifications have been saved!")
            return render_template("edit_type/booking.html", title="Edit Booking", form=form, booking_id = booking_id)
        elif request.method == "GET":
            form.checked_in.data = booking.checked_in
            form.from_date.data = booking.from_date
            form.to_date.data = booking.to_date
            form.room.data = booking.room
            form.user.data = booking.user

        return render_template("edit_type/booking.html", title="Edit Booking", form=form, booking_id = booking_id)
    else:
        return render_template('browse_bookings.html')
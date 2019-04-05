from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditUserForm, AddChainForm, AddHotelForm
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template()


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

@app.route("/book_room/<user_id>/<int:room_id>")
@login_required
def book_room(user_id, room_id):
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

@app.route("/edit_user/<username>/", methods=["GET", "POST"])
def edit_user(username):
    if current_user.priv > 1 or current_user.username == username:
        user = User.query.filter_by(username = username).first_or_404()
        addr = Addr.query.filter_by(id = user.address).first_or_404()
        ph = Phone.query.filter_by(id = user.phone).first_or_404()
        
        form = EditUserForm()
        if form.validate_on_submit():
            # Address
            addr.country = form.country.data
            addr.state = form.state.data
            addr.city = form.city.data
            addr.street_number = form.street_num.data
            addr.street = form.street.data
            addr.zip = form.zip.data
            db.session.commit()

            # Phone
            ph.phone_1 = form.phone1.data
            ph.phone_2 = form.phone2.data
            ph.phone_3 = form.phone3.data
            db.session.commit()

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
            form.country.data = addr.country
            form.state.data = addr.state
            form.city.data = addr.city
            form.street_num.data = addr.street_number
            form.street.data = addr.street
            form.zip.data = addr.zip
            # Contact
            form.phone1.data = ph.phone_1
            form.phone2.data = ph.phone_2
            form.phone3.data = ph.phone_3
        return render_template("/edit_type/user.html", title="Edit User", form=form, username=username)
    else:
        return redirect(url_for('user', username = username))

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


@app.route("/delete_chain/<chain_id>")
def delete_chain(chain_id):
    Chain.query.filter_by(id=chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/delete_hotel/<hotel_id>")
def delete_hotel(chain_id):
    Chain.query.filter_by(id=chain_id).delete()
    db.session.commit()
    return redirect(url_for("view_chains"))

@app.route("/cancel_booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    print(f"Request to cancel booking: {booking_id}")

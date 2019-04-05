from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    username    = db.Column(db.String(64), index = True, unique = True)
    pwd_hash    = db.Column(db.String(128))
    sin         = db.Column(db.Integer, nullable = False)
    first_name  = db.Column(db.String(32), nullable = False)
    middle_name = db.Column(db.String(32), nullable = True)
    last_name   = db.Column(db.String(32), nullable = False)
    email       = db.Column(db.String(128), nullable = False)
    priv        = db.Column(db.Integer, nullable = False, default = 0)

    address     = db.Column(db.Integer, db.ForeignKey('addr.id'))
    phone       = db.Column(db.Integer, db.ForeignKey('phone.id'))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

class Phone(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    phone_1     = db.Column(db.String(9), nullable = False)
    phone_2     = db.Column(db.String(9))
    phone_3     = db.Column(db.String(9))

class Addr(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    zip         = db.Column(db.String(6), nullable = False)
    city        = db.Column(db.String(64), nullable = False)
    street      = db.Column(db.String(64), nullable = False)
    street_number = db.Column(db.Integer, nullable = False)
    state       = db.Column(db.String(64), nullable = False)
    country     = db.Column(db.String(64), nullable = False)


class Chain(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(64), nullable = False)
    hotels_owned = db.Column(db.Integer, nullable = False)
    email       = db.Column(db.String(128), nullable = False)
    rating      = db.Column(db.Integer, nullable = False)
    
    address     = db.Column(db.Integer, db.ForeignKey('addr.id'))
    phone       = db.Column(db.Integer, db.ForeignKey('phone.id'))

    hotels      = db.relationship('Hotel', backref = 'chain', lazy='dynamic')

class Hotel(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    rooms_amt   = db.Column(db.Integer, nullable = False)
    rating      = db.Column(db.Integer, nullable = False)
    email       = db.Column(db.String(128), nullable = False)

    address     = db.Column(db.Integer, db.ForeignKey('addr.id'))
    phone       = db.Column(db.Integer, db.ForeignKey('phone.id'))
    manager     = db.Column(db.Integer, db.ForeignKey('user.id'))
    owned_by    = db.Column(db.Integer, db.ForeignKey('chain.id'))
    
    rooms       = db.relationship("Room", backref = 'hotel', lazy='dynamic')

class Room(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    capacity    = db.Column(db.Integer, nullable = False)
    price       = db.Column(db.Numeric(precision=2), nullable = False)
    condition   = db.Column(db.String(256), nullable = False)
    view        = db.Column(db.String(256), nullable = False)
    amenities   = db.Column(db.String(256), nullable = False)
    extendable  = db.Column(db.Boolean, nullable = False)
    hotel_id    = db.Column(db.Integer, db.ForeignKey('hotel.id'))


class Booking(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    checked_in  = db.Column(db.Boolean, nullable = False)
    from_date   = db.Column(db.Date, unique = True)
    to_date     = db.Column(db.Date, unique = True)

    room        = db.Column(db.Integer, db.ForeignKey('room.id'))
    user        = db.Column(db.Integer, db.ForeignKey('user.id'))

    archive     = db.relationship('Archive', backref = 'a_booking', lazy='dynamic')

class Bookings(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    room        = db.Column(db.Integer, db.ForeignKey('room.id'))
    date        = db.Column(db.Date, index = True)

class Archive(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    book_id     = db.Column(db.Integer, db.ForeignKey('booking.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
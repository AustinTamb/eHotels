import os
from .User import User
from .Config.Config import Config
from flask import Flask, render_template, request, send_file, session, url_for
from flask_login import LoginManager
from Server.db_manager import DBManager

CONFIG_PATH     = 'C:\\Users\\XPS\\Desktop\\CSI2132_Project\\eHotels\\Server\\Config\\config.conf'

#db_handler = DBManager.instance()

app             = Flask(__name__)
config          = Config(CONFIG_PATH)

app.secret_key  = bytes(config.APP_INFO.secret_key, "utf-8")

login_manager   = LoginManager()

rooms = [
    {
        "room_id": 0,
        "capacity":2,
        "price":200,
        "image": "room1"
    },
    {
        "room_id": 1,
        "capacity":1,
        "price":200,
        "image": "room2"
    },
    {
        "room_id": 2,
        "capacity":4,
        "price":200,
        "image": "room3"
    },
    {
        "room_id": 3,
        "capacity":2,
        "price":2000,
        "image": "room4"
    }
]

@app.route("/", methods = ["GET"])
def root():
    return render_template("index.html", title="Home")

'''
LOGIN SECTION
'''
@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        # HANDLE GET - Return login form
        return render_template("login.html", title="Login")
    elif request.method == "POST":
        print(request.form)
        # HANDLE POST - Validate login
        return render_template("index.html", title="Home")
    pass


@app.route("/browse_rooms")
def browse_rooms():
    return render_template("browse_rooms.html", title = "Rooms", rooms = rooms)


@app.route('/room_info/<int:room_id>')
def get_room_info(room_id):
    print("GET ROOM!")
    return render_template("room_info.html", title = "Room Info")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/get_image", methods = ["GET"])
def get_image():
    """
    Gets an image stored on the server if it exists.
    """
    requested_img_name = request.args.get("image")
    # Sanitize the requested name
    sanitized_img_name = requested_img_name.replace(".", "")

    # Clean memory
    del requested_img_name

    # Get the path to the image
    image = f'{config.PATHS.uploads}\\{sanitized_img_name}.jpg'

    # Clean memory
    del sanitized_img_name

    # Ensure the path exists
    if not os.path.exists(image):
        print(f"{image} - not found!")
        return ""

    # Return the file if it's found
    return send_file(image, mimetype='image/gif')


def run(debug : bool):
    login_manager.init_app(app)
    app.run(port = 48879, debug = debug)
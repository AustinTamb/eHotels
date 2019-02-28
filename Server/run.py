import os
from flask import Flask, render_template, request, send_file


app = Flask(__name__)


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

@app.route("/browse_rooms")
def browse_rooms():
    return render_template("browse_rooms.html", title = "Rooms", rooms = rooms)


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
    image = f'{os.getcwd()}\\Server\\uploads\\{sanitized_img_name}.jpg'

    # Clean memory
    del sanitized_img_name

    # Ensure the path exists
    if not os.path.exists(image):
        print(f"{image} - not found!")
        return ""

    # Return the file if it's found
    return send_file(image, mimetype='image/gif')


def run(debug : bool):
    app.run(port = 48879, debug = debug)
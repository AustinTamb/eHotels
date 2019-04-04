import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Config class.
    """
    SECRET_KEY = "+y2$KPng$5_8_M#$"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
        os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
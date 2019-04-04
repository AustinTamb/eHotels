class User(object):
    def __init__(self):
        self.logged_in = False

    def login(self, username, password):
        _user = username
        _pass = password

        if 


    @property
    def is_active(self):
        return self.logged_in

    

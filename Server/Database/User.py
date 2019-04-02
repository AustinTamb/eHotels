

#TODO:WIP
class User:

    def __init__(self, username, password, name):
        self._username = username
        self._password = password
        self._name = name
        self._authenticated = False


    def login(self, password):
        if password == self._password:
            self._authenticated = True
        return self.is_authenticated()

    def logout(self):
        self.is_authenticated = False

    def get_name(self):
        return self._name

    def is_authenticated(self):
        return self._authenticated

    


#TODO:WIP
class User:

    def __init__(self, user_id, user, password):
        self.authenticated = False
        self.is_active     = False


    def is_authenticated(self):
        return self.authenticated

    
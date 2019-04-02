from contextlib import contextmanager
from .User import User
import sqlite3

class DBManager:
    def __init__(self):
        # Setup to have no connection
        self._connection = None
        self.create_tables()

    def __del__(self):
        """
            Cleans up connections on the deletion of
            the class isntance.
        """
        if self._connection is not None:
            self._connection.close()
        del self._connection

    def create_tables(self):
        # Get a connection to the db
        with self.get_connection() as db:
            db.cursor().execute("""
            CREATE TABLE IF NOT EXISTS User(
                username TEXT PRIMARY KEY, 
                password TEXT NOT NULL,
                name     TEXT NOT NULL
            )
            """)
            db.commit()


    def get_user(self):
        #TODO: Query for system user
        #TODO: Create User object and return it
        pass


    def generic_query(self, table_name, values, conditions = None):
        """
            Generic query, make more queries where necessary
        """
        query = f"SELECT {values} FROM {table_name}"

        if conditions is not None:
            query += f" WHERE {conditions}"
        ret = []
        print(f"Query: {query}")
        with self.get_connection() as db:
            tmp = db.cursor()
            qry = tmp.execute(query)
            ret = qry.fetchone()
        return ret

    def add_user(self, user, password, name):
        """
            Method to add a new user
        """
        query = f"""
            INSERT INTO User(username, password, name)
            VALUES (
                '{user}', 
                '{password}', 
                '{name}'
            )
        """
        print(query)
        with self.get_connection() as db:
            db.cursor().execute(query)
            db.commit()

    def get_user(self, username):
        user = self.generic_query("User", "*", f"username = '{username}'")
        print(user)

        if user is None:
            return None

        tmp = User(user[0], user[1], user[2])
        return tmp


    #TODO: Need methods to add entries in table

    #TODO: Need methods to query for entries in the tables.

    #TODO:

    @contextmanager
    def get_connection(self):
        """
        Generator to yield a connection to the database to be used 
        in contexts.
        """
        try:
            # If there's no connection created
            if self._connection is None:
                # Make one
                self._connection = sqlite3.connect('eHotels.db')
        except:
            print("Failed to open connection to db!")
        else:
            yield self._connection
        finally:
            self._connection.close()
            self._connection = None

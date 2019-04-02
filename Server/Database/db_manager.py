from contextlib import contextmanager
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
                password TEXT NOT NULL
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
        
        print(f"Query: {query}")
        with self.get_connection() as db:
            return [entry for entry in db.cursor().execute(query)]

    def add_user(self, user, password):
        """
            Method to add a new user
        """
        with self.get_connection() as db:
            db.cursor().execute(f"""
                INSERT INTO User(username, password) 
                VALUES ('{user}', '{password}')
            """)
            db.commit()

    def get_user(self, username):
        return self.generic_query("User", "*", f"username = '{username}'")


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

from contextlib import contextmanager
from Server.Database.User import User
import sqlite3

class DBManager:
    def __init__(self):
        # Setup to have no connection
        self._connection = None

    def __del__(self):
        """
            Cleans up connections on the deletion of
            the class isntance.
        """
        if self._connection is not None:
            self._connection.close()
        del self._connection

    def create_tables(self):
        # TODO: DO this properly
        # Opens the schema.sql file in the database folder
        with open("Database/Schema.sql") as file:
            # Get a connection to the db
            with self.get_connection() as db:

                for i in file.read().split(";"):
                    db.execute(i)


    def get_user(self):
        #TODO: Query for system user
        #TODO: Create User object and return it
        pass

    def add_hotel_chain(self, hotel_name):
        pass


    def generic_query(self, table_name, values, conditions = None):
        """
        Generic query, make more queries where necessary
        """
        query = f"SELECT {values} FROM {table_name}"

        if conditions is not None:
            query += f" WHERE {conditions}"
        
        with self.get_connection() as db:
            return db.cursor().execute(query)


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

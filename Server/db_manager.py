from Server.Singleton import Singleton
from contextlib import contextmanager
import mysql.connector

class DBManager(Singleton):
    def __init__(self, host, user, password):
        self._connection = get_connection()
        self._hostname = host
        self._user = user
        self._password = password


    def send_query(self, query):
        with self._connection as db:
            #TODO: Send query
            print(db)


    @contextmanager
    def get_connection(self):
        """
        Generator to yield a connection to the database to be used 
        in contexts.
        """
        db = None
        try:
            db = mysql.connector.connect(
                host = self._hostname,
                user = self._username,
                passwd = self._password
            )
        except:
            print("ERROR OCCURED!")
        else:
            yield db
        finally:
            if isinstance(db, mysql.connector.CMySQLConnection):
                db.close()
            db = None

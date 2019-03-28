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
        result = ""
        with self._connection.cursor() as db:
            db.execute(query)

            result += "\n".join(f"{entry}" for entry in db)
        
        return result


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
            yield cursor
        finally:
            if isinstance(db, mysql.connector.MySQLConnection):
                db.close()
            db = None

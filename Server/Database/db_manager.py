from contextlib import contextmanager
from Database.User import User
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

    #creates the Database
    def create_tables(self):
        # Get a connection to the db
        with self.get_connection() as db:
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS HotelChain(
                    hotel_chain_id      VARCHAR(15)                 NOT NULL PRIMARY KEY,
                    hotel_chain_name    VARCHAR(30)                 NOT NULL
                );
            )
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Hotel(
                    hotel_id VARCHAR(15) NOT NULL PRIMARY KEY,
                    hotel_chain_id      VARCHAR(15)                 NOT NULL,
                    hotel_name          VARCHAR(30)                 NOT NULL,
                    rating              ENUM('5','4','3','2','1')   NULL,
                    FOREIGN KEY (hotel_chain_id) REFERENCES HotelChain(hotel_chain_id)
                );
            ) 
            
            db.cursor().execute(
               CREATE TABLE IF NOT EXISTS Room(
                    room_id             VARCHAR(10)                 NOT NULL PRIMARY KEY,
                    capacity            INT                         NOT NULL,
                    hotel_id            VARCHAR(15)                 NOT NULL,
                    available           bit                         NOT NULL,
                    room_conditation    VARCHAR(50)                 NOT NULL,
                    room_view           TEXT                        NOT NULL,
                    amenities           VARCHAR(50)                 NOT NULL,
                    price               DECIMAL(20,2)               NOT NULL,
                    extendable          bit                         NOT NULL,
                    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id)
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS RoomOccupation(
                    booking_id          INT                         NOT NULL PRIMARY KEY,
                    room_id             VARCHAR(15)                 NOT NULL,
                    checked_in          bit                         NOT NULL,
                    from_date           DATE                        NOT NULL,
                    to_date             DATE                        NOT NULL,
                    stay_duration       VARCHAR(15)                 NOT NULL,
                    FOREIGN KEY (room_id) REFERENCES Room(room_id)
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Person(
                    SIN                 VARCHAR(15)                 NOT NULL PRIMARY KEY,
                    first_name          VARCHAR(20)                 NOT NULL,
                    last_name           VARCHAR(20)                 NOT NULL,
                    type                TEXT                        NOT NULL
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Address(
                    ZIP                 CHAR(6)                     NOT NULL,
                    city                VARCHAR(15)                 NOT NULL,
                    street              VARCHAR(15)                 NOT NULL,
                    street_number       INT                         NOT NULL,
                    state               VARCHAR(15)                 NOT NULL,
                    hotel_chain_id      VARCHAR(15)                 NULL,
                    hotel_id            VARCHAR(15)                 NULL,
                    SIN                 VARCHAR(15)                 NULL,
                    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
                    FOREIGN KEY (hotel_chain_id) REFERENCES HotelChain(hotel_chain_id),
                    FOREIGN KEY (SIN) REFERENCES Person(SIN)
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Contact(
                    phone_number        CHAR(12)                    NULL,
                    email               VARCHAR(30)                 NOT NULL,
                    hotel_chain_id      VARCHAR(15)                 NULL,
                    hotel_id            VARCHAR(15)                 NULL,
                    SIN                 VARCHAR(15)                 NULL,
                    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
                    FOREIGN KEY (hotel_chain_id) REFERENCES HotelChain(hotel_chain_id),
                    FOREIGN KEY (SIN) REFERENCES Person(SIN)
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Employee(
                    employee_id         VARCHAR(15)                 NOT NULL PRIMARY KEY,
                    hotel_id            VARCHAR(15)                 NOT NULL,
                    booking_id          INT                         NOT NULL,
                    position            VARCHAR(15)                 NOT NULL,
                    hours               INT                         NOT NULL,
                    salary              DECIMAL(15,2)               NOT NULL, 
                    start_date          DATE                        NOT NULL,
                    SIN                 VARCHAR(15)                 NULL,
                    type                TEXT                        NOT NULL,
                    FOREIGN KEY (SIN) REFERENCES Person(SIN),
                    FOREIGN KEY (type) REFERENCES Person(type),
                    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
                    FOREIGN KEY (booking_id) REFERENCES RoomOccupation(booking_id)
                );
            )
            
            db.cursor().execute(
                CREATE TABLE IF NOT EXISTS Customer(
                    guest_status        VARCHAR(15)                 NOT NULL,
                    booking_id          INT                         NOT NULL,
                    amount_due          DECIMAL(20,2)               NOT NULL, 
                    registration_date   DATE                        NOT NULL,
                    SIN                 VARCHAR(15)                 NULL,
                    type                TEXT                        NOT NULL,
                    FOREIGN KEY (SIN) REFERENCES Person(SIN),
                    FOREIGN KEY (type) REFERENCES Person(type),
                    FOREIGN KEY (booking_id) REFERENCES RoomOccupation(booking_id)
                );
            )
           
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

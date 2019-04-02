CREATE TABLE HotelChain(
    hotel_chain_id      INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
    hotel_chain_name    TEXT        NOT NULL
);

CREATE TABLE Hotel(
    hotel_id            INTEGER     NOT NULL PRIMARY KEY,
    hotel_chain_id      INTEGER     NOT NULL,
    hotel_name          TEXT        NOT NULL,
    rating              INTEGER     NOT NULL,
    FOREIGN KEY(hotel_chain_id) REFERENCES HotelChain(hotel_chain_id),
);

CREATE TABLE HotelChain_Hotel(
    hotel_chain_id      INTEGER,
    hotel_id            INTEGER,
    FOREIGN KEY(hotel_id)       REFERENCES Hotel(hotel_id),
    FOREIGN KEY(hotel_chain_id) REFERENCES HotelChain(hotel_chain_id)
);

CREATE TABLE Room(
    room_id             INTEGER     NOT NULL PRIMARY KEY,
    capacity            INTEGER     NOT NULL,
    hotel_id            INTEGER     NOT NULL,
    available           INTEGER     NOT NULL,       -- Boolean
    FOREIGN KEY(hotel_id) REFERENCES Hotel(hotel_id),
    room_conditation    TEXT        NOT NULL,
    room_view           TEXT        NOT NULL,
    amenities           TEXT        NOT NULL,
    price               REAL        NOT NULL,
    extendable          INTEGER     NOT NULL        -- Boolean
);


CREATE TABLE RoomOccupation(
    booking_id          INTEGER     NOT NULL PRIMARY KEY,
    room_id             INTEGER     NOT NULL,
    FOREIGN KEY(room_id) REFERENCES Room(room_id),
    checked_in          INTEGER     NOT NULL,       -- Boolean
    from_date           DATE        NOT NULL,
    to_date             DATE        NOT NULL,
    stay_duration       INTEGER     NOT NULL
);

CREATE TABLE Address(
    ZIP                 CHAR(6)                     NOT NULL,
    city                VARCHAR(15)                 NOT NULL,
    street              VARCHAR(15)                 NOT NULL,
    street_number       INT                         NOT NULL,
    state               VARCHAR(15)                 NOT NULL,
    hotel_chain_id      VARCHAR(15)                 NULL,
    hotel_id            VARCHAR(15)                 NULL,
    SIN                 VARCHAR(15)                 NULL
);

CREATE TABLE Contact(
    phone_number        CHAR(12)                    NULL,
    email               VARCHAR(30)                 NOT NULL,
    hotel_chain_id      VARCHAR(15)                 NULL,
    hotel_id            VARCHAR(15)                 NULL,
    SIN                 VARCHAR(15)                 NULL
);

CREATE TABLE Person(
    SIN                 VARCHAR(15)                 NOT NULL PRIMARY KEY,
    first_name          VARCHAR(20)                 NOT NULL,
    last_name           VARCHAR(20)                 NOT NULL
);

CREATE TABLE Employee(
    employee_id         VARCHAR(15)                 NOT NULL PRIMARY KEY,
    information         VARCHAR(15)                 NOT NULL FOREIGN KEY,
    hotel_id            VARCHAR(15)                 NOT NULL FOREIGN KEY,
    booking_id          INT                         NOT NULL FOREIGN KEY,
    position            VARCHAR(15)                 NOT NULL,
    hours               INT                         NOT NULL,
    salary              DECIMAL(15,2)               NOT NULL, 
    start_date          DATE                        NOT NULL
);

CREATE TABLE Customer(
    guest_status        VARCHAR(15)                 NOT NULL,
    information         VARCHAR(15)                 NOT NULL FOREIGN KEY,
    booking_id          INT                         NOT NULL FOREIGN KEY,
    amount_due          DECIMAL(20,2)               NOT NULL, 
    registration_date   DATE                        NOT NULL
);
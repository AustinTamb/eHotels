CREATE TABLE HotelChain(
    hotel_chain_id      VARCHAR(15)                 NOT NULL PRIMARY KEY,
    hotel_chain_name    VARCHAR(30)                 NOT NULL
);

CREATE TABLE Hotel(
    hotel_id            VARCHAR(15)                 NOT NULL PRIMARY KEY,
    hotel_chain_id      VARCHAR(15)                 NOT NULL,
    hotel_name          VARCHAR(30)                 NOT NULL,
    rating              ENUM('5','4','3','2','1')   NULL,
    FOREIGN KEY (hotel_chain_id) REFERENCES HotelChain(hotel_chain_id)
);

CREATE TABLE Room(
    room_id             VARCHAR(10)                 NOT NULL PRIMARY KEY,
    capacity            TINYINT                     NOT NULL,
    hotel_id            VARCHAR(15)                 NOT NULL,
    available           bit                         NOT NULL,
    room_conditation    VARCHAR(50)                 NOT NULL,
    room_view           ENUM('Mountain','Sea')      NOT NULL,
    amenities           VARCHAR(50)                 NOT NULL,
    price               DECIMAL(20,2)               NOT NULL,
    extendable          bit                         NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id)
);

CREATE TABLE RoomOccupation(
    booking_id          INT                         NOT NULL PRIMARY KEY,
    room_id             VARCHAR(15)                 NOT NULL,
    checked_in          bit                         NOT NULL,
    from_date           DATE                        NOT NULL,
    to_date             DATE                        NOT NULL,
    stay_duration       VARCHAR(15)                 NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

CREATE TABLE Person(
    SIN                 VARCHAR(15)                 NOT NULL PRIMARY KEY,
    first_name          VARCHAR(20)                 NOT NULL,
    last_name           VARCHAR(20)                 NOT NULL,
    type                ENUM('Guest','Employee')    NOT NULL
);

CREATE TABLE Address02(
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

CREATE TABLE Contact(
    phone_number        CHAR(12)                    NULL,
    email               VARCHAR(30)                 NOT NULL,
    hotel_chain_id      VARCHAR(15)                 NULL,
    hotel_id            VARCHAR(15)                 NULL,
    SIN                 VARCHAR(15)                 NULL,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
    FOREIGN KEY (hotel_chain_id) REFERENCES HotelChain(hotel_chain_id),
    FOREIGN KEY (SIN) REFERENCES Person(SIN)
);

CREATE TABLE Employee(
    employee_id         VARCHAR(15)                 NOT NULL PRIMARY KEY,
    hotel_id            VARCHAR(15)                 NOT NULL,
    booking_id          INT                         NOT NULL,
    position            VARCHAR(15)                 NOT NULL,
    hours               INT                         NOT NULL,
    salary              DECIMAL(15,2)               NOT NULL, 
    start_date          DATE                        NOT NULL,
    SIN                 VARCHAR(15)                 NULL,
    type                ENUM('Guest','Employee')    NOT NULL,
    FOREIGN KEY (SIN) REFERENCES Person(SIN),
    FOREIGN KEY (type) REFERENCES Person(type),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
    FOREIGN KEY (booking_id) REFERENCES RoomOccupation(booking_id)
);

CREATE TABLE Customer(
    guest_status        VARCHAR(15)                 NOT NULL,
    booking_id          INT                         NOT NULL,
    amount_due          DECIMAL(20,2)               NOT NULL, 
    registration_date   DATE                        NOT NULL,
    SIN                 VARCHAR(15)                 NULL,
    type                ENUM('Guest','Employee')    NOT NULL,
    FOREIGN KEY (SIN) REFERENCES Person(SIN),
    FOREIGN KEY (type) REFERENCES Person(type),
    FOREIGN KEY (booking_id) REFERENCES RoomOccupation(booking_id)
);


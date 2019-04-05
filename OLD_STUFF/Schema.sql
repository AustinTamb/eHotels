CREATE TABLE IF NOT EXISTS PhoneNumber(
    phone_number_id     INT             PRIMARY KEY,
    phone_number1       VARCHAR(10)     NOT NULL,
    phone_number2       VARCHAR(10)     NULL,
    phone_number3       VARCHAR(10)     NULL
);

CREATE TABLE IF NOT EXISTS Addr(
    addr_id             INT             PRIMARY KEY,
    zip                 VARCHAR(6)      NOT NULL,
    city                TEXT            NOT NULL,
    street              TEXT            NOT NULL,
    street_number       INT             NOT NULL,
    state               TEXT            NOT NULL
);

CREATE TABLE IF NOT EXISTS User(
    username        TEXT        PRIMARY KEY,
    pass            TEXT        NOT NULL,
    info            VARCHAR(9)  NOT NULL UNIQUE,
    priv            INT         NOT NULL,

    FOREIGN KEY(info) REFERENCES Person(id)
);

CREATE TABLE IF NOT EXISTS Person(
    id              VARCHAR(9)  PRIMARY KEY,
    addr_id         INT         NOT NULL,
    phone_id        INT         NOT NULL,
    first_name      TEXT        NOT NULL,
    middle_name     TEXT        NULL,
    last_name       TEXT        NOT NULL,

    FOREIGN KEY(addr_id) REFERENCES Addr(addr_id),
    FOREIGN KEY(phone_id) REFERENCES PhoneNumber(phone_number_id)
);


CREATE TABLE IF NOT EXISTS Customer(
    customer_id     INT         PRIMARY KEY,
    info            VARCHAR(9)  NOT NULL UNIQUE,

    FOREIGN KEY(info) REFERENCES Person(id)
);

CREATE TABLE IF NOT EXISTS Employee(
    employee_id     INT         PRIMARY KEY,
    info            VARCHAR(9)  NOT NULL UNIQUE,
    position        TEXT        NOT NULL,

    FOREIGN KEY(info) REFERENCES Person(id)
);

CREATE TABLE IF NOT EXISTS HotelChain(
    chain_id        INT     PRIMARY KEY,
    phone_id        INT     NOT NULL,
    hq_addr         INT     NOT NULL,
    chain_name      TEXT    NOT NULL,
    hotels_amt      INT     NOT NULL, 
    email           TEXT    NOT NULL,
    rating          INT     CHECK( rating IN (1, 2, 3, 4, 5) ) NOT NULL,

    FOREIGN KEY(phone_id) REFERENCES PhoneNumber(phone_number_id),
    FOREIGN KEY(hq_addr)    REFERENCES Addr(addr_id)
);

CREATE TABLE IF NOT EXISTS Hotel(
    hotel_id        INT     PRIMARY KEY,
    phone_id        INT     NOT NULL,
    addr_id         INT     NOT NULL,
    rooms_amt       INT     NOT NULL,
    rating          INT     CHECK( rating IN (1, 2, 3, 4, 5) ) NOT NULL,
    email           TEXT    NOT NULL,
    manager         VARCHAR(9) NOT NULL,

    FOREIGN KEY(phone_id) REFERENCES PhoneNumber(phone_number_id),
    FOREIGN KEY(addr_id) REFERENCES Addr(addr_id),
    FOREIGN KEY(manager) REFERENCES Employee(id)
);

CREATE TABLE IF NOT EXISTS Room(
    room_id         INT     PRIMARY KEY,
    hotel_id        INT     NOT NULL,
    capacity        INT     NOT NULL,
    price           REAL    NOT NULL,
    condition       TEXT    NOT NULL,
    view            TEXT    NOT NULL,
    amenities       TEXT    NOT NULL,
    extendable      INT     CHECK( extendable IN (0, 1) ) NOT NULL DEFAULT 0,       --bool

    FOREIGN KEY(hotel_id) REFERENCES Hotel(hotel_id)
);


CREATE TABLE IF NOT EXISTS RoomOccupation(
    booking_id      INT     PRIMARY KEY,
    customer_id     INT     NOT NULL,
    room_id         INT     NOT NULL,
    checked_in      INT     NOT NULL,       -- bool
    from_date       DATE    NOT NULL,
    to_date         DATE    NOT NULL,

    FOREIGN KEY(room_id) REFERENCES Room(room_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
);
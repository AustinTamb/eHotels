CREATE VIEW [ROOMS IN CITY] AS
    SELECT COUNT(Room) FROM Room, Hotel, Addr
    WHERE Room.hotel_id = Hotel.id AND Hotel.address = Addr.id
        AND Addr.city = {"city"};


CREATE VIEW [ROOM CAPACITY AT HOTEL] AS
    SELECT Room.capacity FROM Room
    WHERE Room.hotel_id = "{hotel_id}";
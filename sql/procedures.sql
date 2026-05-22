DROP PROCEDURE IF EXISTS create_booking;
-- PROC_END

CREATE PROCEDURE create_booking(IN p_user_id INT, IN p_showtime_id INT, IN p_seats_json JSON)
BEGIN
    DECLARE v_booking_id INT;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_len INT DEFAULT 0;
    DECLARE v_seat_id INT;
    DECLARE v_price DECIMAL(10,2);

    SELECT pret_baza INTO v_price FROM showtimes WHERE id = p_showtime_id LIMIT 1;

    INSERT INTO bookings(user_id, showtime_id) VALUES (p_user_id, p_showtime_id);
    SET v_booking_id = LAST_INSERT_ID();

    SET v_len = JSON_LENGTH(p_seats_json);

    WHILE v_i < v_len DO
        SET v_seat_id = JSON_EXTRACT(p_seats_json, CONCAT('$[', v_i, ']'));

        INSERT INTO tickets(booking_id, seat_id, pret_final)
        VALUES (v_booking_id, v_seat_id, v_price);

        SET v_i = v_i + 1;
    END WHILE;

    SELECT v_booking_id AS booking_id;
END
-- PROC_END
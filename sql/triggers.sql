DROP TRIGGER IF EXISTS trg_tickets_before_insert;
-- TRIGGER_END

CREATE TRIGGER trg_tickets_before_insert
BEFORE INSERT ON tickets
FOR EACH ROW
BEGIN
    IF NEW.pret_final <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Eroare: Pretul biletului trebuie sa fie mai mare decat 0';
    END IF;
END;
-- TRIGGER_END

DROP TRIGGER IF EXISTS trg_movies_after_update;
-- TRIGGER_END

CREATE TRIGGER trg_movies_after_update
AFTER UPDATE ON movies
FOR EACH ROW
BEGIN
    INSERT INTO users_log (user_id, action)
    VALUES (1, CONCAT('UPDATE MOVIE: ', OLD.titlu));
END;
-- TRIGGER_END

DROP TRIGGER IF EXISTS trg_check_hall_capacity;
-- TRIGGER_END

CREATE TRIGGER trg_check_hall_capacity
BEFORE INSERT ON bookings
FOR EACH ROW
BEGIN
    DECLARE locuri_ocupate INT;
    DECLARE capacitate_maxima INT;

    SELECT COUNT(*) INTO locuri_ocupate
    FROM bookings
    WHERE showtime_id = NEW.showtime_id;

    SELECT h.capacitate INTO capacitate_maxima
    FROM halls h
    JOIN showtimes s ON h.id = s.hall_id
    WHERE s.id = NEW.showtime_id;

    IF locuri_ocupate >= capacitate_maxima THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Eroare: Sala este deja plina pentru aceasta proiectie!';
    END IF;
END;
-- TRIGGER_END
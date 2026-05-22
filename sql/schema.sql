CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    parola VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titlu VARCHAR(50) NOT NULL,
    gen VARCHAR(50) NOT NULL,
    raiting VARCHAR(10) NOT NULL,
    durata INT NOT NULL
);

CREATE TABLE IF NOT EXISTS halls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nume_sala VARCHAR(50) NOT NULL,
    capacitate INT NOT NULL
);

CREATE TABLE IF NOT EXISTS seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hall_id INT NOT NULL,
    rand INT NOT NULL,
    numar INT NOT NULL,
    CONSTRAINT fk_seats_halls FOREIGN KEY (hall_id)
        REFERENCES halls(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS showtimes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    hall_id INT NOT NULL,
    data_ora DATETIME NOT NULL,
    pret_baza DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_showtimes_movies FOREIGN KEY (movie_id)
        REFERENCES movies(id) ON DELETE CASCADE,
    CONSTRAINT fk_showtimes_halls FOREIGN KEY (hall_id)
        REFERENCES halls(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    data_rezervare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bookings_users FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_bookings_showtimes FOREIGN KEY (showtime_id)
        REFERENCES showtimes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    pret_final DECIMAL(10, 2),
    CONSTRAINT fk_tickets_bookings FOREIGN KEY (booking_id)
        REFERENCES bookings(id) ON DELETE CASCADE,
    CONSTRAINT fk_tickets_seats FOREIGN KEY (seat_id)
        REFERENCES seats(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
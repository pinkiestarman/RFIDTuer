-- Initialize the database.

DROP TABLE IF EXISTS logs;

DROP TABLE IF EXISTS gruppe_recht;

DROP TABLE IF EXISTS user_gruppe;

DROP TABLE IF EXISTS user_recht;

DROP TABLE IF EXISTS gruppe;

DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS recht;

DROP TABLE IF EXISTS location;

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `user`

--

CREATE TABLE `user` (
    id INT NOT NULL AUTO_INCREMENT,
    `name` TEXT(70) NOT NULL,
    `transponder_id` BIGINT UNIQUE,
    `passwort_hash` TEXT NOT NULL,
    `admin_flag` BOOLEAN DEFAULT 0,
    `management_code` INT DEFAULT 0,
    PRIMARY KEY(id)
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `location`

--

CREATE TABLE `location` (
    id INT NOT NULL AUTO_INCREMENT,
    `parent_id` INT,
    `name` TEXT,
    `client_id` INT,
    PRIMARY KEY(id),
    FOREIGN KEY (parent_id) REFERENCES location(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `recht`

--

CREATE TABLE `recht` (
    id INT NOT NULL AUTO_INCREMENT,
    `zeit_von` time,
    `zeit_bis` time,
    `objekt_id` INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (objekt_id) REFERENCES location(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `gruppe`

--

CREATE TABLE `gruppe` (
    id INT NOT NULL AUTO_INCREMENT,
    `name` TEXT(70),
    `user_id` INT,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `gruppe_recht`

--

CREATE TABLE `gruppe_recht` (
    id INT NOT NULL AUTO_INCREMENT,
    `gruppe_id` INT NOT NULL,
    `recht_id` INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (gruppe_id) REFERENCES gruppe(id) ON DELETE CASCADE,
    FOREIGN KEY (recht_id) REFERENCES recht(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `logs`

--

CREATE TABLE `logs` (
    id INT NOT NULL AUTO_INCREMENT,
    `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `user_id` INT NOT NULL,
    `objekt_id` INT NOT NULL,
    `description` TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (objekt_id) REFERENCES location(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `User_Gruppe`

--

CREATE TABLE `user_gruppe` (
    id INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `gruppe_id` INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (gruppe_id) REFERENCES gruppe(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- --------------------------------------------------------

--

-- Tabellenstruktur für Tabelle `User_Recht`

--

CREATE TABLE `user_recht` (
    id INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `recht_id` INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (recht_id) REFERENCES recht(id) ON DELETE CASCADE
);

-- User ------------------------------------------

--Admin

DROP USER IF EXISTS 'admin' @'%';

FLUSH PRIVILEGES;

CREATE USER 'admin'@'%' IDENTIFIED BY 'admin';

GRANT ALL PRIVILEGES ON RFID.* TO 'admin'@'%';

--Türen

DROP USER IF EXISTS 'door'@'%';

FLUSH PRIVILEGES;

CREATE USER 'door'@'%' IDENTIFIED BY 'key';

GRANT SELECT ON RFID.* TO 'door'@'%';

GRANT INSERT ON RFID.logs TO 'door'@'%';

GRANT INSERT ON RFID.user TO 'door'@'%';

GRANT INSERT ON RFID.gruppe TO 'door'@'%';

GRANT INSERT ON RFID.user_gruppe TO 'door'@'%';

GRANT INSERT ON RFID.recht TO 'door'@'%';

GRANT INSERT ON RFID.gruppe_recht TO 'door'@'%';

--Verwalter

DROP USER IF EXISTS 'verwalter' @'%';

CREATE USER 'verwalter'@'%' IDENTIFIED BY '123';

FLUSH PRIVILEGES;

GRANT SELECT, INSERT, UPDATE ON RFID.* TO 'verwalter' @'%';

FLUSH PRIVILEGES;

-- Some Testdata ---------------------------------

-- User ----------------------

INSERT INTO
    user (name, passwort_hash, admin_flag)
VALUES
    (
        'admin',
        'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',
        1
    );

INSERT INTO
    user(name, passwort_hash, admin_flag, transponder_id)
VALUES
    (
        'Doorian (Chip Standard User)',
        'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',
        0,
        882784646626
    );

INSERT INTO
    user(
        name,
        passwort_hash,
        admin_flag,
        transponder_id,
        management_code
    )
VALUES
    (
        'CREATE NEW USER (Card)',
        'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',
        0,
        1050655679228,
        1
    );

INSERT INTO
    user(
        name,
        passwort_hash,
        admin_flag,
        transponder_id,
        management_code
    )
VALUES
    (
        'CREATE NEW RIGHT (Card)',
        'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',
        0,
        706167923279,
        2
    );

-- gruppe ----------------------

INSERT INTO gruppe (name) VALUES ('Lehrer');

INSERT INTO gruppe (name, user_id) VALUES ('admin',1);

INSERT INTO
    gruppe (name, user_id)
VALUES
    ('Doorian (Chip Standard User)', 2);

INSERT INTO
    gruppe (name, user_id)
VALUES
    ('CREATE NEW USER (Card)', 3);

INSERT INTO
    gruppe (name, user_id)
VALUES
    ('CREATE NEW RIGHT (Card)', 4);

-- location ----------------------

INSERT INTO location (id, Name) VALUES (5, 'Schulgebäude ID 5');

INSERT INTO
    location (id, Name, parent_id)
VALUES
    (1, 'Lehrerzimmer ID 1', 5);

INSERT INTO
    location (id, name, parent_id, client_id)
VALUES
    (2, 'Tür ID 2', 1, 1);

INSERT INTO
    location (id, name, parent_id)
VALUES
    (3, 'Küche ID 3', 5);

INSERT INTO
    location (id, name, parent_id, client_id)
VALUES
    (4, 'Tür ID 4', 3, 2);

-- user_gruppe ----------------------

INSERT INTO user_gruppe (gruppe_id, user_id) VALUES (1,2);

INSERT INTO user_gruppe (gruppe_id, user_id) VALUES (2,1);

INSERT INTO user_gruppe (gruppe_id, user_id) VALUES (3,2);

INSERT INTO user_gruppe (gruppe_id, user_id) VALUES (4,3);

INSERT INTO user_gruppe (gruppe_id, user_id) VALUES (5,4);

-- recht ----------------------

INSERT INTO recht (objekt_id) VALUES (2);

INSERT INTO recht (objekt_id) VALUES (5);

-- gruppe_recht ----------------------

INSERT INTO gruppe_recht (gruppe_id, recht_id) VALUES (1,1);

INSERT INTO gruppe_recht (gruppe_id, recht_id) VALUES (2,2);

-- logs ----------------------

INSERT INTO
    logs (user_id, objekt_id, description)
VALUES
    (
        2,
        1,
        'Doorian schreitete heroisch durch die Tür'
    );
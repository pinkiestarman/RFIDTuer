--Admin

CREATE USER 'admin'@'@' IDENTIFIED BY 'admin';

GRANT ALL PRIVILEGES ON RFID.* TO 'admin'@'@';

--Türen

GRANT SELECT ON RFID.* TO 'door'@'@' IDENTIFIED BY 'key';

GRANT INSERT ON RFID.logs TO 'door'@'@' IDENTIFIED BY 'key';

--

GRANT
SELECT,
INSERT
    ON RFID.* TO 'Verwalter' @'@' IDENTIFIED BY '123';
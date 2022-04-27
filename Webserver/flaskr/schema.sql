-- Initialize the database.
-- Drop any existing data and create empty tables.
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Gruppe;
DROP TABLE IF EXISTS Gruppe_Recht;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Logs;
DROP TABLE IF EXISTS Recht;
DROP TABLE IF EXISTS User_Gruppe;
DROP TABLE IF EXISTS User_Recht;
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Gruppe`
--
CREATE TABLE `Gruppe` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Name` TEXT NOT NULL UNIQUE
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Gruppe_Recht`
--
CREATE TABLE `Gruppe_Recht` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Gruppe_ID` INTEGER NOT NULL,
  `Recht_ID` INTEGER NOT NULL
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Location`
--
CREATE TABLE `Location` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Parent_ID` INTEGER NOT NULL,
  `Name` TEXT NOT NULL
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Logs`
--
CREATE TABLE `Logs` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `User_ID` INTEGER NOT NULL,
  `Objekt_ID` INTEGER NOT NULL,
  `Description` TEXT NOT NULL
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `Recht`
--
CREATE TABLE `Recht` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Zeit_von` time NOT NULL,
  `Zeit_bis` time NOT NULL,
  `Objekt_ID` INTEGER NOT NULL
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `User`
--
CREATE TABLE `User` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `Name` TEXT UNIQUE NOT NULL,
  `TransponderID` INTEGER,
  `Passwort_hash` TEXT NOT NULL,
  `AdminFlag` BOOLEAN DEFAULT 0
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `User_Gruppe`
--
CREATE TABLE `User_Gruppe` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `User_ID` INTEGER NOT NULL,
  `Gruppe_ID` INTEGER NOT NULL
);
-- --------------------------------------------------------
--
-- Tabellenstruktur für Tabelle `User_Recht`
--
CREATE TABLE `User_Recht` (
  `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
  `User_ID` INTEGER NOT NULL,
  `Recht_ID` INTEGER NOT NULL
);
INSERT INTO
  user (Name, Passwort_hash, AdminFlag)
VALUES
  (
    'admin',
    'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254',
    1
  );
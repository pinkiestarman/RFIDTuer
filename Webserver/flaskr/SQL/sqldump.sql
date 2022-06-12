-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Erstellungszeit: 20. Apr 2022 um 11:29
-- Server-Version: 5.7.32
-- PHP-Version: 7.4.12
SET
  SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET
  time_zone = "+00:00";
--
  -- Datenbank: `RFID`
  --
  -- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `Gruppe`
  --
  CREATE TABLE `Gruppe` (
    `ID` int(11) NOT NULL,
    `Name` varchar(45) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `Gruppe_Recht`
  --
  CREATE TABLE `Gruppe_Recht` (
    `ID` int(11) NOT NULL,
    `Gruppe_ID` int(11) NOT NULL,
    `Recht_ID` int(11) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `Location`
  --
  CREATE TABLE `Location` (
    `ID` int(11) NOT NULL,
    `Parent_ID` int(11) NOT NULL,
    `Name` varchar(45) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `Logs`
  --
  CREATE TABLE `Logs` (
    `ID` int(11) NOT NULL,
    `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `User_ID` int(11) NOT NULL,
    `Objekt_ID` int(11) NOT NULL,
    `Description` varchar(70) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `Recht`
  --
  CREATE TABLE `Recht` (
    `ID` int(11) NOT NULL,
    `Zeit_von` time NOT NULL,
    `Zeit_bis` time NOT NULL,
    `Objekt_ID` int(11) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `User`
  --
  CREATE TABLE `User` (
    `ID` int(11) NOT NULL,
    `Name` varchar(45) NOT NULL,
    `TransponderID` int(11) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `User_Gruppe`
  --
  CREATE TABLE `User_Gruppe` (
    `ID` int(11) NOT NULL,
    `User_ID` int(11) NOT NULL,
    `Gruppe_ID` int(11) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
-- --------------------------------------------------------
  --
  -- Tabellenstruktur für Tabelle `User_Recht`
  --
  CREATE TABLE `User_Recht` (
    `ID` int(11) NOT NULL,
    `User_ID` int(11) NOT NULL,
    `Recht_ID` int(11) NOT NULL
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
--
  -- Indizes der exportierten Tabellen
  --
  --
  -- Indizes für die Tabelle `Gruppe`
  --
ALTER TABLE
  `Gruppe`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `Gruppe_Recht`
  --
ALTER TABLE
  `Gruppe_Recht`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `Location`
  --
ALTER TABLE
  `Location`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `Logs`
  --
ALTER TABLE
  `Logs`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `Recht`
  --
ALTER TABLE
  `Recht`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `User`
  --
ALTER TABLE
  `User`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `User_Gruppe`
  --
ALTER TABLE
  `User_Gruppe`
ADD
  PRIMARY KEY (`ID`);
--
  -- Indizes für die Tabelle `User_Recht`
  --
ALTER TABLE
  `User_Recht`
ADD
  PRIMARY KEY (`ID`);
--
  -- AUTO_INCREMENT für exportierte Tabellen
  --
  --
  -- AUTO_INCREMENT für Tabelle `Gruppe`
  --
ALTER TABLE
  `Gruppe`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `Gruppe_Recht`
  --
ALTER TABLE
  `Gruppe_Recht`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `Location`
  --
ALTER TABLE
  `Location`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `Logs`
  --
ALTER TABLE
  `Logs`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `Recht`
  --
ALTER TABLE
  `Recht`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `User`
  --
ALTER TABLE
  `User`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `User_Gruppe`
  --
ALTER TABLE
  `User_Gruppe`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
--
  -- AUTO_INCREMENT für Tabelle `User_Recht`
  --
ALTER TABLE
  `User_Recht`
MODIFY
  `ID` int(11) NOT NULL AUTO_INCREMENT;
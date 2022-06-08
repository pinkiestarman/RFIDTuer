# imports
import sys
import threading
import time
import traceback
from distutils.util import execute
from numbers import Integral
from datetime import datetime

import mariadb
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from typing_extensions import Self

ClientID = 1


class LED():

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        # set GPIO PIN states
        self.gpio11 = False
        self.gpio13 = False
        self.gpio15 = False
        self.off()
        self.__blinkin = False
        self.__blinkinDelay = 1
        self.thread = threading.Thread(
            name='blinkinLED', target=self.__threadLED, daemon=True)
        self.thread.start()

    def blinkin(self, func=lambda: None, blinkinDelay=1):
        func()
        self.__blinkinDelay = blinkinDelay
        self.__blinkin = True

    def noColor(self):
        self.gpio11 = False
        self.gpio13 = False
        self.gpio15 = False
        self.__blinkin = False

    def yellow(self):
        self.gpio11 = True
        self.gpio13 = True
        self.gpio15 = False
        self.__blinkin = False

    def red(self):
        self.gpio11 = True
        self.gpio13 = False
        self.gpio15 = False
        self.__blinkin = False

    def blue(self):
        self.gpio11 = False
        self.gpio13 = False
        self.gpio15 = True
        self.__blinkin = False

    def green(self):
        self.gpio11 = False
        self.gpio13 = True
        self.gpio15 = False
        self.__blinkin = False

    def off(self):
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)

    def __setGPIOpins(self):
        if(self.gpio11):
            GPIO.output(11, GPIO.HIGH)
        else:
            GPIO.output(11, GPIO.LOW)
        if(self.gpio13):
            GPIO.output(13, GPIO.HIGH)
        else:
            GPIO.output(13, GPIO.LOW)
        if(self.gpio15):
            GPIO.output(15, GPIO.HIGH)
        else:
            GPIO.output(15, GPIO.LOW)

# Für schnellere Reaktion der LED sollte man die vergangene Zeit speichern und nicht solange sleepen Zzz...
    def __threadLED(self):
        while(True):
            self.__setGPIOpins()
            time.sleep(self.__blinkinDelay)
            if(self.__blinkin):
                self.off()
                time.sleep(self.__blinkinDelay)


class db():
    def __init__(self):
        pass

    def connect(self):
        try:
            self.conn.ping()
            return 0
        except:
            try:
                self.conn = mariadb.connect(
                    user="door",
                    password="key",
                    host="127.0.0.1",
                    port=3306,
                    database="RFID"
                )
                return 0
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                return 1

    def cursor_to_dict_array(self, cur):
        res = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row)) for row in cur.fetchall()]
        return res

    def check_acces_right(self, id):
        cur = self.conn.cursor()
        cur.execute('WITH RECURSIVE location_hierarchy AS (SELECT name, id, parent_id FROM location WHERE location.client_id=? UNION ALL SELECT location.name, location.id, location.parent_id FROM location, location_hierarchy WHERE location.id=location_hierarchy.parent_id) SELECT user.transponder_id FROM location_hierarchy INNER JOIN recht ON location_hierarchy.id=recht.objekt_id INNER JOIN gruppe_recht ON recht.id=gruppe_recht.recht_id INNER JOIN gruppe ON gruppe_recht.gruppe_id=gruppe.id INNER JOIN user_gruppe ON gruppe.id=user_gruppe.gruppe_id INNER JOIN user ON user_gruppe.user_id=user.id WHERE user.transponder_id=?', (ClientID, id,))
        rows = cur.fetchall()
        result = cur.rowcount > 0
        cur.close()
        return result

    def check_special_flag(self, id):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT user.management_code FROM user WHERE user.transponder_id=?', (id,))
        rows = cur.fetchall()
        if(cur.rowcount > 0):
            return rows[0][0]
        else:
            return None

    def create_user(self, id):
        cur = self.conn.cursor()
        username = f'Create at Client {ClientID}'
        cur.execute(
            'INSERT INTO user(name, passwort_hash, admin_flag, transponder_id) VALUES (?,?,?,?)', (username, 'pbkdf2:sha256:260000$ClAB2AQV4Jzr8zv8$61cd04ff86bb8a46a7e1fc5caa40ab5be15aca8407227693f50c730cd87c1254', 0, id))
        user = self.get_user(id)
        user_id = user[0]['id']
        cur.execute(
            'INSERT INTO gruppe(name) VALUES (?)', (username,))
        gruppe = self.get_gruppe(user[0]['name'])
        gruppe_id = gruppe[0]['id']
        cur.execute(
            'INSERT INTO user_gruppe(user_id, gruppe_id) VALUES (?,?)', (
                user_id, gruppe_id,)
        )
        
        self.conn.commit()
        cur.close()
        return 0

    def create_right(self, id):
        cur = self.conn.cursor()
        user = self.get_user(id)
        gruppe = self.get_gruppe(user[0]['name'])
        cur.execute(
            'INSERT INTO recht(objekt_id) SELECT location.id from location WHERE location.client_id=?', (ClientID,)
        )
        cur.execute('INSERT INTO gruppe_recht (recht_id, gruppe_id) VALUES (?,?)',
                    (cur.lastrowid, gruppe[0]['id']))
        self.conn.commit()
        return 0

    def get_user(self, id: Integral):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT * FROM user WHERE user.transponder_id=?', (id,))
        return self.cursor_to_dict_array(cur)

    def get_gruppe(self, name: str):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM gruppe WHERE gruppe.name=?', (name,))
        return self.cursor_to_dict_array(cur)

    def write_log(self, user: int, objekt: int, description: str) -> None:
        now = datetime.now()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO logs (timestamp, user_id, objekt_id, description) VALUES (?,?,?, ?)",
            now, user, objekt, description
        )


def main():
    led = LED()
    led.blue()
    reader = SimpleMFRC522()
    database = db()

    while(True):
        # Init
        acces_granted = False
        try:
            print('Check connection to database...')
            if(database.connect() != 0):
                print('Database connection failed, retry in 10 sec')
                led.blinkin(led.red)
                time.sleep(10)
            else:
                print('Database connection established!')
            # Read RFID Chip
            id, text = reader.read()

            # Check special flags
            flag = database.check_special_flag(id)
            print(f'Management Code: {flag}')
            if(flag is not None):
                if(flag == 1):  # Add User
                    led.blinkin(led.yellow, blinkinDelay=0.2)
                    print('Adding new user...')
                    time.sleep(1)
                    id, text = reader.read()
                    user = database.get_user(id)

                    if(len(user) > 0):
                        led.red()
                        print(f'Transponder id: {id} already in use!')
                    else:
                        if(database.create_user(id) == 0):
                            led.green()
                            print(f'Succesfully created new user! id: {id}')
                        else:
                            led.red()
                            print(f'Error while creating user! id: {id}')
                elif(flag == 2):  # Give acces
                    led.blinkin(led.blue, blinkinDelay=0.2)
                    print('Adding new access right...')
                    time.sleep(1)
                    id, text = reader.read()
                    if(database.check_acces_right(id)):
                        led.green()
                        print('Transponder id: {id} has already access!')
                    else:
                        user = database.get_user(id)
                        if(len(user) > 0):
                            database.create_right(id)
                            led.green()
                            print('Succesfully added access right to user!')
                        else:  # User existiert nicht
                            led.red()
                            print(f'No user found for id: {id}')

                else:
                    # Check Access
                    if(database.check_acces_right(id)):
                        print('Acces Granted!')
                        led.blinkin(led.green, blinkinDelay=0.2)
                        write_log()
                    else:
                        print('Acces Denied!')
                        led.red()
            else:
                print('Data spaghetti')
        except mariadb.Error as err:
            print(f'Datenbank fehler: {err}')
            led.blinkin(led.red)
        except BaseException as err:
            led.blinkin(led.red)
            print(f'Error? {err}')
        finally:
            time.sleep(3)
            led.blue()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

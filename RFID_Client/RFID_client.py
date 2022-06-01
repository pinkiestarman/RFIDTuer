# imports
import sys
import time
import threading
import traceback
import RPi.GPIO as GPIO
import mariadb
from mfrc522 import SimpleMFRC522

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
                    host="10.130.0.41",
                    port=3306,
                    database="RFID"
                )
                return 0
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                return 1

    def check_acces_right(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute('WITH RECURSIVE location_hierarchy AS (SELECT name, id, parent_id FROM location WHERE location.client_id=? UNION ALL SELECT location.name, location.id, location.parent_id FROM location, location_hierarchy WHERE location.id=location_hierarchy.parent_id) SELECT user.transponder_id FROM location_hierarchy INNER JOIN recht ON location_hierarchy.id=recht.objekt_id INNER JOIN gruppe_recht ON recht.id=gruppe_recht.recht_id INNER JOIN gruppe ON gruppe_recht.gruppe_id=gruppe.id INNER JOIN user_gruppe ON gruppe.id=user_gruppe.gruppe_id INNER JOIN user ON user_gruppe.user_id=user.id WHERE user.transponder_id=?', (ClientID, id,))
            rows = cur.fetchall()
            result = cur.rowcount > 0
            cur.close()
            return result
        except:
            return False

    def check_special_flag(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute(
                'SELECT user.admin_flag FROM user WHERE user.transponder_id=?', (id,))
            rows = cur.fetchall()
            if(cur.rowcount > 0):
                return rows[0][0]
            else:
                return None
        except:
            return None


def main():
    led = LED()
    led.blue()
    reader = SimpleMFRC522()
    database = db()

    while(True):
        # Init
        acces_granted = False
        id, text = reader.read()
        try:
            print('Check connection to database...')
            if(database.connect() != 0):
                print('Database connection failed, retry in 10 sec')
                led.blinkin(led.red())
                time.sleep(10)
            else:
                print('Database connection established!')
            # Read RFID Chip
            id, text = reader.read()

            # Check special flags
            flag = database.check_special_flag(id)

            if(flag is not None):
                if(flag == 1):
                    led.yellow()
                else:
                    # Check Access
                    if(acces_granted != True):
                        acces_granted = database.check_acces_right(id)

                    if (acces_granted):
                        print('Acces Granted!')
                        led.green()
                    else:
                        print('Acces Denied!')
                        led.red()
            else:
                print('Data spaghetti')
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

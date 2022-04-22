from time import sleep
#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522pi
import mysql

shutdown_id = 0xFFFFFFFFFFFFFFFF
sql_user = ""
sql_pw = ""
sql_host = ""


def init():
    # Sql Connection


def check_acces():
    pass


def read_loop():
    reader = SimpleMFRC522()
    current_id = 0
    while(current_id != shutdown_id):
        try:
            current_id, text = reader.read()
        finally:
            if(current_id != 0):
                check_acces(current_id)
        current_id = 1  # Temporary breakout


if __name__ == "__main__":
    print("END")

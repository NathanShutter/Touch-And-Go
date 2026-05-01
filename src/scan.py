"""
src/scan.py
Touch & Go — Attendance Scanning

Runs continuously on the Raspberry Pi. When a student places their finger
on the sensor, the system identifies them and logs a timestamped attendance
record to the MySQL database. Press Ctrl+C to stop.

Hardware:
  - Adafruit AS608 fingerprint sensor via USB UART (/dev/ttyUSB0)
  - 20x4 I2C LCD display at address 0x27
"""

import sys
import time
import serial
from datetime import datetime

import adafruit_fingerprint
import mysql.connector

sys.path.append("lib")
from i2c_lcd import I2cLcd

from db.config import get_connection

# --- LCD setup ---
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# --- Fingerprint sensor setup ---
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def log_attendance(finger_id: int) -> None:
    """Look up the student by finger_id and insert an attendance record."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT userID FROM student WHERE fingerId = %s", (finger_id,)
        )
        result = cursor.fetchone()
        if result is None:
            print(f"No student found for finger ID {finger_id}.")
            lcd.clear()
            lcd.putstr("Unknown finger ID")
            return

        user_id = result[0]
        cursor.execute(
            "INSERT INTO fingerprint (userID, timestamp) VALUES (%s, %s)",
            (user_id, datetime.now()),
        )
        connection.commit()
        print(f"Attendance logged for userID {user_id}.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()


def scan_fingerprint() -> int | None:
    """
    Wait for a fingerprint, match it against stored templates, and return
    the matched finger_id, or None if no match is found.
    """
    lcd.clear()
    lcd.putstr("Place finger on")
    lcd.move_to(0, 1)
    lcd.putstr("sensor...")
    print("Waiting for fingerprint scan...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return None

    if finger.finger_search() == adafruit_fingerprint.OK:
        lcd.clear()
        lcd.putstr("Fingerprint found")
        print(f"Fingerprint found: ID #{finger.finger_id}")
        return finger.finger_id

    lcd.clear()
    lcd.putstr("Not recognized")
    print("No matching fingerprint found.")
    return None


def main() -> None:
    print("Touch & Go — Attendance Scanner running. Press Ctrl+C to stop.")
    try:
        while True:
            finger_id = scan_fingerprint()
            if finger_id is not None:
                log_attendance(finger_id)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nScanner stopped.")
        lcd.clear()


if __name__ == "__main__":
    main()

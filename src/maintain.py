"""
src/maintain.py
Touch & Go — Admin Fingerprint Management

Interactive menu for enrolling, deleting, and resetting fingerprint
templates stored on the AS608 sensor. Enrollment also links the sensor
template slot to a student record in the database.

Hardware:
  - Adafruit AS608 fingerprint sensor via USB UART (/dev/ttyUSB0)
  - 20x4 I2C LCD display at address 0x27
"""

import sys
import time
import serial

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


def link_finger_to_student(finger_slot: int) -> None:
    """Update the student record to associate a finger slot ID with their name."""
    first_name = input("Enter student first name: ").strip()
    last_name = input("Enter student last name: ").strip()
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE student SET fingerId = %s WHERE firstName = %s AND lastName = %s",
            (finger_slot, first_name, last_name),
        )
        connection.commit()
        if cursor.rowcount == 0:
            print(f"No student found with name '{first_name} {last_name}'.")
        else:
            print(f"Linked finger slot {finger_slot} to {first_name} {last_name}.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if "connection" in locals() and connection.is_connected():
            connection.close()


def get_num(max_number: int) -> int:
    """Prompt for a valid slot ID in range [0, max_number)."""
    i = -1
    while not (0 <= i < max_number):
        try:
            i = int(input(f"Enter ID # from 0–{max_number - 1}: "))
        except ValueError:
            pass
    return i


def enroll_finger(location: int) -> bool:
    """
    Capture two fingerprint images, create a template, store it at `location`
    on the sensor, and link it to a student in the database.
    """
    lcd.clear()
    for scan_num in range(1, 3):
        prompt = "Place finger on sensor..." if scan_num == 1 else "Place same finger again..."
        lcd_line2 = "sensor..." if scan_num == 1 else "again..."
        lcd.clear()
        lcd.putstr("Place finger on" if scan_num == 1 else "Place same finger")
        lcd.move_to(0, 1)
        lcd.putstr(lcd_line2)
        print(prompt, end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(scan_num)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            errors = {
                adafruit_fingerprint.IMAGEMESS: "Image too messy",
                adafruit_fingerprint.FEATUREFAIL: "Could not identify features",
                adafruit_fingerprint.INVALIDIMAGE: "Image invalid",
            }
            print(errors.get(i, "Other error"))
            return False

        if scan_num == 1:
            lcd.clear()
            lcd.putstr("Remove finger")
            print("Remove finger")
            time.sleep(1)
            while finger.get_image() != adafruit_fingerprint.NOFINGER:
                pass

    print("Creating model...", end="")
    i = finger.create_model()
    if i != adafruit_fingerprint.OK:
        print("Prints did not match" if i == adafruit_fingerprint.ENROLLMISMATCH else "Other error")
        return False
    print("Created")

    print(f"Storing model #{location}...", end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        lcd.clear()
        lcd.putstr("Stored!")
        print("Stored")
        link_finger_to_student(location)
        time.sleep(2)
        lcd.clear()
        return True
    else:
        errors = {
            adafruit_fingerprint.BADLOCATION: "Bad storage location",
            adafruit_fingerprint.FLASHERR: "Flash storage error",
        }
        print(errors.get(i, "Other error"))
        return False


def main() -> None:
    while True:
        print("\n----------------")
        if finger.read_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to read templates")
        print("Templates stored:", finger.templates)

        if finger.count_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to count templates")
        print("Template count:", finger.template_count)

        if finger.read_sysparam() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to get system parameters")
        print("Library size:", finger.library_size)
        print()
        print("e) Enroll new fingerprint")
        print("d) Delete fingerprint by ID")
        print("r) Reset entire library")
        print("q) Quit")
        print("----------------")
        c = input("> ").strip().lower()

        if c == "e":
            enroll_finger(get_num(finger.library_size))
        elif c == "d":
            slot = get_num(finger.library_size)
            if finger.delete_model(slot) == adafruit_fingerprint.OK:
                print(f"Deleted slot {slot}.")
            else:
                print("Failed to delete.")
        elif c == "r":
            if finger.empty_library() == adafruit_fingerprint.OK:
                print("Library cleared.")
            else:
                print("Failed to clear library.")
        elif c == "q":
            print("Exiting.")
            raise SystemExit


if __name__ == "__main__":
    main()

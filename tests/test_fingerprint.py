"""
tests/test_fingerprint.py
Touch & Go — Fingerprint Sensor Hardware Test

Interactive script for verifying sensor connectivity and testing
enroll/match/delete operations before running the full system.
Run directly on the Raspberry Pi:

    python tests/test_fingerprint.py

This is a standalone diagnostic tool. It does not write to the database.
"""

import sys
import time
import serial

import adafruit_fingerprint

sys.path.append("lib")
from i2c_lcd import I2cLcd

# --- LCD setup ---
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# --- Sensor setup ---
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def get_num(max_number: int) -> int:
    i = -1
    while not (0 <= i < max_number):
        try:
            i = int(input(f"Enter ID # from 0–{max_number - 1}: "))
        except ValueError:
            pass
    return i


def scan_and_match() -> bool:
    """Scan a fingerprint and check if it matches any stored template."""
    lcd.clear()
    lcd.putstr("Place finger on")
    lcd.move_to(0, 1)
    lcd.putstr("sensor...")
    print("Waiting for image...")

    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    if finger.finger_search() == adafruit_fingerprint.OK:
        lcd.clear()
        output = f"ID #{finger.finger_id}"
        lcd.putstr(output)
        lcd.move_to(0, 1)
        lcd.putstr(f"Conf: {finger.confidence}")
        print(f"Found: #{finger.finger_id}  Confidence: {finger.confidence}")
        time.sleep(3)
        lcd.clear()
        return True

    print("No match found.")
    return False


def enroll_finger(location: int) -> bool:
    """Capture two images, create a template, and store at `location`."""
    lcd.clear()
    for scan_num in range(1, 3):
        prompt = "Place finger..." if scan_num == 1 else "Same finger again..."
        lcd.clear()
        lcd.putstr(prompt)
        print(prompt, end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i != adafruit_fingerprint.NOFINGER:
                print("Error during capture")
                return False

        i = finger.image_2_tz(scan_num)
        if i != adafruit_fingerprint.OK:
            print("Templating failed")
            return False

        if scan_num == 1:
            lcd.clear()
            lcd.putstr("Remove finger")
            time.sleep(1)
            while finger.get_image() != adafruit_fingerprint.NOFINGER:
                pass

    if finger.create_model() != adafruit_fingerprint.OK:
        print("Prints did not match")
        return False

    if finger.store_model(location) == adafruit_fingerprint.OK:
        lcd.clear()
        lcd.putstr(f"Stored at #{location}")
        print(f"Stored at slot {location}")
        time.sleep(2)
        lcd.clear()
        return True

    print("Storage failed")
    return False


def save_image(filename: str = "fingerprint.png") -> bool:
    """Capture a fingerprint image and save it as a PNG."""
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    from PIL import Image
    img = Image.new("L", (256, 288), "white")
    pixels = img.load()
    mask = 0b00001111
    data = finger.get_fpdata(sensorbuffer="image")
    x = y = 0
    for byte in data:
        pixels[x, y] = (int(byte) >> 4) * 17
        x += 1
        pixels[x, y] = (int(byte) & mask) * 17
        x = x + 1 if x < 255 else (0, y + 1)[0] or 0
        if x == 0:
            y += 1
    img.save(filename)
    return True


def main() -> None:
    while True:
        print("\n---- Fingerprint Sensor Test ----")
        if finger.read_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Cannot read templates from sensor.")
        print(f"Stored templates : {finger.templates}")
        print(f"Template count   : {finger.template_count}")
        print(f"Library size     : {finger.library_size}")
        print()
        print("e) Enroll fingerprint")
        print("f) Find / match fingerprint")
        print("d) Delete fingerprint")
        print("s) Save fingerprint image")
        print("r) Reset library")
        print("q) Quit")
        print("---------------------------------")
        c = input("> ").strip().lower()

        if c == "e":
            enroll_finger(get_num(finger.library_size))
        elif c == "f":
            scan_and_match()
        elif c == "d":
            slot = get_num(finger.library_size)
            result = finger.delete_model(slot)
            print("Deleted." if result == adafruit_fingerprint.OK else "Failed to delete.")
        elif c == "s":
            if save_image():
                print("Image saved as fingerprint.png")
        elif c == "r":
            result = finger.empty_library()
            print("Library cleared." if result == adafruit_fingerprint.OK else "Failed.")
        elif c == "q":
            print("Exiting.")
            raise SystemExit


if __name__ == "__main__":
    main()

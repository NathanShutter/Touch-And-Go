# Hardware Setup

## Bill of Materials

| Component | Model | Approx. Cost |
|---|---|---|
| Microcontroller | Raspberry Pi 4 | $100.00 |
| Fingerprint Sensor | Adafruit AS608 | $20.00 |
| LCD Display | 20×4 I2C (PCF8574 backpack) | $15.00 |
| UART Adapter | GPIO-to-UART USB Board | $15.00 |
| **Total (hardware only)** | | **~$150.00** |

> See `docs/` for the full budget breakdown including labor estimates.

---

## Wiring

### Fingerprint Sensor → USB UART Adapter

| Sensor Pin | UART Adapter Pin |
|---|---|
| VCC (3.3V) | 3.3V |
| GND | GND |
| TX | RX |
| RX | TX |

The adapter connects to the Raspberry Pi via USB. The OS enumerates it as `/dev/ttyUSB0`.

### LCD → Raspberry Pi (I2C)

| LCD Pin | Raspberry Pi GPIO |
|---|---|
| VCC | 5V (Pin 2) |
| GND | GND (Pin 6) |
| SDA | GPIO 2 / SDA (Pin 3) |
| SCL | GPIO 3 / SCL (Pin 5) |

Default I2C address: `0x27`. Run `i2cdetect -y 1` to verify.

---

## Raspberry Pi Configuration

### Enable I2C

```bash
sudo raspi-config
# Interface Options → I2C → Enable
sudo reboot
```

Verify the LCD is detected:

```bash
sudo apt install i2c-tools
i2cdetect -y 1
```

You should see `27` in the output grid.

### Serial Port

The fingerprint sensor connects over USB serial. Verify the device path:

```bash
ls /dev/ttyUSB*
# Expected: /dev/ttyUSB0
```

If you see a different path (e.g., `/dev/ttyUSB1`), update the `serial.Serial(...)` call in `src/scan.py` and `src/maintain.py`.

---

## Sensor Calibration

The Adafruit AS608 sensor stores up to 127 fingerprint templates in its onboard flash memory. Template slots are numbered 0–126.

During enrollment (`maintain.py`), two images of the same finger are captured, compared, merged into a template, and stored at the specified slot number. The slot number is then written to the `student.fingerId` column in the database to link the template to a specific student.

**Tips for reliable enrollment:**

- Place the finger flat and centered on the sensor window.
- Avoid moving the finger between the two capture prompts.
- Re-enroll in dry conditions — oils or moisture can affect image quality.
- Run `tests/test_fingerprint.py` to test enrollment without affecting the live database.

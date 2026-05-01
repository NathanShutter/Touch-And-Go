# Touch & Go

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberry-pi&logoColor=white)](https://www.raspberrypi.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **CSC354 — Software Engineering | Kutztown University of Pennsylvania**

A biometric attendance system built on Raspberry Pi that uses a fingerprint scanner to automate student check-in. Students place their finger on the sensor; the system identifies them, logs a timestamped attendance record to a cloud MySQL database, and confirms the result on an I2C LCD display.

---

## Table of Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Web UI](#web-ui)
- [Documentation](#documentation)
- [Team](#team)

---

## Overview

Touch & Go was developed as a capstone project for CSC354 at Kutztown University of Pennsylvania. The motivation was to replace manual sign-in sheets with a fast, reliable fingerprint-based system. Each scan takes under 2 seconds and writes directly to a remote MySQL database, giving instructors real-time attendance visibility.

**Core workflow:**

1. Administrator enrolls students via `maintain.py` — captures two fingerprint images, creates a template stored on the sensor, and links the template ID to the student record in the database.
2. During class, `scan.py` runs continuously. When a student places their finger on the sensor, the system matches the print, looks up the student ID, and inserts a timestamped row into the `fingerprint` attendance table.
3. Students can view their attendance history and schedule through the web UI.

---

## Hardware

| Component | Model | Purpose |
|---|---|---|
| Microcontroller | Raspberry Pi 4 | Main compute platform |
| Fingerprint Sensor | Adafruit AS608 | Biometric capture & matching |
| Display | 20×4 I2C LCD (PCF8574) | User feedback |
| Interface | GPIO-to-UART USB Board | Serial communication |

**Wiring:**
- Fingerprint sensor → USB UART adapter → `/dev/ttyUSB0`
- LCD → I2C bus at address `0x27`

---

## System Architecture

```
┌──────────────────────────────────────────────┐
│                 Raspberry Pi                 │
│                                              │
│  ┌──────────┐    ┌──────────┐  ┌──────────┐ │
│  │ scan.py  │    │maintain  │  │  Web UI  │ │
│  │(attend.) │    │  .py     │  │(student) │ │
│  └────┬─────┘    └────┬─────┘  └──────────┘ │
│       │               │                      │
│  ┌────▼───────────────▼──────────────────┐   │
│  │           src/db/config.py            │   │
│  └────────────────────┬──────────────────┘   │
│                       │ MySQL Connector       │
└───────────────────────┼──────────────────────┘
                        │
              ┌─────────▼──────────┐
              │   AWS RDS MySQL    │
              │  touch_and_go_db   │
              └────────────────────┘
```

**Database tables:**
- `student` — `(userID, firstName, lastName, email, fingerId)`
- `fingerprint` — `(userID, timestamp)` — attendance log

---

## Project Structure

```
Touch-And-Go/
├── README.md
├── .env.example               # Copy to .env and fill in credentials
├── .gitignore
├── requirements.txt
│
├── src/
│   ├── scan.py                # Main attendance scanning loop
│   ├── maintain.py            # Admin: enroll, delete, reset fingerprints
│   └── db/
│       ├── config.py          # Centralized DB connection (reads from .env)
│       ├── pull_db.py         # Utility: query student records
│       └── push_db.py         # Utility: insert student records
│
├── ui/                        # Student-facing web interface
│   ├── styles.css
│   ├── logo.jpg
│   └── student/
│       ├── login.html
│       ├── home.html
│       ├── schedule.html
│       ├── analytics.html
│       ├── contact.html
│       ├── help.html
│       └── logout.html
│
├── lib/                       # Third-party I2C LCD library
│   ├── i2c_lcd.py
│   ├── lcd_api.py
│   └── LICENSE
│
├── tests/
│   ├── test_db.py             # MySQL connection and insertion tests
│   └── test_fingerprint.py   # Fingerprint sensor hardware tests
│
└── docs/
    ├── hardware-setup.md
    ├── database-schema.md
    ├── software-development-plan.md
    └── diagrams/
        ├── class-diagram.png
        ├── sequence-diagram.png
        └── use-case-diagram.png
```

---

## Getting Started

### Prerequisites

- Raspberry Pi running Raspberry Pi OS (tested on Python 3.9)
- Adafruit AS608 fingerprint sensor connected via USB UART adapter
- I2C LCD (20×4) at address `0x27`
- MySQL database (local or remote)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/NathanShutter/Touch-And-Go.git
cd Touch-And-Go

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
nano .env

# 4. Enable I2C on your Raspberry Pi (if not already)
sudo raspi-config  # Interface Options → I2C → Enable
```

### Environment Variables

All database credentials are loaded from a `.env` file. **Never commit your `.env` to version control.**

```env
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=touch_and_go
```

---

## Usage

### Enrolling a Student (Admin)

Run `maintain.py` to manage fingerprint templates stored on the sensor:

```bash
python src/maintain.py
```

Menu options:
- `e` — Enroll a new fingerprint (scans twice, stores template, links to student record)
- `d` — Delete a fingerprint by ID
- `r` — Reset the entire fingerprint library
- `q` — Quit

### Running Attendance Scanning

```bash
python src/scan.py
```

The script runs continuously. Each detected fingerprint triggers a database insert. Press `Ctrl+C` to stop.

### Database Utilities

```bash
# View all student records
python src/db/pull_db.py

# Add a student record manually
python src/db/push_db.py
```

---

## Web UI

The `ui/` directory contains a static HTML/CSS student portal. Pages include:

| Page | Description |
|---|---|
| `login.html` | Student login |
| `home.html` | Dashboard |
| `schedule.html` | Class schedule |
| `analytics.html` | Attendance analytics |
| `contact.html` | Contact information |
| `help.html` | Help & FAQ |
| `logout.html` | Session logout |

Color palette: `#10222E` (navy) and `#FAF8D6` (cream).

---

## Documentation

Full project documentation is located in [`docs/`](docs/):

- [Hardware Setup](docs/hardware-setup.md) — Wiring, sensor calibration, I2C configuration
- [Database Schema](docs/database-schema.md) — Table definitions, ER diagram, sample queries
- [Software Development Plan](docs/software-development-plan.md) — Sprints, Gantt chart, retrospectives

---

## Team

| Name | Role |
|---|---|
| Nathan Shutter | Systems architecture, OU/configuration, delivery |
| Joe | Software process, validation, sequence diagrams |
| Chris | Hardware research, prototype, budget |

**Course:** CSC354 — Software Engineering
**Institution:** Kutztown University of Pennsylvania
**Semester:** Fall 2023

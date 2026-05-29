# Touch & Go

> A biometric attendance tracking system using fingerprint scanning — built for university classrooms on a Raspberry Pi.

> [!NOTE]
> **This project is no longer live.** Touch & Go was a university capstone project completed in Fall 2023. The production site (`touchandgo.software`) and AWS staging environment are no longer running. This repository is preserved as a portfolio and academic archive.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Use Cases & Actors](#use-cases--actors)
- [Fingerprint Scan Flow](#fingerprint-scan-flow)
- [Requirements UML Diagrams](#requirements-uml-diagrams)
- [Database Design](#database-design)
- [Sequence Diagrams](#sequence-diagrams)
- [Testing](#testing)
- [Project Documentation](#project-documentation)
- [Team](#team)

---

## Overview

Touch & Go replaces paper sign-in sheets and manual roll calls with a fingerprint scanner mounted in the classroom. Students scan their finger to mark attendance, professors receive instant attendance reports, and maintenance staff manage enrollments through an admin panel.

The system runs a Python scanner application on a Raspberry Pi connected to an Adafruit fingerprint sensor. A PHP/MySQL web application hosted on AWS handles the admin portal, professor dashboard, and attendance records.

**Key capabilities:**
- Fingerprint scan → database match → attendance recorded in real time
- LCD display gives the student immediate confirmation or error feedback
- Professor dashboard with per-class attendance lists and export
- Admin panel for enrolling fingerprints, managing users, and resetting the scanner
- Automated email attendance reports via cron/SMTP

---

## System Architecture

![UML Context Diagram](docs/images/UML-Context-Diagram.png)

The Raspberry Pi communicates with the fingerprint sensor over I²C. On a successful scan, the Python app queries the MySQL database hosted on AWS to match the fingerprint template and record attendance. The PHP web app sits in front of the same database and provides the professor and admin interfaces.

**Environments (no longer active):**
- Development: `http://localhost/`
- Staging: `http://3.90.89.76/`
- Production: `https://touchandgo.software/`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Hardware | Raspberry Pi, Adafruit Fingerprint Sensor, I²C LCD Display |
| Scanner App | Python |
| Web Backend | PHP |
| Database | MySQL |
| Hosting | AWS EC2 |
| Diagramming | draw.io |

---

## Use Cases & Actors

![UML Use Case Diagram](docs/images/UML-Use-Case-Diagram.png)

Three actors interact with the system:

**Students** — scan their fingerprint to record attendance and receive immediate LCD feedback confirming the scan.

**Professors** — start a class session, then receive a report of who attended and who didn't.

**Maintenance Staff** — manage the admin panel: enroll/remove fingerprints, manage users, initialize class lists, and troubleshoot hardware.

| Use Case | Actor(s) | Description |
|---|---|---|
| Scan Finger | Student | Finger placed on scanner; authenticated against the database and attendance recorded |
| Get Feedback | Student, Professor | Student gets LCD confirmation; professor receives attendance report |
| Update Data | Maintenance Staff | Add/remove fingerprint templates, initialize class lists, resolve data errors |
| Maintain Scanner | Maintenance Staff | Troubleshoot and reset scanner; replace hardware if needed |
| Login / Logout | All | Authenticated access to the web portal |
| Filter Results | Professor | View and filter attendance records by class, date, or student |

---

## Fingerprint Scan Flow

Two approaches were designed during the project. Idea 2 (template-based matching) was implemented, giving finer control over the matching logic by storing raw binary data and building templates in-house rather than relying entirely on the scanner's built-in API.

### Idea 1 — API-Based Matching

![Fingerprint Flow - Idea 1](docs/images/fingerprint-flow-idea-1.png)

The scanner's built-in API handles matching. On a hit, a record is written to the database with the student name and timestamp. A time-triggered cron job queries records and emails the attendance report via SMTP.

### Idea 2 — Template-Based Matching *(Implemented)*

![Fingerprint Flow - Idea 2](docs/images/fingerprint-flow-idea-2.png)

Raw fingerprint binary is captured and stored in the database. Custom code builds templates from the stored data, then uses the scanner API to compare against a live scan. On a match, attendance is recorded and the LCD displays a confirmation message.

---

## Requirements UML Diagrams

Individual use case diagrams were produced for each functional requirement.

### Scan Finger

![Scan Finger UML](docs/images/ScanFingerUML.png)

### Maintain Scanner

![Maintain Scanner UML](docs/images/MaintainUML.png)

### Other Systems

![Other Systems UML](docs/images/OtherSystemsUML.png)

### Security

![Security UML](docs/images/SecurityUML.png)

### Performance

![Performance UML](docs/images/PerformanceUML.png)

> Draw.io source files for all requirements UML diagrams (including GetFeedback, UpdateData, Login, Logout, FilterResults, HardwareHousing) are in [`docs/diagrams/`](docs/diagrams/).

---

## Database Design

The database tracks students, professors, courses, fingerprint templates, and attendance records.

> Draw.io source: [`docs/diagrams/DatabaseSchema.drawio`](docs/diagrams/DatabaseSchema.drawio)

**Key entities:**

| Entity | Key Fields |
|---|---|
| Student | `student_id`, `first_name`, `last_name`, `email`, `password`, `fingerprint (BLOB)` |
| Professor | `professor_id`, `first_name`, `last_name`, `email`, `password` |
| Course | `course_id`, `course_name`, `professor_id (FK)`, `students_enrolled` |
| Attendance | `record_id`, `student_id (FK)`, `course_id (FK)`, `timestamp` |
| Maintenance Staff | `staff_id`, `first_name`, `last_name`, `email`, `password` |

---

## Sequence Diagrams

Draw.io source files for all sequence diagrams are in [`docs/diagrams/`](docs/diagrams/). To view, open with [draw.io](https://app.diagrams.net/) or the VS Code Draw.io extension.

| Diagram | File |
|---|---|
| Login | `LoginSequenceDiagram.drawio` |
| Register Account | `NewRegisterAccountSequenceDiagram.drawio` |
| Complete Scan Flow | `CompleteSequenceDiagram.drawio` |
| Add User | `addUser.drawio` |
| Edit User | `editUser.drawio` |
| Search User | `searchUser.drawio` |
| Create Course | `createCourse.drawio` |
| Edit Course | `editCourse.drawio` |
| Professor Course View | `professorCourse.drawio` |
| Student Course View | `studentCourse.drawio` |
| View Student Contact Info | `viewStudentContactInformation.drawio` |

---

## Testing

Testing was conducted manually against defined test cases in Sprint 6.

| Test Case | Result |
|---|---|
| Scan Finger | Passed |
| Get Feedback | Passed |
| Update Data | Passed |
| Maintain Scanner | Passed |
| Login | Passed |
| Logout | Passed |
| Other Systems | Passed |
| Maintainability | Passed |
| Filter Results | Untested |
| Security | Untested |
| Performance | Untested |
| Housing | Untested |

Automated testing was explored but not implemented within the project timeline.

---

## Project Documentation

Full documentation archive is in [`docs/diagrams/`](docs/diagrams/) and the original project files are on [Google Drive](https://drive.google.com/drive/folders/1u4nIICvpnq-juQDpWkTJimE453x217N9).

| Document | Description |
|---|---|
| Software Requirements Specification | Functional and non-functional requirements |
| Detailed Design Document | System-level design decisions |
| UML Diagrams | Context, use case, and requirements diagrams |
| Sequence Diagrams | All user flows and interactions |
| Requirements Traceability Matrix | Requirements mapped to test cases |
| Sprint 6 Presentation | Final demo deck |

---

## Team

Developed as a software engineering capstone project.

| Name | Role |
|---|---|
| Nathan Shutter | Developer |
| [Teammate] | Developer |
| [Teammate] | Developer |

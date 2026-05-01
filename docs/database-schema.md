# Database Schema

Touch & Go uses a MySQL database hosted on AWS. Two core tables drive the system.

---

## Tables

### `student`

Stores enrolled student records. The `fingerId` field is populated during enrollment and links a student to their fingerprint template slot on the AS608 sensor.

```sql
CREATE TABLE student (
    userID    INT          NOT NULL PRIMARY KEY,
    firstName VARCHAR(50)  NOT NULL,
    lastName  VARCHAR(50)  NOT NULL,
    email     VARCHAR(100),
    fingerId  INT                        -- Sensor template slot (0–126), NULL until enrolled
);
```

### `fingerprint`

Attendance log. Each row represents a successful scan — one record per student per class session.

```sql
CREATE TABLE fingerprint (
    userID     INT          NOT NULL,
    timestamp  DATETIME     NOT NULL,
    FOREIGN KEY (userID) REFERENCES student(userID)
);
```

---

## Entity Relationship Diagram

```
┌─────────────────────────┐         ┌─────────────────────┐
│         student         │         │     fingerprint      │
├─────────────────────────┤         ├─────────────────────┤
│ PK  userID    INT       │──────── │ FK  userID    INT   │
│     firstName VARCHAR   │  1 : N  │     timestamp DATETIME│
│     lastName  VARCHAR   │         └─────────────────────┘
│     email     VARCHAR   │
│     fingerId  INT       │ ◄── AS608 sensor template slot
└─────────────────────────┘
```

---

## Common Queries

**Get all attendance records for a specific student:**

```sql
SELECT s.firstName, s.lastName, f.timestamp
FROM fingerprint f
JOIN student s ON f.userID = s.userID
WHERE s.userID = 42
ORDER BY f.timestamp DESC;
```

**Count attendance per student:**

```sql
SELECT s.firstName, s.lastName, COUNT(f.userID) AS attendance_count
FROM student s
LEFT JOIN fingerprint f ON s.userID = f.userID
GROUP BY s.userID
ORDER BY attendance_count DESC;
```

**Find students not yet enrolled (no fingerId):**

```sql
SELECT userID, firstName, lastName
FROM student
WHERE fingerId IS NULL;
```

---

## Environment Setup

Database credentials are loaded from `.env`. See `.env.example` for the required variables. The connection is managed centrally in `src/db/config.py` — no credentials appear anywhere in the source files.

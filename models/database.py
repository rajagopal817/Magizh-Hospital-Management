"""
models/database.py
------------------
Opens the SQLite database, runs queries and creates the tables.
"""

import sqlite3
import config


# In demo mode the database lives only in memory (RAM), so nothing is
# written to disk. One connection is kept open for the whole session,
# because an in-memory database disappears when its connection closes.
_demo_connection = None


def get_connection():
    global _demo_connection
    if config.DEMO_MODE:
        if _demo_connection is None:
            _demo_connection = sqlite3.connect(":memory:")
        return _demo_connection
    return sqlite3.connect(config.DB_PATH)


def run_query(sql, params=(), fetch=False):
    """Run one SQL statement.
    fetch=True  -> returns the rows (for SELECT)
    fetch=False -> returns the id of the new row (for INSERT/UPDATE)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    result = cur.fetchall() if fetch else cur.lastrowid
    conn.commit()
    if not config.DEMO_MODE:
        conn.close()
    return result


def setup_database():
    """Create the tables on first run and add sample data."""
    run_query("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )""")
    run_query("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            age         INTEGER NOT NULL,
            gender      TEXT NOT NULL,
            contact     TEXT NOT NULL,
            address     TEXT,
            symptoms    TEXT,
            created_on  TEXT NOT NULL
        )""")
    run_query("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            department     TEXT NOT NULL,
            specialization TEXT,
            contact        TEXT,
            available_days TEXT
        )""")
    run_query("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id     INTEGER NOT NULL,
            doctor_id      INTEGER NOT NULL,
            department     TEXT NOT NULL,
            app_date       TEXT NOT NULL,
            app_time       TEXT NOT NULL,
            reason         TEXT,
            status         TEXT NOT NULL DEFAULT 'Booked',
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY (doctor_id)  REFERENCES doctors(doctor_id)
        )""")

    # Default admin user
    if not run_query("SELECT * FROM users", fetch=True):
        run_query("INSERT INTO users VALUES (?, ?)",
                  (config.DEFAULT_USERNAME, config.DEFAULT_PASSWORD))

    # Sample doctors so the demo is not empty
    if not run_query("SELECT * FROM doctors", fetch=True):
        sample = [
            ("Doctor 1", "General Medicine", "MBBS, MD", "98XXXXX111", "Mon-Sat"),
            ("Doctor 2", "Cardiology", "MD, DM Cardiology", "98XXXXX222", "Mon-Fri"),
            ("Doctor 3", "Orthopedics", "MS Ortho", "98XXXXX333", "Tue-Sat"),
            ("Doctor 4", "Pediatrics", "MD Pediatrics", "98XXXXX444", "Mon-Sat"),
        ]
        for d in sample:
            run_query("""INSERT INTO doctors (name, department, specialization,
                         contact, available_days) VALUES (?, ?, ?, ?, ?)""", d)

    # Demo version: fill every screen with sample data
    if config.DEMO_MODE:
        from models.demo_data import load_demo_data
        load_demo_data()

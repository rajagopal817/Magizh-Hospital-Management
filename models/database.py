"""
models/database.py
------------------
Opens the SQLite database, runs queries and creates the tables.
"""

import sqlite3
import config


def run_query(sql, params=(), fetch=False):
    """Run one SQL statement.
    fetch=True  -> returns the rows (for SELECT)
    fetch=False -> returns the id of the new row (for INSERT/UPDATE)
    """
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute(sql, params)
    result = cur.fetchall() if fetch else cur.lastrowid
    conn.commit()
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
            ("Dr. Arun Kumar", "General Medicine", "MBBS, MD", "9840011111", "Mon-Sat"),
            ("Dr. Priya Raman", "Cardiology", "MD, DM Cardiology", "9840022222", "Mon-Fri"),
            ("Dr. Senthil Nathan", "Orthopedics", "MS Ortho", "9840033333", "Tue-Sat"),
            ("Dr. Meena Lakshmi", "Pediatrics", "MD Pediatrics", "9840044444", "Mon-Sat"),
        ]
        for d in sample:
            run_query("""INSERT INTO doctors (name, department, specialization,
                         contact, available_days) VALUES (?, ?, ?, ?, ?)""", d)

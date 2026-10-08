# Surya Hospital Management System

A Python desktop application for managing patients, doctors and appointments,
built with **Tkinter** (screens) and **SQLite** (database) using the **MVC pattern**.

## Features
- Admin login
- Dashboard with patient, doctor and appointment counts
- Patient registration, view and search
- Doctor management and department assignment
- Appointment booking with confirmation, double-booking check and cancellation
- Reports: appointment summary (by doctor / department / date) and patient history

## Project structure
```
main.py              Starts the app
config.py            Settings (hospital name, colours, departments)
models/              Model: database tables and queries
views/               View: Tkinter screens
controllers/         Controller: validation and logic between views and models
```

## How to run
```
python main.py
```
Default login: `admin` / `admin123`

## Build the .exe (Windows)
```
pip install pyinstaller
pyinstaller --onefile --windowed --name HMS main.py
```
The program is created at `dist/HMS.exe`.

## Requirements
- Python 3.x (Tkinter and SQLite are included with Python, no extra libraries needed)

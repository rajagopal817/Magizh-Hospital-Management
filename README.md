# Real-Time Smart Sensor and PPG Data Analytics (Mobile): Makizh Tech

Android app (Python + Flet, MVC pattern). It is a proof of concept: the Bluetooth devices and the PPG signal are simulated. It has the same features as the Windows desktop version.

## Login
- Username: `admin`
- Password: `admin123`

## How to use
1. **Scan**: finds the Bluetooth devices.
2. Pick a device from the list, then tap **Connect**. A "Bluetooth Connected" popup appears.
3. **Start**: the live PPG graph begins. Tap **Pause** to stop it.
4. **Baud rate**, **Signal units** and **Window (ms)** (− / +) change the settings and the graph.
5. **Save CSV** exports the recording. **Clear** empties the graph.
6. **Disconnect**, **Logout**

## Requirements
- Python 3.10 or newer
- `pip install -r requirements.txt`

## Run on a PC (phone-sized window)
```
flet run
```

## Build the Android .apk
```
flet build apk
```
The output is `build\apk\`. The first build downloads the Flutter SDK, JDK and Android SDK automatically, so it takes a while.

## Folders
- `src/main.py`: app start
- `src/models/`: data (recording, PPG simulator, users)
- `src/views/`: screens (login, dashboard, graph)
- `src/controllers/`: logic (login, device, streaming)
- `src/config.py`: names, colours, settings
- `pyproject.toml`: app name and build settings for the .apk

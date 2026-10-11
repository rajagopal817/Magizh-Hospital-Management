# Real-Time Smart Sensor and PPG Data Analytics — Makizh Tech

Windows desktop app (Python + Tkinter, MVC pattern). It is a proof of concept: the Bluetooth devices and the PPG signal are simulated.

## Login
- Username: `admin`
- Password: `admin123`

## How to use
1. **Scan**: finds the Bluetooth devices.
2. Pick a device from the list, then click **Connect**. A "Bluetooth Connected" popup appears.
3. **Start**: the live PPG graph begins. Click **Pause** to stop it.
4. **Baud rate**, **Signal units** and **Window (ms)** change the settings and the graph.
5. **Save CSV** exports the recording. **Clear** empties the graph.
6. **Disconnect**, **Logout**

## Run
```
python main.py
```

## Build .exe
```
python -m PyInstaller --onefile --windowed --name Makizh_PPG_Analytics main.py
```
The output is `dist\Makizh_PPG_Analytics.exe`.

## Folders
- `models/`: data (recording, PPG simulator, users)
- `views/`: screens (login, dashboard, graph)
- `controllers/`: logic (login, device, streaming)
- `config.py`: names, colours, settings

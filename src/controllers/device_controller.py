"""
controllers/device_controller.py
--------------------------------
Bluetooth device handling: scan, connect, disconnect, baud rate.

POC version: the device list is simulated (config.DEMO_DEVICES).
Later this is where the real Bluetooth / serial connection will go.
"""

import config


class DeviceController:
    def __init__(self):
        self.devices = []
        self.connected_device = None
        self.baud_rate = config.DEFAULT_BAUD

    @property
    def is_connected(self):
        return self.connected_device is not None

    def scan(self):
        """Return the list of devices found nearby."""
        self.devices = list(config.DEMO_DEVICES)
        return self.devices

    def connect(self, device_name):
        """Returns (success, title, message)."""
        if not device_name:
            return False, "Select Device", "Please click 'Scan' and select a device first."
        if self.is_connected:
            return False, "Already Connected", f"Already connected to {self.connected_device}."
        self.connected_device = device_name
        return True, "Bluetooth Connected", (
            "Bluetooth connected successfully!\n\n"
            f"Device : {device_name}\n"
            f"Baud rate : {self.baud_rate}")

    def disconnect(self):
        name = self.connected_device
        self.connected_device = None
        return "Bluetooth Disconnected", f"Disconnected from {name}."

    def set_baud_rate(self, baud):
        self.baud_rate = baud

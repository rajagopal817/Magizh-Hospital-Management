"""
controllers/stream_controller.py
--------------------------------
Recording logic: start / pause, reading new samples, clear, save CSV.

POC version: samples come from the PPG simulator.
Later the same methods will read real values from the sensor.
"""

import time
import config
from models.ppg_simulator import PPGSimulator
from models.recording import Recording


class StreamController:
    def __init__(self):
        self.recording = Recording()
        self.simulator = PPGSimulator()
        self.is_running = False
        self._sim_time_ms = 0          # time of the next sample
        self._last_wall_time = None

    # ---------- Start / Pause ----------
    def start(self):
        self.is_running = True
        self._last_wall_time = time.monotonic()

    def pause(self):
        self.is_running = False

    def read_new_samples(self):
        """Add the samples that 'arrived' since the last call. Returns how many."""
        if not self.is_running:
            return 0
        now = time.monotonic()
        elapsed_ms = (now - self._last_wall_time) * 1000
        count = int(elapsed_ms // config.SAMPLE_INTERVAL_MS)
        if count <= 0:
            return 0
        self._last_wall_time += count * config.SAMPLE_INTERVAL_MS / 1000
        for _ in range(count):
            value = self.simulator.value_at(self._sim_time_ms)
            self.recording.add(self._sim_time_ms, value)
            self._sim_time_ms += config.SAMPLE_INTERVAL_MS
        return count

    # ---------- Clear / Save ----------
    def clear(self):
        self.recording.clear()
        self._sim_time_ms = 0

    def has_data(self):
        return len(self.recording.samples) > 0

    def save_csv(self, path, unit):
        """Returns (title, message)."""
        count = self.recording.save_csv(path, unit)
        return "CSV Saved", f"{count:,} samples saved to:\n{path}"

    def csv_bytes(self, unit):
        """CSV file contents as bytes (the phone's Save dialog writes these)."""
        return self.recording.csv_text(unit).encode("utf-8")

    def sample_count(self):
        return len(self.recording.samples)

    # ---------- Information for the screen ----------
    def stats_text(self):
        r = self.recording
        return (f"Recorded: {r.total_recorded:,} | Retained: {len(r.samples):,} | "
                f"Invalid lines: {r.invalid_lines} | Queue drops: {r.queue_drops}")

    def window_samples(self, window_ms):
        return self.recording.window(window_ms)

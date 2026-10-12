"""
models/recording.py
-------------------
Holds the recorded samples (time in ms, signal value) and saves them as CSV.
"""

import csv
import io
from collections import deque
import config


class Recording:
    def __init__(self):
        self.samples = deque(maxlen=config.MAX_SAMPLES)   # keeps only the latest samples
        self.total_recorded = 0
        self.invalid_lines = 0
        self.queue_drops = 0

    def add(self, t_ms, value):
        self.samples.append((t_ms, value))
        self.total_recorded += 1

    def clear(self):
        self.samples.clear()
        self.total_recorded = 0
        self.invalid_lines = 0
        self.queue_drops = 0

    def last_time(self):
        return self.samples[-1][0] if self.samples else 0

    def window(self, window_ms):
        """Samples from the last `window_ms` milliseconds (for the graph)."""
        if not self.samples:
            return []
        start = self.samples[-1][0] - window_ms
        result = []
        for t, v in reversed(self.samples):
            if t < start:
                break
            result.append((t, v))
        result.reverse()
        return result

    def csv_text(self, unit):
        """The whole recording as CSV text (used on Android to save the file)."""
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(["time_ms", f"signal_{unit}"])
        writer.writerows(self.samples)
        return out.getvalue()

    def save_csv(self, path, unit):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time_ms", f"signal_{unit}"])
            writer.writerows(self.samples)
        return len(self.samples)

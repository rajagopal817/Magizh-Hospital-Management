"""
models/ppg_simulator.py
-----------------------
Demo PPG (photoplethysmogram) signal generator.

In the real product this will be replaced by readings from the Bluetooth
sensor. For the POC it produces a realistic-looking pulse wave:
a sharp systolic peak, a small dip (dicrotic notch) and a smaller
diastolic bump, repeating at about 75 beats per minute.
"""

import math
import random


class PPGSimulator:
    def __init__(self, heart_rate_bpm=75):
        self.heart_rate_bpm = heart_rate_bpm

    def value_at(self, t_ms):
        """Signal value (roughly 0.3 to 0.7) at time t_ms."""
        period_ms = 60000 / self.heart_rate_bpm
        phase = (t_ms % period_ms) / period_ms          # 0..1 within one beat

        systolic = 0.35 * math.exp(-((phase - 0.22) / 0.075) ** 2)
        diastolic = 0.09 * math.exp(-((phase - 0.52) / 0.07) ** 2)
        baseline = 0.33 + 0.01 * math.sin(2 * math.pi * t_ms / 7000)   # slow breathing drift
        noise = random.uniform(-0.006, 0.006)

        return round(baseline + systolic + diastolic + noise, 4)

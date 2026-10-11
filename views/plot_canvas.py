"""
views/plot_canvas.py
--------------------
The live graph, drawn on a Tkinter Canvas (no extra libraries needed).
X axis: Time (ms).  Y axis: signal value 0 to 1.
"""

import tkinter as tk
import config

MARGIN_LEFT = 75
MARGIN_RIGHT = 20
MARGIN_TOP = 10
MARGIN_BOTTOM = 55
NICE_STEPS = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]


class PlotCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg=config.WHITE, highlightthickness=0)
        self.samples = []
        self.window_ms = config.DEFAULT_WINDOW_MS
        self.y_label = config.SIGNAL_UNITS[config.DEFAULT_UNIT]
        self.bind("<Configure>", lambda e: self._redraw())

    def update_plot(self, samples, window_ms, y_label):
        self.samples = samples
        self.window_ms = window_ms
        self.y_label = y_label
        self._redraw()

    # ---------- drawing ----------
    def _redraw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 200 or h < 150:
            return
        left, right = MARGIN_LEFT, w - MARGIN_RIGHT
        top, bottom = MARGIN_TOP, h - MARGIN_BOTTOM

        # Visible time range: fills from the left, then scrolls
        last_t = self.samples[-1][0] if self.samples else 0
        x_start = max(0, last_t - self.window_ms)
        x_end = x_start + self.window_ms

        def to_x(t):
            return left + (t - x_start) / (x_end - x_start) * (right - left)

        def to_y(v):
            return bottom - v * (bottom - top)

        # Grid: minor lines first, then major lines
        step = next((s for s in NICE_STEPS if s >= self.window_ms / 10), NICE_STEPS[-1])
        minor = step / 5
        t = (x_start // minor + 1) * minor
        while t < x_end:
            self.create_line(to_x(t), top, to_x(t), bottom, fill=config.GRID_MINOR)
            t += minor
        for i in range(1, 20):
            v = i * 0.05
            self.create_line(left, to_y(v), right, to_y(v), fill=config.GRID_MINOR)

        t = (x_start // step + 1) * step
        while t < x_end:
            x = to_x(t)
            self.create_line(x, top, x, bottom, fill=config.GRID_MAJOR)
            self.create_text(x, bottom + 15, text=f"{int(t)}", font=("Segoe UI", 9), fill="#333")
            t += step
        for v in (0.2, 0.4, 0.6, 0.8):
            y = to_y(v)
            self.create_line(left, y, right, y, fill=config.GRID_MAJOR)
            self.create_text(left - 8, y, text=f"{v:.1f}", anchor="e",
                             font=("Segoe UI", 9), fill="#333")

        # Axes and labels
        self.create_line(left, top, left, bottom, fill=config.AXIS)
        self.create_line(left, bottom, right, bottom, fill=config.AXIS)
        self.create_text((left + right) / 2, bottom + 40, text="Time (ms)",
                         font=("Segoe UI", 11), fill="#333")
        self.create_text(22, (top + bottom) / 2, text=self.y_label, angle=90,
                         font=("Segoe UI", 11), fill="#333")

        # The signal line
        points = [(t, v) for t, v in self.samples if t >= x_start]
        if len(points) >= 2:
            coords = []
            for t, v in points:
                coords.extend((to_x(t), to_y(max(0.0, min(1.0, v)))))
            self.create_line(*coords, fill=config.PLOT_LINE, width=1.5)

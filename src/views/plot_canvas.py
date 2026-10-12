"""
views/plot_canvas.py
--------------------
The live graph, drawn on a Flet Canvas (no chart library needed).
X axis: Time (ms).  Y axis: signal value 0 to 1.
"""

import math
import flet as ft
import flet.canvas as cv
import config

MARGIN_LEFT = 46
MARGIN_RIGHT = 12
MARGIN_TOP = 8
MARGIN_BOTTOM = 42
NICE_STEPS = [100, 200, 500, 1000, 2000, 5000, 10000, 20000]

LABEL_STYLE = ft.TextStyle(size=10, color="#333333")
TITLE_STYLE = ft.TextStyle(size=12, color="#333333")


def _paint(color, width=1.0):
    return ft.Paint(color=color, stroke_width=width, style=ft.PaintingStyle.STROKE)


class PlotCanvas:
    def __init__(self, height=330):
        self.samples = []
        self.window_ms = config.DEFAULT_WINDOW_MS
        self.y_label = config.SIGNAL_UNITS[config.DEFAULT_UNIT]
        self.width = 360          # updated as soon as the canvas knows its real size
        self.height = height
        self.canvas = cv.Canvas(height=height, expand=True, on_resize=self._on_resize,
                                resize_interval=100)
        # The control to put on the screen
        self.control = ft.Container(content=self.canvas, height=height,
                                    bgcolor=config.WHITE)
        self._draw()

    def _on_resize(self, e):
        self.width, self.height = e.width, e.height
        self._draw()
        self.canvas.update()

    def update_plot(self, samples, window_ms, y_label):
        self.samples = samples
        self.window_ms = window_ms
        self.y_label = y_label
        self._draw()

    # ---------- drawing ----------
    def _draw(self):
        w, h = self.width, self.height
        left, right = MARGIN_LEFT, w - MARGIN_RIGHT
        top, bottom = MARGIN_TOP, h - MARGIN_BOTTOM
        shapes = []

        # Visible time range: fills from the left, then scrolls
        last_t = self.samples[-1][0] if self.samples else 0
        x_start = max(0, last_t - self.window_ms)
        x_end = x_start + self.window_ms

        def to_x(t):
            return left + (t - x_start) / (x_end - x_start) * (right - left)

        def to_y(v):
            return bottom - v * (bottom - top)

        # Grid: fewer labels than desktop because the phone screen is narrow
        step = next((s for s in NICE_STEPS if s >= self.window_ms / 5), NICE_STEPS[-1])
        minor = step / 5
        t = (x_start // minor + 1) * minor
        while t < x_end:
            shapes.append(cv.Line(to_x(t), top, to_x(t), bottom, _paint(config.GRID_MINOR)))
            t += minor
        for i in range(1, 20):
            y = to_y(i * 0.05)
            shapes.append(cv.Line(left, y, right, y, _paint(config.GRID_MINOR)))

        t = (x_start // step + 1) * step
        while t < x_end:
            x = to_x(t)
            shapes.append(cv.Line(x, top, x, bottom, _paint(config.GRID_MAJOR)))
            shapes.append(cv.Text(x, bottom + 4, f"{int(t)}", style=LABEL_STYLE,
                                  alignment=ft.Alignment.TOP_CENTER))
            t += step
        for v in (0.2, 0.4, 0.6, 0.8):
            y = to_y(v)
            shapes.append(cv.Line(left, y, right, y, _paint(config.GRID_MAJOR)))
            shapes.append(cv.Text(left - 5, y, f"{v:.1f}", style=LABEL_STYLE,
                                  alignment=ft.Alignment.CENTER_RIGHT))

        # Axes and labels
        shapes.append(cv.Line(left, top, left, bottom, _paint(config.AXIS)))
        shapes.append(cv.Line(left, bottom, right, bottom, _paint(config.AXIS)))
        shapes.append(cv.Text((left + right) / 2, bottom + 22, "Time (ms)", style=TITLE_STYLE,
                              alignment=ft.Alignment.TOP_CENTER))
        shapes.append(cv.Text(10, (top + bottom) / 2, self.y_label, style=TITLE_STYLE,
                              alignment=ft.Alignment.CENTER, rotate=-math.pi / 2))

        # The signal line (at most about one point per pixel, keeps the phone fast)
        points = [(t, v) for t, v in self.samples if t >= x_start]
        if len(points) >= 2:
            every = max(1, len(points) // int(max(1, right - left)))
            offsets = [ft.Offset(to_x(t), to_y(max(0.0, min(1.0, v))))
                       for t, v in points[::every]]
            shapes.append(cv.Points(points=offsets, point_mode=cv.PointMode.POLYGON,
                                    paint=_paint(config.PLOT_LINE, 1.5)))

        self.canvas.shapes = shapes

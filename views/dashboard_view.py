"""
views/dashboard_view.py
-----------------------
The PPG plotter dashboard.

Disconnected : Scan, device list, Connect, Start, Save CSV, Clear, Window (ms)
Connected    : also shows Baud rate, Signal units, recording counts and info bar
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import config
from controllers.device_controller import DeviceController
from controllers.stream_controller import StreamController
from views.plot_canvas import PlotCanvas


class DashboardView:
    def __init__(self, root, username, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.device = DeviceController()
        self.stream = StreamController()
        self._timer = None

        root.title(config.DASHBOARD_TITLE)
        root.resizable(True, True)
        root.minsize(1000, 640)
        root.geometry("1150x720")
        self._maximize(root)
        root.configure(bg=config.WHITE)
        self._setup_styles()

        # ---- Banner ----
        banner = tk.Frame(root, bg=config.PRIMARY, height=150)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text=config.BANNER_TEXT, font=("Segoe UI", 20),
                 bg=config.PRIMARY, fg=config.WHITE).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(banner, text="Logout", command=self.logout, bg=config.WHITE,
                  fg=config.PRIMARY, relief="flat", padx=10).place(relx=1.0, x=-15, y=12, anchor="ne")
        tk.Label(banner, text=f"Logged in as: {username}", bg=config.PRIMARY,
                 fg=config.WHITE).place(relx=1.0, x=-85, y=14, anchor="ne")

        body = tk.Frame(root, bg=config.WHITE)
        body.pack(fill="both", expand=True, padx=12, pady=(8, 0))
        self.body = body

        # ---- Row 1: Scan | device | Connect | Start | Save CSV | Clear | Window (ms) ----
        self.window_var = tk.StringVar(value=str(config.DEFAULT_WINDOW_MS))
        row1 = tk.Frame(body, bg=config.WHITE)
        row1.pack(fill="x", pady=(0, 6))
        self.row1 = row1
        self.scan_btn = ttk.Button(row1, text="Scan", command=self.scan)
        self.scan_btn.pack(side="left", padx=(0, 8), ipady=4)
        self.device_box = ttk.Combobox(row1, state="readonly", width=48)
        self.device_box.pack(side="left", padx=(0, 8), ipady=4)
        self.connect_btn = ttk.Button(row1, text="Connect", command=self.toggle_connect)
        self.connect_btn.pack(side="left", padx=(0, 8), ipady=4)
        self.start_btn = ttk.Button(row1, text="Start", style="Green.TButton", command=self.toggle_start)
        self.start_btn.pack(side="left", padx=(0, 8), ipady=4)
        ttk.Button(row1, text="Save CSV", command=self.save_csv).pack(side="left", padx=(0, 8), ipady=4)
        ttk.Button(row1, text="Clear", command=self.clear).pack(side="left", padx=(0, 8), ipady=4)
        self.window_group1 = self._window_group(row1)
        self.window_group1.pack(side="left", padx=(6, 0))

        # ---- Row 2 (connected only): Baud rate | Window (ms) | Signal units ----
        row2 = tk.Frame(body, bg=config.WHITE)
        self.row2 = row2
        tk.Label(row2, text="Baud rate:", bg=config.WHITE, font=("Segoe UI", 10)).pack(side="left")
        self.baud_box = ttk.Combobox(row2, state="readonly", width=22, values=config.BAUD_RATES)
        self.baud_box.set(config.DEFAULT_BAUD)
        self.baud_box.bind("<<ComboboxSelected>>", lambda e: self.change_baud())
        self.baud_box.pack(side="left", padx=(6, 0), ipady=3)
        self.unit_box = ttk.Combobox(row2, state="readonly", width=12,
                                     values=list(config.SIGNAL_UNITS.keys()))
        self.unit_box.set(config.DEFAULT_UNIT)
        self.unit_box.bind("<<ComboboxSelected>>", lambda e: self.redraw())
        self.unit_box.pack(side="right", ipady=3)
        tk.Label(row2, text="Signal units:", bg=config.WHITE,
                 font=("Segoe UI", 10)).pack(side="right", padx=(0, 6))
        self.window_group2 = self._window_group(row2)
        self.window_group2.pack(side="left", expand=True)

        # ---- Status lines ----
        self.status = tk.Label(body, text="Status: Disconnected", bg=config.WHITE,
                               font=("Segoe UI", 10), fg="#444")
        self.status.pack(pady=(2, 0))
        self.stats = tk.Label(body, text="", bg=config.WHITE, font=("Segoe UI", 10), fg="#444")

        # ---- Footer info (connected only) ----
        self.footer = tk.Label(root, text=config.FOOTER_INFO, bg="#EBEBEB", anchor="w",
                               font=("Segoe UI", 10), padx=8, pady=4)

        # ---- Graph ----
        self.plot = PlotCanvas(body)
        self.plot.pack(fill="both", expand=True, pady=(4, 8))

        self._tick()

    # ================= helpers =================
    @staticmethod
    def _maximize(root):
        """Open the dashboard maximized to fill the whole screen."""
        try:
            root.state("zoomed")              # Windows
        except tk.TclError:
            root.attributes("-zoomed", True)  # Linux

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 2))
        style.configure("Green.TButton", background="#D4EDDA", foreground="#1E5E2E",
                        font=("Segoe UI", 10, "bold"))
        style.map("Green.TButton", background=[("active", "#C3E6CB")])
        style.configure("Red.TButton", background="#E8A0A0", foreground="#5A1010")
        style.map("Red.TButton", background=[("active", "#E08A8A")])

    def _window_group(self, parent):
        frame = tk.Frame(parent, bg=config.WHITE)
        tk.Label(frame, text="Window (ms):", bg=config.WHITE, fg="#555",
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 6))
        spin = ttk.Spinbox(frame, from_=config.WINDOW_MIN_MS, to=config.WINDOW_MAX_MS,
                           increment=config.WINDOW_STEP_MS, width=10,
                           textvariable=self.window_var, command=self.redraw)
        spin.bind("<Return>", lambda e: self.redraw())
        spin.bind("<FocusOut>", lambda e: self.redraw())
        spin.pack(side="left", ipady=3)
        return frame

    def _window_ms(self):
        try:
            value = int(float(self.window_var.get()))
        except ValueError:
            value = config.DEFAULT_WINDOW_MS
        value = max(config.WINDOW_MIN_MS, min(config.WINDOW_MAX_MS, value))
        self.window_var.set(str(value))
        return value

    def _update_status(self):
        if not self.device.is_connected:
            self.status.config(text="Status: Disconnected")
            return
        if self.stream.is_running:
            state = "Recording"
        elif self.stream.has_data():
            state = "Paused"
        else:
            state = "Ready"
        self.status.config(text=f"Status: Connected — {self.device.connected_device} — {state}")
        self.stats.config(text=self.stream.stats_text())

    def _show_connected_layout(self, connected):
        if connected:
            self.window_group1.pack_forget()
            self.row2.pack(fill="x", pady=(0, 4), after=self.row1)
            self.stats.pack(after=self.status)
            self.footer.pack(side="bottom", fill="x", before=self.body)
            self.connect_btn.config(text="Disconnect", style="Red.TButton")
        else:
            self.row2.pack_forget()
            self.stats.pack_forget()
            self.footer.pack_forget()
            self.window_group1.pack(side="left", padx=(6, 0))
            self.connect_btn.config(text="Connect", style="TButton")
            self.start_btn.config(text="Start")

    def redraw(self):
        unit = self.unit_box.get() or config.DEFAULT_UNIT
        window = self._window_ms()
        self.plot.update_plot(self.stream.window_samples(window), window,
                              config.SIGNAL_UNITS[unit])

    def _tick(self):
        """Runs every few milliseconds: reads new samples and refreshes the graph."""
        if self.stream.read_new_samples():
            self.redraw()
            self._update_status()
        self._timer = self.root.after(config.REFRESH_MS, self._tick)

    # ================= button actions =================
    def scan(self):
        self.scan_btn.config(state="disabled")
        self.status.config(text="Status: Scanning for Bluetooth devices...")
        self.root.after(1200, self._scan_done)

    def _scan_done(self):
        devices = self.device.scan()
        self.device_box["values"] = devices
        if not self.device_box.get():
            self.device_box.current(0)
        self.scan_btn.config(state="normal")
        self._update_status()
        messagebox.showinfo("Scan Complete",
                            f"{len(devices)} devices found.\n\n"
                            "Select a device from the list and click 'Connect'.")

    def toggle_connect(self):
        if self.device.is_connected:
            self.stream.pause()
            title, message = self.device.disconnect()
            self._show_connected_layout(False)
            self._update_status()
            messagebox.showinfo(title, message)
            return
        name = self.device_box.get()
        if not name:
            messagebox.showwarning("Select Device", "Please click 'Scan' and select a device first.")
            return
        self.connect_btn.config(state="disabled")
        self.status.config(text=f"Status: Connecting to {name} ...")
        self.root.after(1000, lambda: self._connect_done(name))

    def _connect_done(self, name):
        self.connect_btn.config(state="normal")
        ok, title, message = self.device.connect(name)
        if not ok:
            messagebox.showwarning(title, message)
            self._update_status()
            return
        self._show_connected_layout(True)
        self._update_status()
        messagebox.showinfo(title, message)

    def toggle_start(self):
        if not self.device.is_connected:
            messagebox.showwarning("Not Connected",
                                   "Please connect to a Bluetooth device first.\n\n"
                                   "Click 'Scan', select a device, then click 'Connect'.")
            return
        if self.stream.is_running:
            self.stream.pause()
            self.start_btn.config(text="Start")
        else:
            self.stream.start()
            self.start_btn.config(text="Pause")
        self._update_status()

    def save_csv(self):
        if not self.stream.has_data():
            messagebox.showinfo("No Data", "There is no recorded data yet.\n\n"
                                           "Connect a device and click 'Start' to record.")
            return
        unit = self.unit_box.get() or config.DEFAULT_UNIT
        default_name = f"ppg_recording_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = filedialog.asksaveasfilename(title="Save CSV", defaultextension=".csv",
                                            initialfile=default_name,
                                            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        title, message = self.stream.save_csv(path, unit)
        messagebox.showinfo(title, message)

    def clear(self):
        if not self.stream.has_data():
            messagebox.showinfo("Clear", "The graph is already empty.")
            return
        if messagebox.askyesno("Clear", "Clear all recorded data from the graph?"):
            self.stream.clear()
            self.redraw()
            self._update_status()

    def change_baud(self):
        self.device.set_baud_rate(self.baud_box.get())
        messagebox.showinfo("Baud Rate", f"Baud rate set to {self.baud_box.get()}.")

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.stream.pause()
            if self._timer:
                self.root.after_cancel(self._timer)
            self.on_logout()

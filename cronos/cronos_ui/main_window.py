"""Main Tkinter window for Cronos."""

from __future__ import annotations

import tkinter as tk

from .local_clock_view import LocalClockView


class CronosMainWindow(tk.Tk):
    """Create the focused clock window for Cronos."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Cronos")
        self.geometry("1340x860")
        self.minsize(1180, 760)
        self.configure(bg="#0b1023")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        local_clock_view = LocalClockView(self)
        local_clock_view.grid(row=0, column=0, sticky="nsew")

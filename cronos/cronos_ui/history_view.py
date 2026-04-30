"""History view placeholder for future phases."""

from __future__ import annotations

import tkinter as tk


class HistoryView(tk.Frame):
    """Display the history placeholder screen."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, bg="#f8fafc")
        title_label = tk.Label(
            self,
            text="Historial",
            font=("Helvetica", 24, "bold"),
            fg="#0f172a",
            bg="#f8fafc",
        )
        title_label.pack(anchor="w", padx=28, pady=(28, 12))

        description_label = tk.Label(
            self,
            text="Vista base preparada para el historial.",
            font=("Helvetica", 13),
            fg="#475569",
            bg="#f8fafc",
        )
        description_label.pack(anchor="w", padx=28)

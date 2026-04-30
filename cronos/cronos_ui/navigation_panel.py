"""Navigation panel for the Cronos interface."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable


class NavigationPanel(tk.Frame):
    """Display the main navigation buttons."""

    def __init__(
        self,
        master: tk.Misc,
        on_local_clock_selected: Callable[[], None],
        on_stopwatch_selected: Callable[[], None],
        on_history_selected: Callable[[], None],
    ) -> None:
        super().__init__(master, bg="#111827", width=220)
        self.pack_propagate(False)
        self._build_title()
        self._build_button("Reloj local", on_local_clock_selected)
        self._build_button("Cronómetro", on_stopwatch_selected)
        self._build_button("Historial", on_history_selected)

    def _build_title(self) -> None:
        title_label = tk.Label(
            self,
            text="Cronos",
            font=("Helvetica", 24, "bold"),
            fg="#f8fafc",
            bg="#111827",
        )
        title_label.pack(padx=20, pady=(28, 22), anchor="w")

    def _build_button(self, button_text: str, action: Callable[[], None]) -> None:
        navigation_button = tk.Button(
            self,
            text=button_text,
            command=action,
            font=("Helvetica", 13, "bold"),
            fg="#e5e7eb",
            bg="#1f2937",
            activebackground="#374151",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=12,
        )
        navigation_button.pack(fill="x", padx=20, pady=8)

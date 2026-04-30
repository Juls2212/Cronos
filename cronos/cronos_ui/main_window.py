"""Main Tkinter window for Cronos."""

from __future__ import annotations

import tkinter as tk

from .history_view import HistoryView
from .local_clock_view import LocalClockView
from .navigation_panel import NavigationPanel
from .stopwatch_view import StopwatchView


class CronosMainWindow(tk.Tk):
    """Create the base desktop window and placeholder views."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Cronos")
        self.geometry("1100x750")
        self.minsize(980, 680)
        self.configure(bg="#e5e7eb")

        self._view_container = tk.Frame(self, bg="#e5e7eb")
        self._visible_view: tk.Frame | None = None

        self._build_layout()
        self.show_local_clock_view()

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        navigation_panel = NavigationPanel(
            self,
            on_local_clock_selected=self.show_local_clock_view,
            on_stopwatch_selected=self.show_stopwatch_view,
            on_history_selected=self.show_history_view,
        )
        navigation_panel.grid(row=0, column=0, sticky="nsw")

        self._view_container.grid(row=0, column=1, sticky="nsew")
        self._view_container.columnconfigure(0, weight=1)
        self._view_container.rowconfigure(0, weight=1)

    def show_local_clock_view(self) -> None:
        """Display the local clock placeholder view."""
        self._show_view(LocalClockView)

    def show_stopwatch_view(self) -> None:
        """Display the stopwatch placeholder view."""
        self._show_view(StopwatchView)

    def show_history_view(self) -> None:
        """Display the history placeholder view."""
        self._show_view(HistoryView)

    def _show_view(self, view_type: type[tk.Frame]) -> None:
        if self._visible_view is not None:
            self._visible_view.destroy()

        self._visible_view = view_type(self._view_container)
        self._visible_view.grid(row=0, column=0, sticky="nsew")

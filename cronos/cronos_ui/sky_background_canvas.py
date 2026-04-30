"""Dynamic sky background canvas for Cronos."""

from __future__ import annotations

import tkinter as tk


class SkyBackgroundCanvas(tk.Canvas):
    """Draw the sky according to the current period."""

    def __init__(self, master: tk.Misc, **kwargs: object) -> None:
        super().__init__(master, highlightthickness=0, bd=0, **kwargs)
        self._current_period_name = "day"
        self.bind("<Configure>", self._redraw_background)

    def set_period(self, period_name: str) -> None:
        """Store the active period and redraw the sky."""
        self._current_period_name = period_name
        self._draw_background()

    def _redraw_background(self, _event: tk.Event[tk.Misc]) -> None:
        self._draw_background()

    def _draw_background(self) -> None:
        self.delete("all")
        canvas_width = max(self.winfo_width(), 1)
        canvas_height = max(self.winfo_height(), 1)

        if self._current_period_name == "dawn":
            self._draw_dawn(width=canvas_width, height=canvas_height)
        elif self._current_period_name == "day":
            self._draw_day(width=canvas_width, height=canvas_height)
        elif self._current_period_name == "evening":
            self._draw_evening(width=canvas_width, height=canvas_height)
        else:
            self._draw_night(width=canvas_width, height=canvas_height)

    def _draw_dawn(self, width: int, height: int) -> None:
        self._draw_vertical_bands(
            width=width,
            height=height,
            colors=("#fde68a", "#fdba74", "#f9a8d4", "#dbeafe"),
        )
        self.create_oval(60, 60, 180, 180, fill="#fff7b2", outline="")
        self._draw_cloud(260, 120, "#fef3c7")
        self._draw_cloud(width - 260, 180, "#fef3c7")

    def _draw_day(self, width: int, height: int) -> None:
        self._draw_vertical_bands(
            width=width,
            height=height,
            colors=("#93c5fd", "#7dd3fc", "#bae6fd", "#e0f2fe"),
        )
        self.create_oval(70, 60, 170, 160, fill="#fde047", outline="")
        self._draw_cloud(260, 110, "#eff6ff")
        self._draw_cloud(width - 300, 150, "#eff6ff")
        self._draw_cloud(width - 190, 90, "#f8fafc")

    def _draw_evening(self, width: int, height: int) -> None:
        self._draw_vertical_bands(
            width=width,
            height=height,
            colors=("#fdba74", "#fb7185", "#c084fc", "#7c3aed"),
        )
        self.create_oval(width - 220, height - 220, width - 110, height - 110, fill="#fde68a", outline="")
        self._draw_cloud(220, 130, "#fed7aa")
        self._draw_cloud(width - 320, 210, "#fbcfe8")

    def _draw_night(self, width: int, height: int) -> None:
        self._draw_vertical_bands(
            width=width,
            height=height,
            colors=("#0f172a", "#172554", "#1e293b", "#312e81"),
        )
        self.create_oval(70, 60, 160, 150, fill="#f8fafc", outline="")
        self.create_oval(95, 60, 185, 150, fill="#172554", outline="")

        for star_left, star_top in (
            (220, 90),
            (310, 150),
            (450, 80),
            (590, 140),
            (740, 100),
            (880, 160),
            (width - 140, 80),
        ):
            self.create_oval(
                star_left,
                star_top,
                star_left + 4,
                star_top + 4,
                fill="#f8fafc",
                outline="",
            )

    def _draw_vertical_bands(self, width: int, height: int, colors: tuple[str, ...]) -> None:
        band_height = max(height // len(colors), 1)
        for color_index, color_value in enumerate(colors):
            top_position = color_index * band_height
            lower_position = height if color_index == len(colors) - 1 else top_position + band_height
            self.create_rectangle(0, top_position, width, lower_position, fill=color_value, outline="")

    def _draw_cloud(self, left_position: int, top_position: int, cloud_color: str) -> None:
        self.create_oval(left_position, top_position + 20, left_position + 70, top_position + 70, fill=cloud_color, outline="")
        self.create_oval(left_position + 40, top_position, left_position + 120, top_position + 70, fill=cloud_color, outline="")
        self.create_oval(left_position + 90, top_position + 20, left_position + 160, top_position + 70, fill=cloud_color, outline="")
        self.create_rectangle(left_position + 25, top_position + 35, left_position + 135, top_position + 70, fill=cloud_color, outline="")

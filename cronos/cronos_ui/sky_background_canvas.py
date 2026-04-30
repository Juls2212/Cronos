"""Dynamic sky background canvas for Cronos."""

from __future__ import annotations

import tkinter as tk


class SkyBackgroundCanvas(tk.Canvas):
    """Draw a clean time-of-day background with warm and cool palettes."""

    def __init__(self, master: tk.Misc, **kwargs: object) -> None:
        super().__init__(master, highlightthickness=0, bd=0, **kwargs)
        self._current_period_name = "day"
        self.bind("<Configure>", self._redraw_background)

    def set_period(self, period_name: str) -> None:
        """Store the active period and redraw the background."""
        if period_name == self._current_period_name:
            return
        self._current_period_name = period_name
        self._draw_background()

    def _redraw_background(self, _event: tk.Event[tk.Misc]) -> None:
        self._draw_background()

    def _draw_background(self) -> None:
        self.delete("all")
        canvas_width = max(self.winfo_width(), 1)
        canvas_height = max(self.winfo_height(), 1)

        if self._current_period_name in {"dawn", "day"}:
            palette = {
                "sky": ("#fff8ec", "#fbe7c7", "#dcefff", "#b8ddf8"),
                "orb": "#fde68a",
                "orb_glow": "#fef3c7",
                "curve": "#f6c998",
                "curve_secondary": "#9cc7ef",
                "ridge": "#d8c29b",
                "base": "#f4efe3",
                "cloud": "#fffdf8",
            }
        else:
            palette = {
                "sky": ("#091326", "#13233d", "#1d3557", "#304b77"),
                "orb": "#f8fafc",
                "orb_glow": "#dbeafe",
                "curve": "#4c6fa7",
                "curve_secondary": "#8d7cc8",
                "ridge": "#111c31",
                "base": "#162541",
                "cloud": "#243655",
            }

        self._draw_vertical_gradient(canvas_width, canvas_height, palette["sky"])
        self._draw_soft_orb(canvas_width, canvas_height, palette["orb_glow"], palette["orb"])
        self._draw_curves(canvas_width, canvas_height, palette["curve"], palette["curve_secondary"])
        self._draw_clouds(canvas_width, canvas_height, palette["cloud"])
        self._draw_horizon(canvas_width, canvas_height, palette["ridge"], palette["base"])

    def _draw_vertical_gradient(
        self,
        width: int,
        height: int,
        colors: tuple[str, ...],
    ) -> None:
        stripe_height = max(height // len(colors), 1)
        for color_index, color_value in enumerate(colors):
            top_position = color_index * stripe_height
            lower_position = height if color_index == len(colors) - 1 else top_position + stripe_height
            self.create_rectangle(0, top_position, width, lower_position, fill=color_value, outline="")

    def _draw_soft_orb(
        self,
        width: int,
        height: int,
        glow_color: str,
        orb_color: str,
    ) -> None:
        center_x = int(width * 0.18)
        center_y = int(height * 0.16)
        self.create_oval(
            center_x - 78,
            center_y - 78,
            center_x + 78,
            center_y + 78,
            fill=glow_color,
            outline="",
            stipple="gray50",
        )
        self.create_oval(
            center_x - 48,
            center_y - 48,
            center_x + 48,
            center_y + 48,
            fill=orb_color,
            outline="",
        )

    def _draw_curves(
        self,
        width: int,
        height: int,
        primary_color: str,
        secondary_color: str,
    ) -> None:
        self.create_arc(
            -width * 0.10,
            -height * 0.05,
            width * 0.72,
            height * 0.68,
            start=270,
            extent=110,
            style=tk.ARC,
            outline=primary_color,
            width=2,
        )
        self.create_arc(
            width * 0.28,
            -height * 0.10,
            width * 1.05,
            height * 0.58,
            start=110,
            extent=112,
            style=tk.ARC,
            outline=secondary_color,
            width=2,
        )

    def _draw_clouds(self, width: int, height: int, cloud_color: str) -> None:
        self._draw_cloud(int(width * 0.12), int(height * 0.20), cloud_color, 1.0)
        self._draw_cloud(int(width * 0.40), int(height * 0.28), cloud_color, 1.2)
        self._draw_cloud(int(width * 0.72), int(height * 0.18), cloud_color, 0.9)

    def _draw_cloud(self, left_position: int, top_position: int, cloud_color: str, scale_value: float) -> None:
        self.create_oval(
            left_position,
            top_position + int(18 * scale_value),
            left_position + int(70 * scale_value),
            top_position + int(56 * scale_value),
            fill=cloud_color,
            outline="",
        )
        self.create_oval(
            left_position + int(24 * scale_value),
            top_position,
            left_position + int(96 * scale_value),
            top_position + int(52 * scale_value),
            fill=cloud_color,
            outline="",
        )
        self.create_oval(
            left_position + int(58 * scale_value),
            top_position + int(14 * scale_value),
            left_position + int(130 * scale_value),
            top_position + int(60 * scale_value),
            fill=cloud_color,
            outline="",
        )

    def _draw_horizon(self, width: int, height: int, ridge_color: str, base_color: str) -> None:
        horizon_y = int(height * 0.74)
        self.create_polygon(
            0,
            horizon_y + 24,
            width * 0.14,
            horizon_y - 6,
            width * 0.28,
            horizon_y + 12,
            width * 0.46,
            horizon_y - 14,
            width * 0.64,
            horizon_y + 20,
            width * 0.84,
            horizon_y - 8,
            width,
            horizon_y + 14,
            width,
            height,
            0,
            height,
            fill=ridge_color,
            outline="",
        )
        self.create_rectangle(0, horizon_y + 10, width, height, fill=base_color, outline="")

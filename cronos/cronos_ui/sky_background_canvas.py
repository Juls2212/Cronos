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
                "sky": ("#f8efe1", "#f5dfbf", "#dbeaf5", "#bcd5e8"),
                "orb": "#edc96d",
                "orb_glow": "#f7e6be",
                "curve": "#e3ba79",
                "curve_secondary": "#95b8d1",
                "ridge": "#d7c3a7",
                "base": "#f6efe6",
                "cloud": "#fffaf4",
                "star": "#ffffff",
            }
        else:
            palette = {
                "sky": ("#081221", "#132137", "#1f3350", "#30456a"),
                "orb": "#eef3fd",
                "orb_glow": "#7b8fbd",
                "curve": "#5f76a9",
                "curve_secondary": "#9289bc",
                "ridge": "#111d30",
                "base": "#16253e",
                "cloud": "#23324e",
                "star": "#f7f2ff",
            }

        self._draw_vertical_gradient(canvas_width, canvas_height, palette["sky"])
        self._draw_duality_wash(canvas_width, canvas_height, palette["curve"], palette["curve_secondary"])
        self._draw_soft_orb(canvas_width, canvas_height, palette["orb_glow"], palette["orb"])
        self._draw_curves(canvas_width, canvas_height, palette["curve"], palette["curve_secondary"])
        if self._current_period_name in {"evening", "night"}:
            self._draw_stars(canvas_width, canvas_height, palette["star"])
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
        center_x = int(width * 0.16)
        center_y = int(height * 0.18)
        self.create_oval(
            center_x - 92,
            center_y - 92,
            center_x + 92,
            center_y + 92,
            fill=glow_color,
            outline="",
            stipple="gray50",
        )
        self.create_oval(
            center_x - 52,
            center_y - 52,
            center_x + 52,
            center_y + 52,
            fill=orb_color,
            outline="",
        )

    def _draw_duality_wash(
        self,
        width: int,
        height: int,
        primary_color: str,
        secondary_color: str,
    ) -> None:
        self.create_oval(
            -width * 0.10,
            -height * 0.18,
            width * 0.52,
            height * 0.52,
            fill=primary_color,
            outline="",
            stipple="gray50",
        )
        self.create_oval(
            width * 0.38,
            -height * 0.10,
            width * 1.05,
            height * 0.62,
            fill=secondary_color,
            outline="",
            stipple="gray50",
        )

    def _draw_curves(
        self,
        width: int,
        height: int,
        primary_color: str,
        secondary_color: str,
    ) -> None:
        self.create_arc(
            -width * 0.08,
            -height * 0.08,
            width * 0.82,
            height * 0.78,
            start=270,
            extent=118,
            style=tk.ARC,
            outline=primary_color,
            width=2,
        )
        self.create_arc(
            width * 0.20,
            -height * 0.16,
            width * 1.04,
            height * 0.66,
            start=102,
            extent=126,
            style=tk.ARC,
            outline=secondary_color,
            width=2,
        )
        self.create_arc(
            width * 0.06,
            -height * 0.02,
            width * 0.94,
            height * 0.92,
            start=250,
            extent=60,
            style=tk.ARC,
            outline=secondary_color,
            width=1,
        )

    def _draw_stars(self, width: int, height: int, star_color: str) -> None:
        for horizontal_ratio, vertical_ratio, radius in (
            (0.22, 0.13, 2),
            (0.33, 0.24, 1),
            (0.52, 0.11, 2),
            (0.66, 0.20, 1),
            (0.79, 0.14, 2),
            (0.88, 0.27, 1),
        ):
            center_x = int(width * horizontal_ratio)
            center_y = int(height * vertical_ratio)
            self.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                fill=star_color,
                outline="",
            )

    def _draw_clouds(self, width: int, height: int, cloud_color: str) -> None:
        self._draw_cloud(int(width * 0.10), int(height * 0.22), cloud_color, 0.95)
        self._draw_cloud(int(width * 0.44), int(height * 0.30), cloud_color, 1.05)
        self._draw_cloud(int(width * 0.76), int(height * 0.18), cloud_color, 0.82)

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
        horizon_y = int(height * 0.76)
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

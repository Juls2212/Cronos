"""Analog clock canvas for Cronos."""

from __future__ import annotations

import math
import tkinter as tk


class AnalogClockCanvas(tk.Canvas):
    """Draw a clean analog clock face with a configurable palette."""

    def __init__(
        self,
        master: tk.Misc,
        width: int = 520,
        height: int = 520,
        show_numerals: bool = True,
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg="#f8fafc",
            highlightthickness=0,
            bd=0,
        )
        self._show_numerals = show_numerals
        self._hour_hand_angle = 0.0
        self._minute_hand_angle = 0.0
        self._second_hand_angle = 0.0
        self._palette = {
            "background": "#f7f0e0",
            "outer_shadow": "#d8c6a5",
            "glow": "#fde68a",
            "frame": "#d4a373",
            "face": "#fffdf7",
            "inner_ring": "#f2e8d5",
            "day_face": "#fff6e2",
            "night_face": "#dfeaf6",
            "numeral": "#7c3f00",
            "major_tick": "#b45309",
            "minor_tick": "#cbd5e1",
            "ring_primary": "#d9a857",
            "ring_secondary": "#9eb9d0",
            "hour_hand": "#9a3412",
            "minute_hand": "#2563eb",
            "second_hand": "#ef4444",
            "center_outer": "#7c2d12",
            "center_inner": "#fde68a",
        }
        self._applied_palette_signature = tuple(sorted(self._palette.items()))
        self.bind("<Configure>", self._redraw_clock)

    def configure_visual_theme(self, palette: dict[str, str]) -> None:
        """Apply a new visual palette and redraw the clock."""
        updated_palette = dict(self._palette)
        updated_palette.update(palette)
        updated_signature = tuple(sorted(updated_palette.items()))
        if updated_signature == self._applied_palette_signature:
            return

        self._palette = updated_palette
        self._applied_palette_signature = updated_signature
        self.configure(bg=self._palette["background"])
        self._draw_clock()

    def update_clock_hands(
        self,
        hour_hand_angle: float,
        minute_hand_angle: float,
        second_hand_angle: float,
    ) -> None:
        """Update the displayed hand angles and redraw the clock."""
        self._hour_hand_angle = hour_hand_angle
        self._minute_hand_angle = minute_hand_angle
        self._second_hand_angle = second_hand_angle
        self._draw_clock()

    def _redraw_clock(self, _event: tk.Event[tk.Misc]) -> None:
        self._draw_clock()

    def _draw_clock(self) -> None:
        self.delete("all")
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        if canvas_width <= 1:
            canvas_width = int(self.cget("width"))
        if canvas_height <= 1:
            canvas_height = int(self.cget("height"))

        center_x = canvas_width / 2
        center_y = canvas_height / 2

        minimum_dimension = min(canvas_width, canvas_height)
        safe_margin = max(minimum_dimension * 0.14, 36)
        outer_glow_extension = safe_margin * 0.08
        outer_shadow_horizontal_extension = safe_margin * 0.14
        outer_shadow_top_extension = safe_margin * 0.08
        outer_shadow_bottom_extension = safe_margin * 0.18
        maximum_outer_extension = max(
            outer_glow_extension,
            outer_shadow_horizontal_extension,
            outer_shadow_top_extension,
            outer_shadow_bottom_extension,
        )
        radius = max(minimum_dimension / 2 - safe_margin - maximum_outer_extension, 42)
        inner_face_inset = max(radius * 0.045, 10)

        self.create_oval(
            center_x - radius - outer_shadow_horizontal_extension,
            center_y - radius - outer_shadow_top_extension,
            center_x + radius + outer_shadow_horizontal_extension,
            center_y + radius + outer_shadow_bottom_extension,
            fill=self._palette["outer_shadow"],
            outline="",
        )
        self.create_oval(
            center_x - radius - outer_glow_extension,
            center_y - radius - outer_glow_extension,
            center_x + radius + outer_glow_extension,
            center_y + radius + outer_glow_extension,
            fill=self._palette["glow"],
            outline="",
            stipple="gray50",
        )
        self.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill=self._palette["frame"],
            outline="",
        )
        self.create_oval(
            center_x - radius + inner_face_inset * 0.28,
            center_y - radius + inner_face_inset * 0.28,
            center_x + radius - inner_face_inset * 0.28,
            center_y + radius - inner_face_inset * 0.28,
            outline=self._palette["ring_primary"],
            width=2,
        )
        self.create_oval(
            center_x - radius + inner_face_inset,
            center_y - radius + inner_face_inset,
            center_x + radius - inner_face_inset,
            center_y + radius - inner_face_inset,
            fill=self._palette["face"],
            outline=self._palette["inner_ring"],
            width=3,
        )
        self._draw_duality_face(
            center_x=center_x,
            center_y=center_y,
            radius=radius - inner_face_inset - 6,
        )

        self._draw_ticks(center_x=center_x, center_y=center_y, radius=radius)
        if self._show_numerals:
            self._draw_numerals(center_x=center_x, center_y=center_y, radius=radius)
        self._draw_hand(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.48,
            angle=self._hour_hand_angle,
            color=self._palette["hour_hand"],
            width=8 if self._show_numerals else 5,
        )
        self._draw_hand(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.68,
            angle=self._minute_hand_angle,
            color=self._palette["minute_hand"],
            width=5 if self._show_numerals else 3,
        )
        self._draw_second_hand(center_x=center_x, center_y=center_y, radius=radius * 0.80)
        self.create_oval(
            center_x - 11,
            center_y - 11,
            center_x + 11,
            center_y + 11,
            fill=self._palette["center_outer"],
            outline="",
        )
        self.create_oval(
            center_x - 4,
            center_y - 4,
            center_x + 4,
            center_y + 4,
            fill=self._palette["center_inner"],
            outline="",
        )

    def _draw_duality_face(self, center_x: float, center_y: float, radius: float) -> None:
        self.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=90,
            extent=180,
            fill=self._palette["day_face"],
            outline="",
        )
        self.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=270,
            extent=180,
            fill=self._palette["night_face"],
            outline="",
        )

        flow_radius = radius * 0.50
        flow_offset = radius * 0.25
        small_orb_radius = max(radius * 0.10, 10)
        sun_center_x = center_x
        sun_center_y = center_y - flow_offset
        moon_center_x = center_x
        moon_center_y = center_y + flow_offset

        self.create_oval(
            center_x - flow_radius,
            center_y - radius * 0.88,
            center_x + flow_radius,
            center_y + radius * 0.12,
            fill=self._palette["day_face"],
            outline="",
        )
        self.create_oval(
            center_x - flow_radius,
            center_y - radius * 0.12,
            center_x + flow_radius,
            center_y + radius * 0.88,
            fill=self._palette["night_face"],
            outline="",
        )
        self.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=90,
            extent=180,
            style=tk.ARC,
            outline=self._palette["ring_primary"],
            width=2,
        )
        self.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=270,
            extent=180,
            style=tk.ARC,
            outline=self._palette["ring_secondary"],
            width=2,
        )
        self.create_oval(
            sun_center_x - small_orb_radius,
            sun_center_y - small_orb_radius,
            sun_center_x + small_orb_radius,
            sun_center_y + small_orb_radius,
            fill=self._palette["night_face"],
            outline="",
        )
        self.create_oval(
            moon_center_x - small_orb_radius,
            moon_center_y - small_orb_radius,
            moon_center_x + small_orb_radius,
            moon_center_y + small_orb_radius,
            fill=self._palette["day_face"],
            outline="",
        )
        self.create_arc(
            moon_center_x - small_orb_radius * 0.9,
            moon_center_y - small_orb_radius * 0.9,
            moon_center_x + small_orb_radius * 0.9,
            moon_center_y + small_orb_radius * 0.9,
            start=300,
            extent=150,
            style=tk.ARC,
            outline=self._palette["ring_primary"],
            width=2,
        )
        self.create_oval(
            sun_center_x - small_orb_radius * 0.36,
            sun_center_y - small_orb_radius * 0.36,
            sun_center_x + small_orb_radius * 0.36,
            sun_center_y + small_orb_radius * 0.36,
            fill=self._palette["ring_primary"],
            outline="",
        )
        self.create_oval(
            center_x - radius * 0.92,
            center_y - radius * 0.92,
            center_x + radius * 0.92,
            center_y + radius * 0.92,
            outline=self._palette["ring_secondary"],
            width=1,
        )

    def _draw_ticks(self, center_x: float, center_y: float, radius: float) -> None:
        outer_tick_radius = radius - max(radius * 0.04, 10)
        major_tick_inner_radius = radius - max(radius * 0.15, 30)
        minor_tick_inner_radius = radius - max(radius * 0.09, 18)
        for position_number in range(60):
            outer_x, outer_y = self._angle_to_point(
                center_x=center_x,
                center_y=center_y,
                radius=outer_tick_radius,
                angle=position_number * 6,
            )
            inner_radius = (
                major_tick_inner_radius
                if position_number % 5 == 0
                else minor_tick_inner_radius
            )
            inner_x, inner_y = self._angle_to_point(
                center_x=center_x,
                center_y=center_y,
                radius=inner_radius,
                angle=position_number * 6,
            )
            self.create_line(
                inner_x,
                inner_y,
                outer_x,
                outer_y,
                fill=(
                    self._palette["major_tick"]
                    if position_number % 5 == 0
                    else self._palette["minor_tick"]
                ),
                width=3 if position_number % 5 == 0 else 1,
            )

    def _draw_numerals(self, center_x: float, center_y: float, radius: float) -> None:
        numeral_radius = radius - max(radius * 0.20, 46)
        for numeral_value in range(1, 13):
            numeral_x, numeral_y = self._angle_to_point(
                center_x=center_x,
                center_y=center_y,
                radius=numeral_radius,
                angle=numeral_value * 30,
            )
            self.create_text(
                numeral_x,
                numeral_y,
                text=str(numeral_value),
                fill=self._palette["numeral"],
                font=("Georgia", max(11, int(radius * 0.085)), "bold"),
            )

    def _draw_hand(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        angle: float,
        color: str,
        width: int,
    ) -> None:
        end_x, end_y = self._angle_to_point(
            center_x=center_x,
            center_y=center_y,
            radius=radius,
            angle=angle,
        )
        self.create_line(
            center_x,
            center_y,
            end_x,
            end_y,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
        )

    def _draw_second_hand(self, center_x: float, center_y: float, radius: float) -> None:
        end_x, end_y = self._angle_to_point(
            center_x=center_x,
            center_y=center_y,
            radius=radius,
            angle=self._second_hand_angle,
        )
        tail_x, tail_y = self._angle_to_point(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.18,
            angle=self._second_hand_angle + 180,
        )
        self.create_line(
            tail_x,
            tail_y,
            end_x,
            end_y,
            fill=self._palette["second_hand"],
            width=2,
            capstyle=tk.ROUND,
        )

    def _angle_to_point(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        angle: float,
    ) -> tuple[float, float]:
        angle_in_radians = math.radians(angle - 90)
        horizontal_position = center_x + radius * math.cos(angle_in_radians)
        vertical_position = center_y + radius * math.sin(angle_in_radians)
        return horizontal_position, vertical_position

"""Analog clock canvas for Cronos."""

from __future__ import annotations

import math
import tkinter as tk


class AnalogClockCanvas(tk.Canvas):
    """Draw an analog clock face with animated hands."""

    def __init__(
        self,
        master: tk.Misc,
        width: int = 520,
        height: int = 520,
        face_fill_color: str = "#f8fafc",
        border_color: str = "#0f172a",
        numeral_color: str = "#0f172a",
        hand_color: str = "#0f172a",
        minute_hand_color: str = "#1d4ed8",
        second_hand_color: str = "#dc2626",
        background_color: str = "#dbeafe",
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            bg=background_color,
            highlightthickness=0,
            bd=0,
        )
        self._face_fill_color = face_fill_color
        self._border_color = border_color
        self._numeral_color = numeral_color
        self._hand_color = hand_color
        self._minute_hand_color = minute_hand_color
        self._second_hand_color = second_hand_color
        self._hour_hand_angle = 0.0
        self._minute_hand_angle = 0.0
        self._second_hand_angle = 0.0
        self.bind("<Configure>", self._redraw_clock)

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
        canvas_width = max(self.winfo_width(), int(self.cget("width")))
        canvas_height = max(self.winfo_height(), int(self.cget("height")))
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        radius = min(canvas_width, canvas_height) / 2 - 24

        self.create_oval(
            center_x - radius - 6,
            center_y - radius - 6,
            center_x + radius + 6,
            center_y + radius + 6,
            fill="#cbd5e1",
            outline="",
        )
        self.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill=self._face_fill_color,
            outline=self._border_color,
            width=5,
        )
        self.create_oval(
            center_x - radius + 10,
            center_y - radius + 10,
            center_x + radius - 10,
            center_y + radius - 10,
            outline="#94a3b8",
            width=2,
        )

        self._draw_hour_marks(center_x=center_x, center_y=center_y, radius=radius)
        self._draw_numerals(center_x=center_x, center_y=center_y, radius=radius)
        self._draw_hand(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.50,
            angle=self._hour_hand_angle,
            color=self._hand_color,
            width=8,
        )
        self._draw_hand(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.72,
            angle=self._minute_hand_angle,
            color=self._minute_hand_color,
            width=5,
        )
        self._draw_hand(
            center_x=center_x,
            center_y=center_y,
            radius=radius * 0.82,
            angle=self._second_hand_angle,
            color=self._second_hand_color,
            width=2,
        )
        self.create_oval(
            center_x - 9,
            center_y - 9,
            center_x + 9,
            center_y + 9,
            fill=self._border_color,
            outline="",
        )
        self.create_oval(
            center_x - 4,
            center_y - 4,
            center_x + 4,
            center_y + 4,
            fill="#f8fafc",
            outline="",
        )

    def _draw_hour_marks(self, center_x: float, center_y: float, radius: float) -> None:
        for position_number in range(60):
            outer_x, outer_y = self._angle_to_point(
                center_x=center_x,
                center_y=center_y,
                radius=radius - 14,
                angle=position_number * 6,
            )
            inner_radius = radius - 42 if position_number % 5 == 0 else radius - 28
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
                fill="#475569" if position_number % 5 == 0 else "#94a3b8",
                width=3 if position_number % 5 == 0 else 1,
            )

    def _draw_numerals(self, center_x: float, center_y: float, radius: float) -> None:
        for numeral_value in range(1, 13):
            numeral_x, numeral_y = self._angle_to_point(
                center_x=center_x,
                center_y=center_y,
                radius=radius - 65,
                angle=numeral_value * 30,
            )
            self.create_text(
                numeral_x,
                numeral_y,
                text=str(numeral_value),
                fill=self._numeral_color,
                font=("Helvetica", max(12, int(radius * 0.09)), "bold"),
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

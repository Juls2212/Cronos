"""Local time clock service for Cronos."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from .circular_doubly_linked_sequence import CircularDoublyLinkedSequence


class LocalTimeClockService:
    """Provide real local time snapshots backed by circular sequences."""

    def __init__(
        self,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self._now_provider = now_provider or datetime.now
        self._hour_sequence = self._build_numeric_sequence(24)
        self._minute_sequence = self._build_numeric_sequence(60)
        self._second_sequence = self._build_numeric_sequence(60)
        self._current_snapshot = self._build_snapshot(hour=0, minute=0, second=0)
        self.refresh_from_system_time()

    def refresh_from_system_time(self) -> dict[str, float | int | str]:
        """Read system time and align the circular selections."""
        current_time = self._now_provider()
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second

        self._hour_sequence.select_value(current_hour)
        self._minute_sequence.select_value(current_minute)
        self._second_sequence.select_value(current_second)

        self._current_snapshot = self._build_snapshot(
            hour=current_hour,
            minute=current_minute,
            second=current_second,
        )
        return dict(self._current_snapshot)

    def get_current_local_time_snapshot(self) -> dict[str, float | int | str]:
        """Return the most recent local time snapshot."""
        return dict(self._current_snapshot)

    def get_current_hand_angles(self) -> dict[str, float]:
        """Return the current analog hand angles."""
        return {
            "second_hand_angle": float(self._current_snapshot["second_hand_angle"]),
            "minute_hand_angle": float(self._current_snapshot["minute_hand_angle"]),
            "hour_hand_angle": float(self._current_snapshot["hour_hand_angle"]),
        }

    def get_formatted_time(self, use_24_hour_format: bool = True) -> str:
        """Return the current time in the requested digital format."""
        if use_24_hour_format:
            return str(self._current_snapshot["formatted_24_hour_time"])
        return str(self._current_snapshot["formatted_12_hour_time"])

    def get_milliseconds_until_next_second(self) -> int:
        """Return the delay needed to align the next repaint with real time."""
        current_time = self._now_provider()
        milliseconds_until_next_second = 1000 - int(current_time.microsecond / 1000)
        if milliseconds_until_next_second <= 0:
            return 1
        return milliseconds_until_next_second

    def _build_numeric_sequence(self, size: int) -> CircularDoublyLinkedSequence[int]:
        numeric_sequence = CircularDoublyLinkedSequence[int]()
        for numeric_value in range(size):
            numeric_sequence.append_value(numeric_value)
        return numeric_sequence

    def _build_snapshot(self, hour: int, minute: int, second: int) -> dict[str, float | int | str]:
        second_hand_angle = second * 6
        minute_hand_angle = minute * 6 + second * 0.1
        hour_hand_angle = (hour % 12) * 30 + minute * 0.5

        hour_in_12_format = hour % 12
        if hour_in_12_format == 0:
            hour_in_12_format = 12

        meridiem_label = "AM" if hour < 12 else "PM"

        return {
            "hour": hour,
            "minute": minute,
            "second": second,
            "formatted_24_hour_time": f"{hour:02d}:{minute:02d}:{second:02d}",
            "formatted_12_hour_time": (
                f"{hour_in_12_format:02d}:{minute:02d}:{second:02d} {meridiem_label}"
            ),
            "second_hand_angle": float(second_hand_angle),
            "minute_hand_angle": float(minute_hand_angle),
            "hour_hand_angle": float(hour_hand_angle),
        }

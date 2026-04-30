"""Theme period service for Cronos."""

from __future__ import annotations

from .circular_doubly_linked_sequence import CircularDoublyLinkedSequence


class ThemePeriodService:
    """Determine the current visual sky period through a circular cycle."""

    def __init__(self) -> None:
        self._period_sequence = CircularDoublyLinkedSequence[str]()
        for period_name in ("dawn", "day", "evening", "night"):
            self._period_sequence.append_value(period_name)
        self._period_sequence.select_value("day")

    def get_period_for_hour(self, hour: int) -> str:
        """Return the correct period for a 24-hour clock value."""
        normalized_hour = hour % 24

        if 5 <= normalized_hour <= 7:
            period_name = "dawn"
        elif 8 <= normalized_hour <= 16:
            period_name = "day"
        elif 17 <= normalized_hour <= 19:
            period_name = "evening"
        else:
            period_name = "night"

        self._period_sequence.select_value(period_name)
        selected_period = self._period_sequence.get_selected_value()
        if selected_period is None:
            raise RuntimeError("Theme period selection failed.")
        return selected_period

    def get_period_cycle_snapshot(self) -> list[str]:
        """Return the configured period cycle."""
        return self._period_sequence.get_values_snapshot()

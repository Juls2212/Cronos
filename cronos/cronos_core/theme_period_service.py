"""Theme period service for Cronos."""

from __future__ import annotations

from .circular_doubly_linked_sequence import CircularDoublyLinkedSequence


class ThemePeriodService:
    """Determine visual periods and palettes through a circular cycle."""

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

    def get_theme_mode_for_hour(self, hour: int) -> str:
        """Return whether the hour belongs to a warm or cool theme mode."""
        period_name = self.get_period_for_hour(hour)
        if period_name in {"dawn", "day"}:
            return "warm"
        return "cool"

    def get_local_view_palette(self, hour: int) -> dict[str, str]:
        """Return the main local screen palette for the provided hour."""
        period_name = self.get_period_for_hour(hour)

        if period_name == "dawn":
            return {
                "window_background": "#f7ead7",
                "hero_shell": "#d7b98b",
                "hero_panel": "#fff7ed",
                "hero_stage": "#f4dfc1",
                "title": "#7c2d12",
                "subtitle": "#b45309",
                "digital_time": "#78350f",
                "toggle_shell": "#e9d5b5",
                "toggle_panel": "#fff7ed",
                "toggle_inactive_text": "#7c2d12",
                "toggle_active_fill": "#fbbf24",
                "toggle_active_text": "#431407",
                "clock_background": "#f6ead7",
                "clock_face": "#fff8ee",
                "clock_border": "#d97706",
                "clock_numeral": "#78350f",
                "clock_hour_hand": "#92400e",
                "clock_minute_hand": "#ea580c",
                "clock_second_hand": "#ef4444",
                "clock_glow": "#fde68a",
                "world_panel_shell": "#d7b98b",
                "world_panel_background": "#fff7ed",
            }
        if period_name == "day":
            return {
                "window_background": "#e9f4ff",
                "hero_shell": "#bfd8ee",
                "hero_panel": "#fffdf8",
                "hero_stage": "#f8f1e3",
                "title": "#155e75",
                "subtitle": "#ca8a04",
                "digital_time": "#164e63",
                "toggle_shell": "#dbeafe",
                "toggle_panel": "#f8fafc",
                "toggle_inactive_text": "#1e3a8a",
                "toggle_active_fill": "#fcd34d",
                "toggle_active_text": "#1f2937",
                "clock_background": "#f7f0e0",
                "clock_face": "#fffdf7",
                "clock_border": "#d4a373",
                "clock_numeral": "#7c3f00",
                "clock_hour_hand": "#9a3412",
                "clock_minute_hand": "#2563eb",
                "clock_second_hand": "#ef4444",
                "clock_glow": "#fef3c7",
                "world_panel_shell": "#bfd8ee",
                "world_panel_background": "#fffdf8",
            }
        if period_name == "evening":
            return {
                "window_background": "#21123c",
                "hero_shell": "#4c2a85",
                "hero_panel": "#2f1e55",
                "hero_stage": "#3b275f",
                "title": "#fde68a",
                "subtitle": "#f9a8d4",
                "digital_time": "#fff7ed",
                "toggle_shell": "#43326d",
                "toggle_panel": "#2f1e55",
                "toggle_inactive_text": "#f5d0fe",
                "toggle_active_fill": "#fb923c",
                "toggle_active_text": "#2c1206",
                "clock_background": "#38255f",
                "clock_face": "#fff7ed",
                "clock_border": "#f59e0b",
                "clock_numeral": "#5b210a",
                "clock_hour_hand": "#6d28d9",
                "clock_minute_hand": "#f97316",
                "clock_second_hand": "#fb7185",
                "clock_glow": "#c084fc",
                "world_panel_shell": "#4c2a85",
                "world_panel_background": "#2f1e55",
            }

        return {
            "window_background": "#071224",
            "hero_shell": "#162541",
            "hero_panel": "#0f1b32",
            "hero_stage": "#12213b",
            "title": "#f8fafc",
            "subtitle": "#c4b5fd",
            "digital_time": "#e2e8f0",
            "toggle_shell": "#1d2d4a",
            "toggle_panel": "#10203b",
            "toggle_inactive_text": "#dbeafe",
            "toggle_active_fill": "#93c5fd",
            "toggle_active_text": "#0f172a",
            "clock_background": "#0f1b32",
            "clock_face": "#f8fafc",
            "clock_border": "#c4b5fd",
            "clock_numeral": "#1e1b4b",
            "clock_hour_hand": "#0f172a",
            "clock_minute_hand": "#2563eb",
            "clock_second_hand": "#f472b6",
            "clock_glow": "#1d4ed8",
            "world_panel_shell": "#162541",
            "world_panel_background": "#0f1b32",
        }

    def get_world_clock_palette(self, hour: int) -> dict[str, str]:
        """Return a smaller card palette for a specific timezone hour."""
        theme_mode = self.get_theme_mode_for_hour(hour)

        if theme_mode == "warm":
            return {
                "card_shell": "#d3b58a",
                "card_background": "#fff8ec",
                "title": "#92400e",
                "digital_time": "#78350f",
                "remove_fill": "#c2410c",
                "remove_text": "#fff7ed",
                "accent_primary": "#f59e0b",
                "accent_secondary": "#fb7185",
                "clock_background": "#f8ebd0",
                "clock_face": "#fffdf8",
                "clock_border": "#d97706",
                "clock_numeral": "#78350f",
                "clock_hour_hand": "#9a3412",
                "clock_minute_hand": "#ea580c",
                "clock_second_hand": "#ef4444",
                "clock_glow": "#fde68a",
            }

        return {
            "card_shell": "#22355a",
            "card_background": "#11213b",
            "title": "#f8fafc",
            "digital_time": "#dbeafe",
            "remove_fill": "#7c2d12",
            "remove_text": "#fff7ed",
            "accent_primary": "#93c5fd",
            "accent_secondary": "#d8b4fe",
            "clock_background": "#13233d",
            "clock_face": "#f8fafc",
            "clock_border": "#c4b5fd",
            "clock_numeral": "#1e1b4b",
            "clock_hour_hand": "#0f172a",
            "clock_minute_hand": "#2563eb",
            "clock_second_hand": "#f472b6",
            "clock_glow": "#1d4ed8",
        }

    def get_period_cycle_snapshot(self) -> list[str]:
        """Return the configured period cycle."""
        return self._period_sequence.get_values_snapshot()

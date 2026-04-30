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
                "window_background": "#f7efe0",
                "hero_shell": "#d7c0a1",
                "hero_panel": "#fffaf2",
                "hero_stage": "#f4e5cd",
                "title": "#6f3c19",
                "subtitle": "#b0672d",
                "digital_time": "#7a4320",
                "toggle_shell": "#e8d9bf",
                "toggle_panel": "#fff8ef",
                "toggle_inactive_text": "#7a4320",
                "toggle_active_fill": "#f0c56d",
                "toggle_active_text": "#49230f",
                "clock_background": "#f7eddc",
                "clock_face": "#fff9f1",
                "clock_border": "#d2a66d",
                "clock_numeral": "#6d4423",
                "clock_hour_hand": "#8b4a1e",
                "clock_minute_hand": "#da8a4b",
                "clock_second_hand": "#de5f6f",
                "clock_glow": "#f6d8a2",
                "clock_day_face": "#fff7ea",
                "clock_night_face": "#d8e7f4",
                "clock_ring_primary": "#e1b15f",
                "clock_ring_secondary": "#90b8d8",
                "world_panel_shell": "#d7c0a1",
                "world_panel_background": "#fffaf2",
            }
        if period_name == "day":
            return {
                "window_background": "#e8f1f8",
                "hero_shell": "#b5c8d9",
                "hero_panel": "#fffaf3",
                "hero_stage": "#f6ecdb",
                "title": "#204f67",
                "subtitle": "#af7d2f",
                "digital_time": "#31556b",
                "toggle_shell": "#d7e2eb",
                "toggle_panel": "#f8faf8",
                "toggle_inactive_text": "#355168",
                "toggle_active_fill": "#efc768",
                "toggle_active_text": "#2b261c",
                "clock_background": "#f3ecdf",
                "clock_face": "#fffdf8",
                "clock_border": "#cfa979",
                "clock_numeral": "#6b4526",
                "clock_hour_hand": "#7f4a2b",
                "clock_minute_hand": "#5b8eb4",
                "clock_second_hand": "#d96872",
                "clock_glow": "#f4dfae",
                "clock_day_face": "#fff8e8",
                "clock_night_face": "#d7e6f0",
                "clock_ring_primary": "#ddb15f",
                "clock_ring_secondary": "#9ebdd4",
                "world_panel_shell": "#b5c8d9",
                "world_panel_background": "#fffaf3",
            }
        if period_name == "evening":
            return {
                "window_background": "#211934",
                "hero_shell": "#4d3f71",
                "hero_panel": "#2d2444",
                "hero_stage": "#382d54",
                "title": "#f3dfb1",
                "subtitle": "#d5a6c8",
                "digital_time": "#f4ecfb",
                "toggle_shell": "#473a67",
                "toggle_panel": "#2e2547",
                "toggle_inactive_text": "#e3d8f3",
                "toggle_active_fill": "#dca76c",
                "toggle_active_text": "#251608",
                "clock_background": "#312748",
                "clock_face": "#fbf4ed",
                "clock_border": "#c89a67",
                "clock_numeral": "#513334",
                "clock_hour_hand": "#50327b",
                "clock_minute_hand": "#d78d54",
                "clock_second_hand": "#e2879a",
                "clock_glow": "#8f7ab5",
                "clock_day_face": "#f8e5cc",
                "clock_night_face": "#cec7ea",
                "clock_ring_primary": "#d7a363",
                "clock_ring_secondary": "#9e8dd0",
                "world_panel_shell": "#4d3f71",
                "world_panel_background": "#2d2444",
            }

        return {
            "window_background": "#081221",
            "hero_shell": "#1b2940",
            "hero_panel": "#101b2e",
            "hero_stage": "#13213a",
            "title": "#f4f6fb",
            "subtitle": "#bfb8de",
            "digital_time": "#dbe6f0",
            "toggle_shell": "#21314c",
            "toggle_panel": "#13223a",
            "toggle_inactive_text": "#dce7f5",
            "toggle_active_fill": "#91add6",
            "toggle_active_text": "#10151f",
            "clock_background": "#0f1c31",
            "clock_face": "#f6f7fb",
            "clock_border": "#94a2c9",
            "clock_numeral": "#26304e",
            "clock_hour_hand": "#20283b",
            "clock_minute_hand": "#5e7db7",
            "clock_second_hand": "#d78baa",
            "clock_glow": "#2a426d",
            "clock_day_face": "#f0dfba",
            "clock_night_face": "#dce3f7",
            "clock_ring_primary": "#ccb076",
            "clock_ring_secondary": "#8d9dcc",
            "world_panel_shell": "#1b2940",
            "world_panel_background": "#101b2e",
        }

    def get_world_clock_palette(self, hour: int) -> dict[str, str]:
        """Return a smaller card palette for a specific timezone hour."""
        theme_mode = self.get_theme_mode_for_hour(hour)

        if theme_mode == "warm":
            return {
                "card_shell": "#d6c0a3",
                "card_background": "#fff9f0",
                "title": "#7a4a28",
                "digital_time": "#82502b",
                "remove_fill": "#d79b68",
                "remove_text": "#412111",
                "accent_primary": "#d8ad68",
                "accent_secondary": "#95b8d1",
                "clock_background": "#f7ecdd",
                "clock_face": "#fffdf8",
                "clock_border": "#d0aa7a",
                "clock_numeral": "#71462a",
                "clock_hour_hand": "#865133",
                "clock_minute_hand": "#c48a5f",
                "clock_second_hand": "#d9717d",
                "clock_glow": "#f2d9a4",
                "clock_day_face": "#fff7e9",
                "clock_night_face": "#dbe7ef",
                "clock_ring_primary": "#ddb068",
                "clock_ring_secondary": "#9abed5",
            }

        return {
            "card_shell": "#24344f",
            "card_background": "#122036",
            "title": "#eef2f8",
            "digital_time": "#d6e0ec",
            "remove_fill": "#7f8fb0",
            "remove_text": "#0e1522",
            "accent_primary": "#c8b07b",
            "accent_secondary": "#8da1cf",
            "clock_background": "#13233b",
            "clock_face": "#f8fafc",
            "clock_border": "#92a3cb",
            "clock_numeral": "#33405b",
            "clock_hour_hand": "#202a3f",
            "clock_minute_hand": "#6f88bc",
            "clock_second_hand": "#d791a9",
            "clock_glow": "#2c456d",
            "clock_day_face": "#ecdfbf",
            "clock_night_face": "#dde4f6",
            "clock_ring_primary": "#cdb17a",
            "clock_ring_secondary": "#90a1cd",
        }

    def get_period_cycle_snapshot(self) -> list[str]:
        """Return the configured period cycle."""
        return self._period_sequence.get_values_snapshot()

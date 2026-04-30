"""World clock service for Cronos."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable
import unicodedata

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - fallback for older Python environments
    ZoneInfo = None  # type: ignore[assignment]

    class ZoneInfoNotFoundError(Exception):
        """Fallback exception when zoneinfo is unavailable."""

from .theme_period_service import ThemePeriodService


@dataclass(frozen=True, slots=True)
class WorldClockDefinition:
    """Describe a world clock option."""

    city_name: str
    time_zone_name: str


class WorldClockService:
    """Maintain user-selected world clocks and generate live snapshots."""

    def __init__(
        self,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self._now_provider = now_provider or datetime.now
        self._theme_period_service = ThemePeriodService()
        self._available_clock_definitions = self._build_available_clock_definitions()
        self._selected_clock_definitions: dict[str, WorldClockDefinition] = {}

    def get_available_time_zones(self) -> list[dict[str, str]]:
        """Return the supported city and time zone options."""
        return [
            {
                "city_name": definition.city_name,
                "time_zone_name": definition.time_zone_name,
            }
            for definition in self._available_clock_definitions.values()
        ]

    def add_world_clock(self, city_name: str) -> bool:
        """Add a supported world clock if it is not already selected."""
        normalized_city_name = self._normalize_city_name(city_name)
        selected_definition = self._find_definition_by_city_name(normalized_city_name)
        if selected_definition is None:
            return False

        if selected_definition.city_name in self._selected_clock_definitions:
            return False

        self._selected_clock_definitions[selected_definition.city_name] = selected_definition
        return True

    def remove_world_clock(self, city_name: str) -> bool:
        """Remove a previously selected world clock."""
        normalized_city_name = self._normalize_city_name(city_name)
        selected_definition = self._find_definition_by_city_name(normalized_city_name)
        if selected_definition is None:
            return False

        if selected_definition.city_name not in self._selected_clock_definitions:
            return False

        del self._selected_clock_definitions[selected_definition.city_name]
        return True

    def get_world_clock_snapshots(self) -> list[dict[str, float | int | str]]:
        """Return current time snapshots for all selected world clocks."""
        if ZoneInfo is None:
            return []

        current_time = self._resolve_current_time()
        world_clock_snapshots: list[dict[str, float | int | str]] = []

        for definition in self._selected_clock_definitions.values():
            zone_information = ZoneInfo(definition.time_zone_name)
            zoned_time = current_time.astimezone(zone_information)

            hour_value = zoned_time.hour
            minute_value = zoned_time.minute
            second_value = zoned_time.second
            hour_in_12_format = hour_value % 12 or 12
            meridiem_label = "AM" if hour_value < 12 else "PM"
            visual_period = self._theme_period_service.get_period_for_hour(hour_value)
            theme_mode = self._theme_period_service.get_theme_mode_for_hour(hour_value)

            world_clock_snapshots.append(
                {
                    "city_name": definition.city_name,
                    "time_zone_name": definition.time_zone_name,
                    "hour": hour_value,
                    "minute": minute_value,
                    "second": second_value,
                    "visual_period": visual_period,
                    "theme_mode": theme_mode,
                    "formatted_24_hour_time": (
                        f"{hour_value:02d}:{minute_value:02d}:{second_value:02d}"
                    ),
                    "formatted_12_hour_time": (
                        f"{hour_in_12_format:02d}:{minute_value:02d}:{second_value:02d} "
                        f"{meridiem_label}"
                    ),
                    "second_hand_angle": float(second_value * 6),
                    "minute_hand_angle": float(minute_value * 6 + second_value * 0.1),
                    "hour_hand_angle": float((hour_value % 12) * 30 + minute_value * 0.5),
                }
            )

        return world_clock_snapshots

    def _build_available_clock_definitions(self) -> dict[str, WorldClockDefinition]:
        city_pairs = (
            ("Londres", "Europe/London"),
            ("Nueva York", "America/New_York"),
            ("Madrid", "Europe/Madrid"),
            ("Tokio", "Asia/Tokyo"),
            ("Par\u00eds", "Europe/Paris"),
            ("Ciudad de M\u00e9xico", "America/Mexico_City"),
            ("Buenos Aires", "America/Argentina/Buenos_Aires"),
        )

        available_clock_definitions: dict[str, WorldClockDefinition] = {}
        for city_name, time_zone_name in city_pairs:
            if ZoneInfo is None:
                break
            try:
                ZoneInfo(time_zone_name)
            except ZoneInfoNotFoundError:
                continue

            available_clock_definitions[self._normalize_city_name(city_name)] = WorldClockDefinition(
                city_name=city_name,
                time_zone_name=time_zone_name,
            )

        return available_clock_definitions

    def _find_definition_by_city_name(self, city_name: str) -> WorldClockDefinition | None:
        return self._available_clock_definitions.get(self._normalize_city_name(city_name))

    def _normalize_city_name(self, city_name: str) -> str:
        compact_city_name = " ".join(city_name.split())
        normalized_city_name = unicodedata.normalize("NFC", compact_city_name)
        return normalized_city_name.casefold()

    def _resolve_current_time(self) -> datetime:
        current_time = self._now_provider()
        if current_time.tzinfo is None:
            return current_time.astimezone()
        return current_time

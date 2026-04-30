"""Tests for the local time clock service."""

from datetime import datetime

from cronos_core.local_time_clock_service import LocalTimeClockService


def test_refresh_from_system_time_selects_matching_values() -> None:
    fixed_time = datetime(2026, 4, 29, 18, 37, 42)
    local_time_clock_service = LocalTimeClockService(now_provider=lambda: fixed_time)

    current_snapshot = local_time_clock_service.refresh_from_system_time()

    assert current_snapshot["hour"] == 18
    assert current_snapshot["minute"] == 37
    assert current_snapshot["second"] == 42
    assert local_time_clock_service._hour_sequence.get_selected_value() == 18
    assert local_time_clock_service._minute_sequence.get_selected_value() == 37
    assert local_time_clock_service._second_sequence.get_selected_value() == 42


def test_get_current_local_time_snapshot_contains_expected_fields() -> None:
    fixed_time = datetime(2026, 4, 29, 0, 5, 9)
    local_time_clock_service = LocalTimeClockService(now_provider=lambda: fixed_time)

    current_snapshot = local_time_clock_service.get_current_local_time_snapshot()

    assert current_snapshot == {
        "hour": 0,
        "minute": 5,
        "second": 9,
        "formatted_24_hour_time": "00:05:09",
        "formatted_12_hour_time": "12:05:09 AM",
        "second_hand_angle": 54.0,
        "minute_hand_angle": 30.9,
        "hour_hand_angle": 2.5,
    }


def test_get_current_hand_angles_follows_required_formulas() -> None:
    fixed_time = datetime(2026, 4, 29, 15, 10, 30)
    local_time_clock_service = LocalTimeClockService(now_provider=lambda: fixed_time)

    assert local_time_clock_service.get_current_hand_angles() == {
        "second_hand_angle": 180.0,
        "minute_hand_angle": 63.0,
        "hour_hand_angle": 95.0,
    }


def test_get_formatted_time_supports_both_formats() -> None:
    fixed_time = datetime(2026, 4, 29, 23, 59, 8)
    local_time_clock_service = LocalTimeClockService(now_provider=lambda: fixed_time)

    assert local_time_clock_service.get_formatted_time(use_24_hour_format=True) == "23:59:08"
    assert local_time_clock_service.get_formatted_time(use_24_hour_format=False) == "11:59:08 PM"


def test_numeric_sequences_cover_full_ranges() -> None:
    local_time_clock_service = LocalTimeClockService(
        now_provider=lambda: datetime(2026, 4, 29, 12, 0, 0)
    )

    assert local_time_clock_service._hour_sequence.get_size() == 24
    assert local_time_clock_service._minute_sequence.get_size() == 60
    assert local_time_clock_service._second_sequence.get_size() == 60

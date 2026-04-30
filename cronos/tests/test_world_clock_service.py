"""Tests for the world clock service."""

from datetime import datetime

from cronos_core.world_clock_service import WorldClockService


def test_get_available_time_zones_returns_expected_city_names() -> None:
    world_clock_service = WorldClockService(
        now_provider=lambda: datetime(2026, 4, 29, 12, 0, 0).astimezone()
    )

    available_city_names = [
        available_entry["city_name"]
        for available_entry in world_clock_service.get_available_time_zones()
    ]

    assert "Bogot\u00e1" in available_city_names
    assert "Londres" in available_city_names
    assert "Tokio" in available_city_names


def test_add_and_remove_world_clock() -> None:
    world_clock_service = WorldClockService(
        now_provider=lambda: datetime(2026, 4, 29, 12, 0, 0).astimezone()
    )

    assert world_clock_service.add_world_clock("Bogot\u00e1") is True
    assert world_clock_service.add_world_clock("Bogot\u00e1") is False
    assert world_clock_service.remove_world_clock("Bogot\u00e1") is True
    assert world_clock_service.remove_world_clock("Bogot\u00e1") is False


def test_get_world_clock_snapshots_returns_live_snapshot_information() -> None:
    fixed_time = datetime(2026, 4, 29, 12, 15, 30).astimezone()
    world_clock_service = WorldClockService(now_provider=lambda: fixed_time)
    world_clock_service.add_world_clock("Bogot\u00e1")

    world_clock_snapshots = world_clock_service.get_world_clock_snapshots()

    assert len(world_clock_snapshots) == 1
    first_snapshot = world_clock_snapshots[0]
    assert first_snapshot["city_name"] == "Bogot\u00e1"
    assert "formatted_24_hour_time" in first_snapshot
    assert "formatted_12_hour_time" in first_snapshot
    assert "second_hand_angle" in first_snapshot
    assert "minute_hand_angle" in first_snapshot
    assert "hour_hand_angle" in first_snapshot


def test_unknown_world_clock_cannot_be_added() -> None:
    world_clock_service = WorldClockService(
        now_provider=lambda: datetime(2026, 4, 29, 12, 0, 0).astimezone()
    )

    assert world_clock_service.add_world_clock("Mars") is False

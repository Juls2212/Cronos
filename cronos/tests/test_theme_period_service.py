"""Tests for the theme period service."""

from cronos_core.theme_period_service import ThemePeriodService


def test_period_cycle_snapshot_matches_expected_order() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_cycle_snapshot() == [
        "dawn",
        "day",
        "evening",
        "night",
    ]


def test_get_period_for_hour_returns_dawn() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_for_hour(5) == "dawn"
    assert theme_period_service.get_period_for_hour(7) == "dawn"


def test_get_period_for_hour_returns_day() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_for_hour(8) == "day"
    assert theme_period_service.get_period_for_hour(16) == "day"


def test_get_period_for_hour_returns_evening() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_for_hour(17) == "evening"
    assert theme_period_service.get_period_for_hour(19) == "evening"


def test_get_period_for_hour_returns_night() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_for_hour(20) == "night"
    assert theme_period_service.get_period_for_hour(4) == "night"
    assert theme_period_service.get_period_for_hour(0) == "night"

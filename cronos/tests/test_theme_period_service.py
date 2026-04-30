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


def test_get_period_for_hour_returns_expected_periods() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_period_for_hour(5) == "dawn"
    assert theme_period_service.get_period_for_hour(7) == "dawn"
    assert theme_period_service.get_period_for_hour(8) == "day"
    assert theme_period_service.get_period_for_hour(16) == "day"
    assert theme_period_service.get_period_for_hour(17) == "evening"
    assert theme_period_service.get_period_for_hour(19) == "evening"
    assert theme_period_service.get_period_for_hour(20) == "night"
    assert theme_period_service.get_period_for_hour(4) == "night"


def test_get_theme_mode_for_hour_returns_warm_or_cool() -> None:
    theme_period_service = ThemePeriodService()

    assert theme_period_service.get_theme_mode_for_hour(6) == "warm"
    assert theme_period_service.get_theme_mode_for_hour(12) == "warm"
    assert theme_period_service.get_theme_mode_for_hour(18) == "cool"
    assert theme_period_service.get_theme_mode_for_hour(2) == "cool"


def test_get_local_view_palette_returns_required_color_keys() -> None:
    theme_period_service = ThemePeriodService()

    local_palette = theme_period_service.get_local_view_palette(11)

    assert local_palette["window_background"]
    assert local_palette["hero_panel"]
    assert local_palette["clock_face"]
    assert local_palette["clock_border"]


def test_get_world_clock_palette_returns_required_color_keys() -> None:
    theme_period_service = ThemePeriodService()

    world_palette = theme_period_service.get_world_clock_palette(23)

    assert world_palette["card_background"]
    assert world_palette["clock_face"]
    assert world_palette["clock_border"]
    assert world_palette["remove_fill"]

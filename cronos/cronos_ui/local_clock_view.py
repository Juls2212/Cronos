"""Local clock view for Cronos."""

from __future__ import annotations

import tkinter as tk

from cronos_core.local_time_clock_service import LocalTimeClockService
from cronos_core.theme_period_service import ThemePeriodService
from cronos_core.world_clock_service import WorldClockService

from .analog_clock_canvas import AnalogClockCanvas
from .sky_background_canvas import SkyBackgroundCanvas
from .world_clocks_panel import WorldClocksPanel


class LocalClockView(tk.Frame):
    """Display the real local clock with a cleaner responsive layout."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, bg="#e9f4ff")
        self._local_time_clock_service = LocalTimeClockService()
        self._theme_period_service = ThemePeriodService()
        self._world_clock_service = WorldClockService()
        self._use_24_hour_format = tk.BooleanVar(value=True)
        self._scheduled_refresh_identifier: str | None = None
        self._current_local_period: str | None = None
        self._current_local_theme_mode: str | None = None
        self._format_12_button: tk.Button | None = None
        self._format_24_button: tk.Button | None = None
        self._app_title_label: tk.Label | None = None
        self._screen_title_label: tk.Label | None = None
        self._subtitle_label: tk.Label | None = None
        self._digital_time_label: tk.Label | None = None
        self._hero_shell: tk.Frame | None = None
        self._hero_panel: tk.Frame | None = None
        self._stage_shell: tk.Frame | None = None
        self._stage_body: tk.Frame | None = None
        self._top_band_frame: tk.Frame | None = None
        self._branding_frame: tk.Frame | None = None
        self._information_strip: tk.Frame | None = None
        self._text_block: tk.Frame | None = None
        self._format_segment_shell: tk.Frame | None = None
        self._format_segment_frame: tk.Frame | None = None

        for default_city_name in ("Londres", "Tokio", "Nueva York"):
            self._world_clock_service.add_world_clock(default_city_name)

        self._build_layout()
        self._refresh_display()

    def destroy(self) -> None:
        """Cancel scheduled updates before destroying the view."""
        if self._scheduled_refresh_identifier is not None:
            self.after_cancel(self._scheduled_refresh_identifier)
            self._scheduled_refresh_identifier = None
        super().destroy()

    def _build_layout(self) -> None:
        self._background_canvas = SkyBackgroundCanvas(self, bg="#e9f4ff")
        self._background_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        interface_frame = tk.Frame(self, bg="#e9f4ff")
        interface_frame.pack(fill="both", expand=True, padx=34, pady=32)
        interface_frame.columnconfigure(0, weight=8)
        interface_frame.columnconfigure(1, weight=3)
        interface_frame.rowconfigure(0, weight=1)

        self._hero_shell = tk.Frame(interface_frame, bg="#bfd8ee", padx=1, pady=1)
        self._hero_shell.grid(row=0, column=0, sticky="nsew", padx=(0, 22))

        self._hero_panel = tk.Frame(self._hero_shell, bg="#fffdf8")
        self._hero_panel.pack(fill="both", expand=True)
        self._hero_panel.columnconfigure(0, weight=1)
        self._hero_panel.rowconfigure(2, weight=1)

        self._top_band_frame = tk.Frame(self._hero_panel, bg="#fffdf8")
        self._top_band_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(28, 0))
        self._top_band_frame.columnconfigure(0, weight=1)
        self._top_band_frame.columnconfigure(1, weight=0)

        self._branding_frame = tk.Frame(self._top_band_frame, bg="#fffdf8")
        self._branding_frame.grid(row=0, column=0, sticky="w")

        self._app_title_label = tk.Label(
            self._branding_frame,
            text="Cronos",
            font=("Georgia", 30, "bold"),
            fg="#155e75",
            bg="#fffdf8",
        )
        self._app_title_label.pack(anchor="w")

        self._screen_title_label = tk.Label(
            self._branding_frame,
            text="Reloj local",
            font=("Helvetica", 14, "bold"),
            fg="#b45309",
            bg="#fffdf8",
        )
        self._screen_title_label.pack(anchor="w", pady=(4, 0))

        self._build_format_segment(self._top_band_frame)

        self._information_strip = tk.Frame(self._hero_panel, bg="#fffdf8")
        self._information_strip.grid(row=1, column=0, sticky="ew", padx=40, pady=(22, 14))
        self._information_strip.columnconfigure(0, weight=1)

        self._text_block = tk.Frame(self._information_strip, bg="#fffdf8")
        self._text_block.grid(row=0, column=0, sticky="w")

        self._subtitle_label = tk.Label(
            self._text_block,
            text="Hora local",
            font=("Helvetica", 13, "bold"),
            fg="#ca8a04",
            bg="#fffdf8",
        )
        self._subtitle_label.pack(anchor="w")

        self._digital_time_label = tk.Label(
            self._text_block,
            text="00:00:00",
            font=("Helvetica", 31, "bold"),
            fg="#164e63",
            bg="#fffdf8",
        )
        self._digital_time_label.pack(anchor="w", pady=(6, 0))

        stage_frame = tk.Frame(self._hero_panel, bg="#fffdf8")
        stage_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(2, 26))
        stage_frame.columnconfigure(0, weight=1)
        stage_frame.rowconfigure(0, weight=1)

        self._stage_shell = tk.Frame(stage_frame, bg="#d7b98b", padx=1, pady=1)
        self._stage_shell.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        self._stage_body = tk.Frame(self._stage_shell, bg="#f8f1e3")
        self._stage_body.pack(fill="both", expand=True)

        self._analog_clock_canvas = AnalogClockCanvas(
            self._stage_body,
            width=620,
            height=620,
            show_numerals=True,
        )
        self._analog_clock_canvas.pack(expand=True, fill="both", padx=30, pady=30)

        self._world_clocks_panel = WorldClocksPanel(
            interface_frame,
            world_clock_service=self._world_clock_service,
            theme_period_service=self._theme_period_service,
        )
        self._world_clocks_panel.grid(row=0, column=1, sticky="nsew")

        self._refresh_format_segment()

    def _build_format_segment(self, master: tk.Misc) -> None:
        self._format_segment_shell = tk.Frame(master, bg="#dbeafe", padx=2, pady=2)
        self._format_segment_shell.grid(row=0, column=1, sticky="e")

        self._format_segment_frame = tk.Frame(self._format_segment_shell, bg="#f8fafc")
        self._format_segment_frame.pack()

        self._format_24_button = tk.Button(
            self._format_segment_frame,
            text="Formato 24 horas",
            command=lambda: self._set_time_format(True),
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
        )
        self._format_24_button.pack(side="left")

        self._format_12_button = tk.Button(
            self._format_segment_frame,
            text="Formato 12 horas",
            command=lambda: self._set_time_format(False),
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
        )
        self._format_12_button.pack(side="left")

    def _refresh_display(self) -> None:
        current_snapshot = self._local_time_clock_service.refresh_from_system_time()
        current_hour = int(current_snapshot["hour"])
        current_period = self._theme_period_service.get_period_for_hour(current_hour)
        current_theme_mode = self._theme_period_service.get_theme_mode_for_hour(current_hour)
        local_palette = self._theme_period_service.get_local_view_palette(current_hour)

        if self._current_local_period != current_period:
            self._background_canvas.set_period(current_period)
            self._current_local_period = current_period

        if self._current_local_theme_mode != current_theme_mode:
            self._apply_local_palette(local_palette)
            self._analog_clock_canvas.configure_visual_theme(
                {
                    "background": local_palette["clock_background"],
                    "outer_shadow": local_palette["hero_shell"],
                    "glow": local_palette["clock_glow"],
                    "frame": local_palette["clock_border"],
                    "face": local_palette["clock_face"],
                    "inner_ring": local_palette["hero_stage"],
                    "day_face": local_palette["clock_day_face"],
                    "night_face": local_palette["clock_night_face"],
                    "numeral": local_palette["clock_numeral"],
                    "major_tick": local_palette["clock_ring_primary"],
                    "minor_tick": local_palette["window_background"],
                    "hour_hand": local_palette["clock_hour_hand"],
                    "minute_hand": local_palette["clock_minute_hand"],
                    "second_hand": local_palette["clock_second_hand"],
                    "ring_primary": local_palette["clock_ring_primary"],
                    "ring_secondary": local_palette["clock_ring_secondary"],
                    "center_outer": local_palette["clock_hour_hand"],
                    "center_inner": local_palette["clock_glow"],
                }
            )
            if self._world_clocks_panel.get_panel_theme_mode() != current_theme_mode:
                self._world_clocks_panel.apply_panel_palette(local_palette)
                self._world_clocks_panel.set_panel_theme_mode(current_theme_mode)
            self._refresh_format_segment(local_palette)
            self._current_local_theme_mode = current_theme_mode

        self._analog_clock_canvas.update_clock_hands(
            hour_hand_angle=float(current_snapshot["hour_hand_angle"]),
            minute_hand_angle=float(current_snapshot["minute_hand_angle"]),
            second_hand_angle=float(current_snapshot["second_hand_angle"]),
        )

        current_time_label = self._local_time_clock_service.get_formatted_time(
            use_24_hour_format=self._use_24_hour_format.get()
        )
        if self._digital_time_label is not None:
            self._digital_time_label.configure(text=current_time_label)

        self._world_clocks_panel.refresh_world_clocks()

        next_refresh_delay = self._local_time_clock_service.get_milliseconds_until_next_second()
        self._scheduled_refresh_identifier = self.after(next_refresh_delay, self._refresh_display)

    def _apply_local_palette(self, palette: dict[str, str]) -> None:
        self.configure(bg=palette["window_background"])
        self._background_canvas.configure(bg=palette["window_background"])
        if self._hero_shell is not None:
            self._hero_shell.configure(bg=palette["hero_shell"])
        if self._hero_panel is not None:
            self._hero_panel.configure(bg=palette["hero_panel"])
        if self._top_band_frame is not None:
            self._top_band_frame.configure(bg=palette["hero_panel"])
        if self._branding_frame is not None:
            self._branding_frame.configure(bg=palette["hero_panel"])
        if self._information_strip is not None:
            self._information_strip.configure(bg=palette["hero_panel"])
        if self._text_block is not None:
            self._text_block.configure(bg=palette["hero_panel"])
        if self._stage_shell is not None:
            self._stage_shell.configure(bg=palette["hero_shell"])
        if self._stage_body is not None:
            self._stage_body.configure(bg=palette["hero_stage"])
        if self._format_segment_shell is not None:
            self._format_segment_shell.configure(bg=palette["toggle_shell"])
        if self._format_segment_frame is not None:
            self._format_segment_frame.configure(bg=palette["toggle_panel"])
        if self._app_title_label is not None:
            self._app_title_label.configure(bg=palette["hero_panel"], fg=palette["title"])
        if self._screen_title_label is not None:
            self._screen_title_label.configure(bg=palette["hero_panel"], fg=palette["subtitle"])
        if self._subtitle_label is not None:
            self._subtitle_label.configure(bg=palette["hero_panel"], fg=palette["subtitle"])
        if self._digital_time_label is not None:
            self._digital_time_label.configure(bg=palette["hero_panel"], fg=palette["digital_time"])

    def _set_time_format(self, use_24_hour_format: bool) -> None:
        self._use_24_hour_format.set(use_24_hour_format)
        self._refresh_digital_format_only()

    def _refresh_digital_format_only(self) -> None:
        current_time_label = self._local_time_clock_service.get_formatted_time(
            use_24_hour_format=self._use_24_hour_format.get()
        )
        if self._digital_time_label is not None:
            self._digital_time_label.configure(text=current_time_label)
        self._world_clocks_panel.set_use_24_hour_format(self._use_24_hour_format.get())
        current_hour = int(
            self._local_time_clock_service.get_current_local_time_snapshot()["hour"]
        )
        local_palette = self._theme_period_service.get_local_view_palette(current_hour)
        self._refresh_format_segment(local_palette)
        self._world_clocks_panel.refresh_world_clocks()

    def _refresh_format_segment(self, local_palette: dict[str, str] | None = None) -> None:
        if self._format_24_button is None or self._format_12_button is None:
            return

        if local_palette is None:
            current_hour = int(
                self._local_time_clock_service.get_current_local_time_snapshot()["hour"]
            )
            local_palette = self._theme_period_service.get_local_view_palette(current_hour)

        if self._use_24_hour_format.get():
            self._format_24_button.configure(
                bg=local_palette["toggle_active_fill"],
                fg=local_palette["toggle_active_text"],
                activebackground=local_palette["toggle_active_fill"],
                activeforeground=local_palette["toggle_active_text"],
            )
            self._format_12_button.configure(
                bg=local_palette["toggle_panel"],
                fg=local_palette["toggle_inactive_text"],
                activebackground=local_palette["toggle_panel"],
                activeforeground=local_palette["toggle_inactive_text"],
            )
        else:
            self._format_12_button.configure(
                bg=local_palette["toggle_active_fill"],
                fg=local_palette["toggle_active_text"],
                activebackground=local_palette["toggle_active_fill"],
                activeforeground=local_palette["toggle_active_text"],
            )
            self._format_24_button.configure(
                bg=local_palette["toggle_panel"],
                fg=local_palette["toggle_inactive_text"],
                activebackground=local_palette["toggle_panel"],
                activeforeground=local_palette["toggle_inactive_text"],
            )

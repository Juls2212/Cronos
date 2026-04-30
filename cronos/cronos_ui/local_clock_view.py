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
    """Display the real local clock with background and world clocks."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, bg="#dbeafe")
        self._local_time_clock_service = LocalTimeClockService()
        self._theme_period_service = ThemePeriodService()
        self._world_clock_service = WorldClockService()
        self._use_24_hour_format = tk.BooleanVar(value=True)
        self._scheduled_refresh_identifier: str | None = None

        for default_city_name in ("Bogot\u00e1", "Londres", "Tokio"):
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
        self._background_canvas = SkyBackgroundCanvas(self, bg="#dbeafe")
        self._background_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        main_content_frame = tk.Frame(self, bg="#dbeafe")
        main_content_frame.pack(fill="both", expand=True, padx=24, pady=24)
        main_content_frame.columnconfigure(0, weight=3)
        main_content_frame.columnconfigure(1, weight=1)
        main_content_frame.rowconfigure(0, weight=1)

        local_clock_panel = tk.Frame(main_content_frame, bg="#dbeafe")
        local_clock_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        title_label = tk.Label(
            local_clock_panel,
            text="Reloj local",
            font=("Helvetica", 26, "bold"),
            fg="#0f172a",
            bg="#dbeafe",
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            local_clock_panel,
            text="Hora local",
            font=("Helvetica", 16, "bold"),
            fg="#1e3a8a",
            bg="#dbeafe",
        )
        subtitle_label.pack(anchor="w", pady=(6, 12))

        top_information_frame = tk.Frame(local_clock_panel, bg="#dbeafe")
        top_information_frame.pack(fill="x", pady=(0, 14))

        self._digital_time_label = tk.Label(
            top_information_frame,
            text="00:00:00",
            font=("Helvetica", 22, "bold"),
            fg="#0f172a",
            bg="#dbeafe",
        )
        self._digital_time_label.pack(side="left")

        format_toggle_frame = tk.Frame(top_information_frame, bg="#dbeafe")
        format_toggle_frame.pack(side="right")

        format_24_button = tk.Radiobutton(
            format_toggle_frame,
            text="Formato 24 horas",
            value=True,
            variable=self._use_24_hour_format,
            command=self._refresh_digital_format_only,
            font=("Helvetica", 11, "bold"),
            fg="#0f172a",
            bg="#dbeafe",
            selectcolor="#bfdbfe",
            activebackground="#dbeafe",
        )
        format_24_button.pack(anchor="e")

        format_12_button = tk.Radiobutton(
            format_toggle_frame,
            text="Formato 12 horas",
            value=False,
            variable=self._use_24_hour_format,
            command=self._refresh_digital_format_only,
            font=("Helvetica", 11, "bold"),
            fg="#0f172a",
            bg="#dbeafe",
            selectcolor="#bfdbfe",
            activebackground="#dbeafe",
        )
        format_12_button.pack(anchor="e")

        self._analog_clock_canvas = AnalogClockCanvas(
            local_clock_panel,
            width=560,
            height=560,
            face_fill_color="#f8fafc",
            border_color="#0f172a",
            numeral_color="#0f172a",
            hand_color="#0f172a",
            minute_hand_color="#1d4ed8",
            second_hand_color="#dc2626",
            background_color="#dbeafe",
        )
        self._analog_clock_canvas.pack(expand=True, fill="both")

        self._world_clocks_panel = WorldClocksPanel(
            main_content_frame,
            world_clock_service=self._world_clock_service,
        )
        self._world_clocks_panel.grid(row=0, column=1, sticky="nsew")

    def _refresh_display(self) -> None:
        current_snapshot = self._local_time_clock_service.refresh_from_system_time()
        current_period = self._theme_period_service.get_period_for_hour(int(current_snapshot["hour"]))
        self._background_canvas.set_period(current_period)
        self._analog_clock_canvas.update_clock_hands(
            hour_hand_angle=float(current_snapshot["hour_hand_angle"]),
            minute_hand_angle=float(current_snapshot["minute_hand_angle"]),
            second_hand_angle=float(current_snapshot["second_hand_angle"]),
        )

        current_time_label = self._local_time_clock_service.get_formatted_time(
            use_24_hour_format=self._use_24_hour_format.get()
        )
        self._digital_time_label.configure(text=current_time_label)
        self._world_clocks_panel.set_use_24_hour_format(self._use_24_hour_format.get())
        self._world_clocks_panel.refresh_world_clocks()

        next_refresh_delay = self._local_time_clock_service.get_milliseconds_until_next_second()
        self._scheduled_refresh_identifier = self.after(next_refresh_delay, self._refresh_display)

    def _refresh_digital_format_only(self) -> None:
        current_time_label = self._local_time_clock_service.get_formatted_time(
            use_24_hour_format=self._use_24_hour_format.get()
        )
        self._digital_time_label.configure(text=current_time_label)
        if hasattr(self, "_world_clocks_panel"):
            self._world_clocks_panel.set_use_24_hour_format(self._use_24_hour_format.get())

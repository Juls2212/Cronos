"""World clocks side panel for Cronos."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from cronos_core.world_clock_service import WorldClockService

from .analog_clock_canvas import AnalogClockCanvas


class WorldClockCard(tk.Frame):
    """Display one small world clock entry."""

    def __init__(
        self,
        master: tk.Misc,
        city_name: str,
        remove_action,
    ) -> None:
        super().__init__(master, bg="#f8fafc", bd=1, relief=tk.SOLID)
        self._city_name = city_name
        self._time_label = tk.Label(
            self,
            text="--:--:--",
            font=("Helvetica", 12, "bold"),
            fg="#1e293b",
            bg="#f8fafc",
        )
        header_frame = tk.Frame(self, bg="#f8fafc")
        header_frame.pack(fill="x", padx=12, pady=(10, 6))

        city_label = tk.Label(
            header_frame,
            text=city_name,
            font=("Helvetica", 13, "bold"),
            fg="#0f172a",
            bg="#f8fafc",
        )
        city_label.pack(side="left")

        remove_button = tk.Button(
            header_frame,
            text="Eliminar",
            command=lambda: remove_action(city_name),
            font=("Helvetica", 9, "bold"),
            fg="#ffffff",
            bg="#dc2626",
            activeforeground="#ffffff",
            activebackground="#b91c1c",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
        )
        remove_button.pack(side="right")

        self._analog_clock_canvas = AnalogClockCanvas(
            self,
            width=160,
            height=160,
            face_fill_color="#ffffff",
            border_color="#1e293b",
            numeral_color="#1e293b",
            hand_color="#0f172a",
            minute_hand_color="#2563eb",
            second_hand_color="#ef4444",
            background_color="#f8fafc",
        )
        self._analog_clock_canvas.pack(padx=10, pady=4)
        self._time_label.pack(pady=(0, 12))

    def refresh_clock(
        self,
        digital_time: str,
        hour_hand_angle: float,
        minute_hand_angle: float,
        second_hand_angle: float,
    ) -> None:
        """Refresh the small analog clock and digital label."""
        self._time_label.configure(text=digital_time)
        self._analog_clock_canvas.update_clock_hands(
            hour_hand_angle=hour_hand_angle,
            minute_hand_angle=minute_hand_angle,
            second_hand_angle=second_hand_angle,
        )

    @property
    def city_name(self) -> str:
        """Return the represented city name."""
        return self._city_name


class WorldClocksPanel(tk.Frame):
    """Display world clocks in a narrow side column."""

    def __init__(self, master: tk.Misc, world_clock_service: WorldClockService) -> None:
        super().__init__(master, bg="#eff6ff", bd=1, relief=tk.SOLID)
        self._world_clock_service = world_clock_service
        self._use_24_hour_format = True
        self._city_selector_variable = tk.StringVar()
        self._clock_cards: dict[str, WorldClockCard] = {}
        self._build_layout()

    def set_use_24_hour_format(self, use_24_hour_format: bool) -> None:
        """Update the digital format used by all world clocks."""
        self._use_24_hour_format = use_24_hour_format
        self.refresh_world_clocks()

    def refresh_world_clocks(self) -> None:
        """Redraw every selected world clock."""
        for clock_snapshot in self._world_clock_service.get_world_clock_snapshots():
            city_name = str(clock_snapshot["city_name"])
            clock_card = self._clock_cards.get(city_name)
            if clock_card is None:
                continue

            digital_time = (
                str(clock_snapshot["formatted_24_hour_time"])
                if self._use_24_hour_format
                else str(clock_snapshot["formatted_12_hour_time"])
            )
            clock_card.refresh_clock(
                digital_time=digital_time,
                hour_hand_angle=float(clock_snapshot["hour_hand_angle"]),
                minute_hand_angle=float(clock_snapshot["minute_hand_angle"]),
                second_hand_angle=float(clock_snapshot["second_hand_angle"]),
            )

    def _build_layout(self) -> None:
        title_label = tk.Label(
            self,
            text="Relojes mundiales",
            font=("Helvetica", 17, "bold"),
            fg="#0f172a",
            bg="#eff6ff",
        )
        title_label.pack(anchor="w", padx=16, pady=(18, 10))

        controls_frame = tk.Frame(self, bg="#eff6ff")
        controls_frame.pack(fill="x", padx=16, pady=(0, 12))

        available_city_names = [
            entry["city_name"] for entry in self._world_clock_service.get_available_time_zones()
        ]
        if available_city_names:
            self._city_selector_variable.set(available_city_names[0])

        city_selector = ttk.Combobox(
            controls_frame,
            textvariable=self._city_selector_variable,
            values=available_city_names,
            state="readonly",
            width=18,
        )
        city_selector.pack(fill="x", pady=(0, 8))

        add_button = tk.Button(
            controls_frame,
            text="Agregar reloj",
            command=self._add_selected_city,
            font=("Helvetica", 10, "bold"),
            fg="#ffffff",
            bg="#2563eb",
            activeforeground="#ffffff",
            activebackground="#1d4ed8",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=8,
        )
        add_button.pack(fill="x")

        self._clock_cards_container = tk.Frame(self, bg="#eff6ff")
        self._clock_cards_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _add_selected_city(self) -> None:
        city_name = self._city_selector_variable.get()
        if not city_name:
            return

        if not self._world_clock_service.add_world_clock(city_name):
            return

        clock_card = WorldClockCard(
            self._clock_cards_container,
            city_name=city_name,
            remove_action=self._remove_city,
        )
        clock_card.pack(fill="x", pady=8)
        self._clock_cards[city_name] = clock_card
        self.refresh_world_clocks()

    def _remove_city(self, city_name: str) -> None:
        if not self._world_clock_service.remove_world_clock(city_name):
            return

        clock_card = self._clock_cards.pop(city_name, None)
        if clock_card is not None:
            clock_card.destroy()

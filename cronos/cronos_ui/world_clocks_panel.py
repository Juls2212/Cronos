"""World clocks side panel for Cronos."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from cronos_core.theme_period_service import ThemePeriodService
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
        super().__init__(master, bg="#ffffff", highlightthickness=0, bd=0)
        self._remove_action = remove_action
        self._city_name = city_name
        self._theme_mode: str | None = None
        self._card_shell = tk.Frame(self, bg="#d3b58a", padx=2, pady=2)
        self._card_shell.pack(fill="x")

        self._card_body = tk.Frame(self._card_shell, bg="#fff8ec")
        self._card_body.pack(fill="x")

        header_frame = tk.Frame(self._card_body, bg="#fff8ec")
        header_frame.pack(fill="x", padx=14, pady=(12, 4))

        self._city_label = tk.Label(
            header_frame,
            text=city_name,
            font=("Georgia", 13, "bold"),
            fg="#92400e",
            bg="#fff8ec",
        )
        self._city_label.pack(side="left")

        self._remove_button = tk.Button(
            header_frame,
            text="Eliminar",
            command=lambda: self._remove_action(city_name),
            font=("Helvetica", 9, "bold"),
            fg="#fff7ed",
            bg="#c2410c",
            activeforeground="#ffffff",
            activebackground="#9a3412",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
        )
        self._remove_button.pack(side="right")

        self._analog_clock_canvas = AnalogClockCanvas(
            self._card_body,
            width=126,
            height=126,
            show_numerals=False,
        )
        self._analog_clock_canvas.pack(pady=(4, 4))

        self._time_label = tk.Label(
            self._card_body,
            text="--:--:--",
            font=("Helvetica", 12, "bold"),
            fg="#78350f",
            bg="#fff8ec",
        )
        self._time_label.pack(pady=(0, 14))

    def apply_palette(self, palette: dict[str, str]) -> None:
        """Apply the card palette and update the mini clock styling."""
        self.configure(bg=palette["card_background"])
        self._card_shell.configure(bg=palette["card_shell"])
        self._card_body.configure(bg=palette["card_background"])
        self._city_label.configure(
            fg=palette["title"],
            bg=palette["card_background"],
        )
        self._time_label.configure(
            fg=palette["digital_time"],
            bg=palette["card_background"],
        )
        self._remove_button.configure(
            fg=palette["remove_text"],
            bg=palette["remove_fill"],
            activeforeground=palette["remove_text"],
            activebackground=palette["remove_fill"],
        )
        self._analog_clock_canvas.configure_visual_theme(
            {
                "background": palette["card_background"],
                "outer_shadow": palette["card_shell"],
                "glow": palette["clock_glow"],
                "frame": palette["clock_border"],
                "face": palette["clock_face"],
                "inner_ring": palette["card_background"],
                "numeral": palette["clock_numeral"],
                "major_tick": palette["accent_primary"],
                "minor_tick": palette["accent_secondary"],
                "hour_hand": palette["clock_hour_hand"],
                "minute_hand": palette["clock_minute_hand"],
                "second_hand": palette["clock_second_hand"],
                "center_outer": palette["clock_hour_hand"],
                "center_inner": palette["accent_primary"],
            }
        )

    def get_theme_mode(self) -> str | None:
        """Return the current theme mode applied to this card."""
        return self._theme_mode

    def set_theme_mode(self, theme_mode: str) -> None:
        """Store the theme mode currently applied to this card."""
        self._theme_mode = theme_mode

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


class WorldClocksPanel(tk.Frame):
    """Display world clocks in a compact scrollable right-side column."""

    def __init__(
        self,
        master: tk.Misc,
        world_clock_service: WorldClockService,
        theme_period_service: ThemePeriodService,
    ) -> None:
        super().__init__(master, bg="#bfd8ee", highlightthickness=0, bd=0, width=320)
        self._world_clock_service = world_clock_service
        self._theme_period_service = theme_period_service
        self._use_24_hour_format = True
        self._city_selector_variable = tk.StringVar()
        self._clock_cards: dict[str, WorldClockCard] = {}
        self._panel_theme_mode: str | None = None
        self.grid_propagate(False)
        self._build_layout()

    def apply_panel_palette(self, palette: dict[str, str]) -> None:
        """Apply the current local palette to the panel shell and controls."""
        self.configure(bg=palette["world_panel_shell"])
        self._panel_shell.configure(bg=palette["world_panel_shell"])
        self._panel_body.configure(bg=palette["world_panel_background"])
        self._title_label.configure(
            bg=palette["world_panel_background"],
            fg=palette["title"],
        )
        self._controls_shell.configure(bg=palette["world_panel_shell"])
        self._controls_body.configure(bg=palette["world_panel_background"])
        self._scroll_canvas.configure(bg=palette["world_panel_background"])
        self._cards_container.configure(bg=palette["world_panel_background"])

    def set_use_24_hour_format(self, use_24_hour_format: bool) -> None:
        """Update the digital format used by all world clocks."""
        self._use_24_hour_format = use_24_hour_format

    def set_panel_theme_mode(self, theme_mode: str) -> None:
        """Store the local panel theme mode used to avoid redundant recoloring."""
        self._panel_theme_mode = theme_mode

    def get_panel_theme_mode(self) -> str | None:
        """Return the theme mode currently applied to the panel."""
        return self._panel_theme_mode

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
            theme_mode = str(clock_snapshot["theme_mode"])
            if clock_card.get_theme_mode() != theme_mode:
                card_palette = self._theme_period_service.get_world_clock_palette(
                    int(clock_snapshot["hour"])
                )
                clock_card.apply_palette(card_palette)
                clock_card.set_theme_mode(theme_mode)
            clock_card.refresh_clock(
                digital_time=digital_time,
                hour_hand_angle=float(clock_snapshot["hour_hand_angle"]),
                minute_hand_angle=float(clock_snapshot["minute_hand_angle"]),
                second_hand_angle=float(clock_snapshot["second_hand_angle"]),
            )

    def _build_layout(self) -> None:
        self._panel_shell = tk.Frame(self, bg="#bfd8ee", padx=2, pady=2)
        self._panel_shell.pack(fill="both", expand=True)

        self._panel_body = tk.Frame(self._panel_shell, bg="#fffdf8")
        self._panel_body.pack(fill="both", expand=True)

        self._title_label = tk.Label(
            self._panel_body,
            text="Relojes mundiales",
            font=("Georgia", 17, "bold"),
            fg="#155e75",
            bg="#fffdf8",
        )
        self._title_label.pack(anchor="w", padx=16, pady=(16, 10))

        self._controls_shell = tk.Frame(self._panel_body, bg="#bfd8ee", padx=2, pady=2)
        self._controls_shell.pack(fill="x", padx=14, pady=(0, 10))

        self._controls_body = tk.Frame(self._controls_shell, bg="#fffdf8")
        self._controls_body.pack(fill="x")
        self._controls_body.columnconfigure(0, weight=1)

        available_city_names = [
            entry["city_name"] for entry in self._world_clock_service.get_available_time_zones()
        ]
        if available_city_names:
            self._city_selector_variable.set(available_city_names[0])

        style_object = ttk.Style()
        style_object.configure(
            "Cronos.TCombobox",
            fieldbackground="#ffffff",
            background="#ffffff",
            foreground="#334155",
            arrowcolor="#334155",
            borderwidth=0,
            relief="flat",
        )

        city_selector = ttk.Combobox(
            self._controls_body,
            textvariable=self._city_selector_variable,
            values=available_city_names,
            state="readonly",
            width=20,
            style="Cronos.TCombobox",
        )
        city_selector.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))

        add_button = tk.Button(
            self._controls_body,
            text="Agregar reloj",
            command=self._add_selected_city,
            font=("Helvetica", 10, "bold"),
            fg="#1f2937",
            bg="#fcd34d",
            activeforeground="#1f2937",
            activebackground="#fbbf24",
            relief=tk.FLAT,
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
        )
        add_button.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        list_frame = tk.Frame(self._panel_body, bg="#fffdf8")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self._scroll_canvas = tk.Canvas(
            list_frame,
            bg="#fffdf8",
            highlightthickness=0,
            bd=0,
        )
        self._scroll_canvas.grid(row=0, column=0, sticky="nsew")

        scroll_bar = tk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self._scroll_canvas.yview,
        )
        scroll_bar.grid(row=0, column=1, sticky="ns")
        self._scroll_canvas.configure(yscrollcommand=scroll_bar.set)

        self._cards_container = tk.Frame(self._scroll_canvas, bg="#fffdf8")
        self._cards_window = self._scroll_canvas.create_window(
            (0, 0),
            window=self._cards_container,
            anchor="nw",
        )
        self._cards_container.bind("<Configure>", self._on_cards_container_configure)
        self._scroll_canvas.bind("<Configure>", self._on_scroll_canvas_configure)

    def _add_selected_city(self) -> None:
        city_name = self._city_selector_variable.get()
        if not city_name:
            return

        if not self._world_clock_service.add_world_clock(city_name):
            return

        clock_card = WorldClockCard(
            self._cards_container,
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
        self._on_cards_container_configure()

    def _on_cards_container_configure(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        self._scroll_canvas.configure(scrollregion=self._scroll_canvas.bbox("all"))

    def _on_scroll_canvas_configure(self, event: tk.Event[tk.Misc]) -> None:
        self._scroll_canvas.itemconfigure(self._cards_window, width=event.width)

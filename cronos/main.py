"""Application entry point for Cronos."""

from cronos_ui.main_window import CronosMainWindow


def main() -> None:
    """Create the main Tkinter window and start the event loop."""
    application_window = CronosMainWindow()
    application_window.mainloop()


if __name__ == "__main__":
    main()

"""Application entry point for the Cronos desktop clock."""

from src.cronos.app.application import build_application


def main() -> None:
    """Create and start the Tkinter application."""
    application = build_application()
    application.mainloop()


if __name__ == "__main__":
    main()

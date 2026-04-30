"""Tkinter application bootstrap for Cronos."""

from tkinter import Label, Tk


class CronosApplication(Tk):
    """Base Tkinter window for the phase-one project skeleton."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Cronos")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg="#0f172a")
        self._build_phase_message()

    def _build_phase_message(self) -> None:
        """Render a minimal visual placeholder for the first development phase."""
        title_label = Label(
            self,
            text="Cronos",
            font=("Helvetica", 28, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        )
        title_label.pack(pady=(60, 12))

        phase_label = Label(
            self,
            text="Fase 1: estructura base y secuencia circular doble",
            font=("Helvetica", 14),
            fg="#cbd5e1",
            bg="#0f172a",
        )
        phase_label.pack()


def build_application() -> CronosApplication:
    """Create the main Tkinter application instance."""
    return CronosApplication()

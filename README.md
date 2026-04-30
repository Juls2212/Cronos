# Cronos

Cronos is an academic desktop clock application developed in Python with Tkinter for a Data Structures / Software Structure course.

## Development rules

- The user interface must be desktop-based and built only with Python and Tkinter.
- Internal code, structure names, and technical documentation are written in English.
- Visible interface text may be written in Spanish.
- Circular doubly linked lists are manually implemented and used as a core academic requirement.
- The main internal mechanism must not be replaced by standard Python lists.

## Phase-based development

This repository is being built in phases.

### Phase 1

Current scope:

- Base Python project structure
- Tkinter desktop entry point
- Manual circular doubly linked sequence implementation
- Academic documentation for the selected data structure

Not implemented yet:

- Analog local clock
- World clocks
- Stopwatch
- History section
- Dynamic background
- 12-hour / 24-hour format switching

## Project structure

```text
chronos.py
src/
  chronos/
    app/
      application.py
    structures/
      circular_doubly_linked_sequence.py
README.md
ACADEMIC_EXPLANATION.md
```

## Running the current phase

```bash
python chronos.py
```

The current application window is a minimal phase-one placeholder. Later phases will replace that placeholder with the real clock interface.

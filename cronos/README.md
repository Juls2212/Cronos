# Cronos

Cronos is a desktop clock application built with Python and Tkinter.

## Academic focus

This project was created for an academic context where the main technical focus is the design and use of a circular doubly linked list. The linked structure is implemented manually and is intended to support future clock-related cycles such as hours, minutes, seconds, and visual time periods.

## Language rules

- Internal code is written in English.
- Technical names such as classes, methods, variables, file names, and comments are written in English.
- Visible user interface text is written in Spanish.

## Interface scope

Cronos uses a desktop interface implemented with Tkinter only.

The project does not use:

- Flask
- HTML
- CSS
- JavaScript
- React
- Browser-based code

## How to run the application

From the `cronos` directory:

```bash
python main.py
```

This opens Cronos directly into the focused clock interface with the real local analog clock, world clocks, dynamic background, and digital 12-hour / 24-hour formatting toggle.

## How to run the tests

From the `cronos` directory:

```bash
python -m pytest
```

The test suite validates the circular doubly linked list behavior and the active clock services.

# Academic Explanation

## Why a circular doubly linked list is appropriate for Cronos

Cronos is a clock application, and clocks are inherently cyclical systems:

- Hours repeat
- Minutes repeat
- Seconds repeat
- Visual day periods can repeat in sequence

A circular doubly linked list is an academically appropriate structure for this domain because:

- The last linked element connects back to the first one
- The first linked element connects back to the last one
- The selected position can move both forward and backward
- The structure models cyclic navigation directly instead of simulating it with index arithmetic over a standard Python list

## Implemented structure

The linked structure is split into two classes:

- `CircularSequenceElement`
- `CircularDoublyLinkedSequence`

Each `CircularSequenceElement` explicitly stores:

- `value`
- `previous_reference`
- `next_reference`

This satisfies the academic requirement that every linked element must maintain real bidirectional references.

## Academic integrity of the implementation

The linked sequence does not use a normal Python list as its main internal mechanism.

The internal behavior is based on real connected elements. A standard Python list is only used in:

- `get_values_snapshot`
- Tests for assertions and inspection

This keeps the structure academically defensible while still allowing straightforward validation.

## Intended future use in Cronos

The base linked structure is designed to support the active clock services such as:

- `LocalTimeClockService`
- `WorldClockService`
- `ThemePeriodService`

These services connect the academic structure to the visual Tkinter clock application.

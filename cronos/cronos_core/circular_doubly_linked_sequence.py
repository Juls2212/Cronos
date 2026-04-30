"""Circular doubly linked sequence implementation for Cronos."""

from __future__ import annotations

from typing import Generic, TypeVar

from .circular_sequence_element import CircularSequenceElement


SequenceValue = TypeVar("SequenceValue")


class CircularDoublyLinkedSequence(Generic[SequenceValue]):
    """Maintain values through real circular bidirectional links."""

    def __init__(self) -> None:
        self._first_element: CircularSequenceElement[SequenceValue] | None = None
        self._selected_element: CircularSequenceElement[SequenceValue] | None = None
        self._sequence_size = 0

    def append_value(self, value: SequenceValue) -> None:
        """Append a value at the logical end of the circular sequence."""
        appended_element = CircularSequenceElement(value=value)

        if self._first_element is None:
            appended_element.previous_reference = appended_element
            appended_element.next_reference = appended_element
            self._first_element = appended_element
            self._selected_element = appended_element
            self._sequence_size = 1
            return

        first_element = self._first_element
        last_element = first_element.previous_reference
        if last_element is None:
            raise RuntimeError("Broken circular sequence: missing previous reference.")

        appended_element.previous_reference = last_element
        appended_element.next_reference = first_element
        last_element.next_reference = appended_element
        first_element.previous_reference = appended_element
        self._sequence_size += 1

    def select_value(self, expected_value: SequenceValue) -> bool:
        """Select the first occurrence of the provided value."""
        if self._first_element is None:
            return False

        current_element = self._first_element
        for _ in range(self._sequence_size):
            if current_element.value == expected_value:
                self._selected_element = current_element
                return True

            next_element = current_element.next_reference
            if next_element is None:
                raise RuntimeError("Broken circular sequence: missing next reference.")
            current_element = next_element

        return False

    def get_selected_value(self) -> SequenceValue | None:
        """Return the currently selected value, or None when empty."""
        if self._selected_element is None:
            return None
        return self._selected_element.value

    def move_to_next_value(self) -> SequenceValue | None:
        """Move the selection forward in circular order."""
        if self._selected_element is None:
            return None

        next_element = self._selected_element.next_reference
        if next_element is None:
            raise RuntimeError("Broken circular sequence: missing next reference.")

        self._selected_element = next_element
        return self._selected_element.value

    def move_to_previous_value(self) -> SequenceValue | None:
        """Move the selection backward in circular order."""
        if self._selected_element is None:
            return None

        previous_element = self._selected_element.previous_reference
        if previous_element is None:
            raise RuntimeError("Broken circular sequence: missing previous reference.")

        self._selected_element = previous_element
        return self._selected_element.value

    def reset_to_first_value(self) -> SequenceValue | None:
        """Reset the selection to the first inserted value."""
        self._selected_element = self._first_element
        return self.get_selected_value()

    def get_values_snapshot(self) -> list[SequenceValue]:
        """Return the sequence values in logical order for inspection."""
        snapshot: list[SequenceValue] = []

        if self._first_element is None:
            return snapshot

        current_element = self._first_element
        for _ in range(self._sequence_size):
            snapshot.append(current_element.value)
            next_element = current_element.next_reference
            if next_element is None:
                raise RuntimeError("Broken circular sequence: missing next reference.")
            current_element = next_element

        return snapshot

    def get_size(self) -> int:
        """Return the number of linked values."""
        return self._sequence_size

    def is_empty(self) -> bool:
        """Return whether the sequence has no values."""
        return self._sequence_size == 0

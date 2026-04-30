"""Circular doubly linked sequence implementation for academic use."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar


SequenceValue = TypeVar("SequenceValue")


@dataclass(slots=True)
class CircularSequenceElement(Generic[SequenceValue]):
    """Linked element with explicit bidirectional references."""

    value: SequenceValue
    previous_reference: CircularSequenceElement[SequenceValue] | None = None
    next_reference: CircularSequenceElement[SequenceValue] | None = None


class CircularDoublyLinkedSequence(Generic[SequenceValue]):
    """Manual circular doubly linked sequence.

    The structure keeps an anchor reference to one element. From that
    reference, the previous and next connections allow full circular
    traversal in both directions.
    """

    def __init__(self) -> None:
        self._anchor_element: CircularSequenceElement[SequenceValue] | None = None
        self._element_count = 0

    def __len__(self) -> int:
        return self._element_count

    def __iter__(self) -> Iterator[SequenceValue]:
        if self._anchor_element is None:
            return

        current_element = self._anchor_element
        for _ in range(self._element_count):
            yield current_element.value
            next_element = current_element.next_reference
            if next_element is None:
                raise RuntimeError("Broken circular sequence: next reference is missing.")
            current_element = next_element

    def is_empty(self) -> bool:
        """Return whether the sequence has no linked elements."""
        return self._element_count == 0

    def append_value(self, value: SequenceValue) -> CircularSequenceElement[SequenceValue]:
        """Insert a value before the anchor, preserving the current anchor."""
        new_element = CircularSequenceElement(value=value)

        if self._anchor_element is None:
            self._connect_first_element(new_element)
            return new_element

        anchor_element = self._anchor_element
        last_element = anchor_element.previous_reference
        if last_element is None:
            raise RuntimeError("Broken circular sequence: previous reference is missing.")

        new_element.previous_reference = last_element
        new_element.next_reference = anchor_element
        last_element.next_reference = new_element
        anchor_element.previous_reference = new_element
        self._element_count += 1
        return new_element

    def prepend_value(self, value: SequenceValue) -> CircularSequenceElement[SequenceValue]:
        """Insert a value as the new anchor element."""
        new_element = self.append_value(value)
        self._anchor_element = new_element
        return new_element

    def remove_anchor_value(self) -> SequenceValue:
        """Remove and return the current anchor value."""
        if self._anchor_element is None:
            raise IndexError("Cannot remove from an empty circular sequence.")

        removed_element = self._anchor_element

        if self._element_count == 1:
            self._anchor_element = None
            self._element_count = 0
            return removed_element.value

        previous_element = removed_element.previous_reference
        next_element = removed_element.next_reference
        if previous_element is None or next_element is None:
            raise RuntimeError("Broken circular sequence: linked references are missing.")

        previous_element.next_reference = next_element
        next_element.previous_reference = previous_element
        self._anchor_element = next_element
        self._element_count -= 1
        return removed_element.value

    def get_anchor_element(self) -> CircularSequenceElement[SequenceValue] | None:
        """Return the current anchor element."""
        return self._anchor_element

    def move_anchor_forward(
        self, steps: int = 1
    ) -> CircularSequenceElement[SequenceValue] | None:
        """Advance the anchor through the circular next references."""
        return self._move_anchor(steps=steps, use_next_reference=True)

    def move_anchor_backward(
        self, steps: int = 1
    ) -> CircularSequenceElement[SequenceValue] | None:
        """Move the anchor through the circular previous references."""
        return self._move_anchor(steps=steps, use_next_reference=False)

    def find_first_element_by_value(
        self, expected_value: SequenceValue
    ) -> CircularSequenceElement[SequenceValue] | None:
        """Locate the first linked element whose value matches the expectation."""
        if self._anchor_element is None:
            return None

        current_element = self._anchor_element
        for _ in range(self._element_count):
            if current_element.value == expected_value:
                return current_element
            next_element = current_element.next_reference
            if next_element is None:
                raise RuntimeError("Broken circular sequence: next reference is missing.")
            current_element = next_element
        return None

    def build_value_snapshot(self) -> list[SequenceValue]:
        """Return a standard list only for inspection and documentation use."""
        return list(iter(self))

    def _connect_first_element(
        self, first_element: CircularSequenceElement[SequenceValue]
    ) -> None:
        first_element.previous_reference = first_element
        first_element.next_reference = first_element
        self._anchor_element = first_element
        self._element_count = 1

    def _move_anchor(
        self, steps: int, use_next_reference: bool
    ) -> CircularSequenceElement[SequenceValue] | None:
        if self._anchor_element is None:
            return None

        if steps < 0:
            raise ValueError("Step count must be zero or positive.")

        current_element = self._anchor_element
        for _ in range(steps):
            linked_element = (
                current_element.next_reference
                if use_next_reference
                else current_element.previous_reference
            )
            if linked_element is None:
                raise RuntimeError("Broken circular sequence: linked reference is missing.")
            current_element = linked_element

        self._anchor_element = current_element
        return current_element

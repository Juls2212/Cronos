"""Linked element definition for the circular sequence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


SequenceValue = TypeVar("SequenceValue")


@dataclass(slots=True)
class CircularSequenceElement(Generic[SequenceValue]):
    """Represent one value in a circular doubly linked sequence."""

    value: SequenceValue
    previous_reference: CircularSequenceElement[SequenceValue] | None = None
    next_reference: CircularSequenceElement[SequenceValue] | None = None

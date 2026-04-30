"""Tests for the circular doubly linked sequence."""

from cronos_core.circular_doubly_linked_sequence import CircularDoublyLinkedSequence


def test_empty_sequence() -> None:
    clock_sequence = CircularDoublyLinkedSequence[int]()

    assert clock_sequence.is_empty() is True
    assert clock_sequence.get_size() == 0
    assert clock_sequence.get_selected_value() is None
    assert clock_sequence.get_values_snapshot() == []
    assert clock_sequence.move_to_next_value() is None
    assert clock_sequence.move_to_previous_value() is None
    assert clock_sequence.reset_to_first_value() is None
    assert clock_sequence.select_value(10) is False


def test_one_value_sequence() -> None:
    clock_sequence = CircularDoublyLinkedSequence[str]()
    clock_sequence.append_value("one")

    assert clock_sequence.is_empty() is False
    assert clock_sequence.get_size() == 1
    assert clock_sequence.get_selected_value() == "one"
    assert clock_sequence.get_values_snapshot() == ["one"]

    first_element = clock_sequence._first_element
    assert first_element is not None
    assert first_element.previous_reference is first_element
    assert first_element.next_reference is first_element


def test_several_value_sequence() -> None:
    clock_sequence = CircularDoublyLinkedSequence[int]()
    clock_sequence.append_value(1)
    clock_sequence.append_value(2)
    clock_sequence.append_value(3)

    assert clock_sequence.get_size() == 3
    assert clock_sequence.get_values_snapshot() == [1, 2, 3]
    assert clock_sequence.get_selected_value() == 1


def test_circular_forward_movement() -> None:
    clock_sequence = CircularDoublyLinkedSequence[int]()
    clock_sequence.append_value(1)
    clock_sequence.append_value(2)
    clock_sequence.append_value(3)

    assert clock_sequence.move_to_next_value() == 2
    assert clock_sequence.move_to_next_value() == 3
    assert clock_sequence.move_to_next_value() == 1


def test_circular_backward_movement() -> None:
    clock_sequence = CircularDoublyLinkedSequence[int]()
    clock_sequence.append_value(1)
    clock_sequence.append_value(2)
    clock_sequence.append_value(3)

    assert clock_sequence.move_to_previous_value() == 3
    assert clock_sequence.move_to_previous_value() == 2
    assert clock_sequence.move_to_previous_value() == 1


def test_select_value_behavior() -> None:
    clock_sequence = CircularDoublyLinkedSequence[str]()
    clock_sequence.append_value("alpha")
    clock_sequence.append_value("beta")
    clock_sequence.append_value("gamma")

    assert clock_sequence.select_value("beta") is True
    assert clock_sequence.get_selected_value() == "beta"
    assert clock_sequence.select_value("missing") is False
    assert clock_sequence.get_selected_value() == "beta"
    assert clock_sequence.reset_to_first_value() == "alpha"


def test_previous_reference_and_next_reference_correctness() -> None:
    clock_sequence = CircularDoublyLinkedSequence[int]()
    clock_sequence.append_value(10)
    clock_sequence.append_value(20)
    clock_sequence.append_value(30)

    first_element = clock_sequence._first_element
    assert first_element is not None

    second_element = first_element.next_reference
    third_element = first_element.previous_reference

    assert second_element is not None
    assert third_element is not None

    assert first_element.previous_reference is third_element
    assert first_element.next_reference is second_element
    assert second_element.previous_reference is first_element
    assert second_element.next_reference is third_element
    assert third_element.previous_reference is second_element
    assert third_element.next_reference is first_element


def test_get_values_snapshot_behavior() -> None:
    clock_sequence = CircularDoublyLinkedSequence[str]()
    clock_sequence.append_value("sunrise")
    clock_sequence.append_value("noon")
    clock_sequence.append_value("night")

    initial_snapshot = clock_sequence.get_values_snapshot()
    clock_sequence.select_value("night")
    clock_sequence.move_to_next_value()
    later_snapshot = clock_sequence.get_values_snapshot()

    assert initial_snapshot == ["sunrise", "noon", "night"]
    assert later_snapshot == ["sunrise", "noon", "night"]

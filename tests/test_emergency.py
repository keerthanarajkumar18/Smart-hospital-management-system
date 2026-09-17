from hospital.emergency import EmergencyQueue


def test_lower_severity_has_higher_priority() -> None:
    """Verify that a lower severity number is processed first."""
    queue = EmergencyQueue()

    queue.push("Patient-3", severity=3)
    queue.push("Patient-1", severity=1)
    queue.push("Patient-2", severity=2)

    assert queue.pop().patient == "Patient-1"
    assert queue.pop().patient == "Patient-2"
    assert queue.pop().patient == "Patient-3"


def test_same_severity_uses_arrival_order() -> None:
    """Verify that same-severity emergencies use arrival order."""
    queue = EmergencyQueue()

    queue.push("Patient-A", severity=1)
    queue.push("Patient-B", severity=1)
    queue.push("Patient-C", severity=1)

    assert queue.pop().patient == "Patient-A"
    assert queue.pop().patient == "Patient-B"
    assert queue.pop().patient == "Patient-C"


def test_multiple_severity_levels() -> None:
    """Verify ordering across multiple severity levels."""
    queue = EmergencyQueue()

    queue.push("Patient-5", severity=5)
    queue.push("Patient-2", severity=2)
    queue.push("Patient-4", severity=4)
    queue.push("Patient-1", severity=1)
    queue.push("Patient-3", severity=3)

    result = [queue.pop().patient for _ in range(5)]

    assert result == [
        "Patient-1",
        "Patient-2",
        "Patient-3",
        "Patient-4",
        "Patient-5",
    ]


def test_empty_queue() -> None:
    """Verify that a new queue is empty."""
    queue = EmergencyQueue()

    assert queue.is_empty() is True


def test_queue_becomes_empty_after_pop() -> None:
    """Verify that the queue becomes empty after removing its only item."""
    queue = EmergencyQueue()

    queue.push("Patient-1", severity=1)

    assert queue.is_empty() is False

    queue.pop()

    assert queue.is_empty() is True


def test_same_severity_preserves_first_arrival() -> None:
    """Verify first arrival wins when severity is identical."""
    queue = EmergencyQueue()

    queue.push("First", severity=2)
    queue.push("Second", severity=2)

    first = queue.pop()
    second = queue.pop()

    assert first.patient == "First"
    assert second.patient == "Second"
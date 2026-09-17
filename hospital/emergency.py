"""Emergency priority queue implementation."""

import heapq
from dataclasses import dataclass
from itertools import count
from typing import Any


@dataclass
class EmergencyEntry:
    """Represent an emergency patient waiting for treatment."""

    severity: int
    sequence: int
    patient: Any


class EmergencyQueue:
    """Manage emergency patients using a severity-based min-heap."""

    def __init__(self) -> None:
        """Initialize an empty emergency queue."""
        self._queue: list[tuple[int, int, EmergencyEntry]] = []
        self._sequence = count()

    def push(self, patient: Any, severity: int) -> None:
        """Add an emergency patient to the queue."""
        sequence_number = next(self._sequence)

        entry = EmergencyEntry(
            severity=severity,
            sequence=sequence_number,
            patient=patient,
        )

        heapq.heappush(
            self._queue,
            (severity, sequence_number, entry),
        )

    def pop(self) -> EmergencyEntry:
        """Remove and return the highest-priority emergency."""
        _, _, entry = heapq.heappop(self._queue)
        return entry

    def is_empty(self) -> bool:
        """Return True when the emergency queue is empty."""
        return len(self._queue) == 0
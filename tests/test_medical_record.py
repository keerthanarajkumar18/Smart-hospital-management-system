import pytest
import inspect
from typing import Iterator

from hospital.medical_record import MedicalRecord, Visit


def test_append_visit() -> None:
    """Verify that a visit can be appended."""
    record = MedicalRecord()

    record.append_visit(
        visit_date="2026-09-16",
        doctor_id="D001",
        diagnosis="Fever",
        notes="Mild fever.",
    )

    history = record.get_history()

    assert len(history) == 1
    assert history[0].doctor_id == "D001"
    assert history[0].diagnosis == "Fever"


def test_multiple_visits_are_preserved() -> None:
    """Verify that multiple visits are retained."""
    record = MedicalRecord()

    record.append_visit(
        "2026-09-15",
        "D001",
        "Fever",
        "Mild fever.",
    )

    record.append_visit(
        "2026-09-16",
        "D002",
        "Infection",
        "Treatment started.",
    )

    history = record.get_history()

    assert len(history) == 2
    assert history[0].diagnosis == "Fever"
    assert history[1].diagnosis == "Infection"


def test_get_full_history() -> None:
    """Verify that full history returns all visits."""
    record = MedicalRecord()

    record.append_visit(
        "2026-09-15",
        "D001",
        "Fever",
        "Observation.",
    )

    record.append_visit(
        "2026-09-16",
        "D002",
        "Cough",
        "Medication prescribed.",
    )

    history = record.get_history()

    assert len(history) == 2


def test_filter_history_by_doctor() -> None:
    """Verify that history can be filtered by doctor."""
    record = MedicalRecord()

    record.append_visit(
        "2026-09-15",
        "D001",
        "Fever",
        "Observation.",
    )

    record.append_visit(
        "2026-09-16",
        "D002",
        "Cough",
        "Medication prescribed.",
    )

    record.append_visit(
        "2026-09-17",
        "D001",
        "Infection",
        "Follow-up.",
    )

    history = record.get_history_by_doctor("D001")

    assert len(history) == 2
    assert all(visit.doctor_id == "D001" for visit in history)


def test_empty_history() -> None:
    """Verify that a new medical record has no visits."""
    record = MedicalRecord()

    assert record.get_history() == []
    assert len(record) == 0


def test_visit_is_immutable() -> None:
    """Verify that an existing visit cannot be modified."""
    visit = Visit(
        visit_date="2026-09-16",
        doctor_id="D001",
        diagnosis="Fever",
        notes="Observation.",
    )

    with pytest.raises(AttributeError):
        visit.diagnosis = "Infection"

def test_stream_history_returns_generator() -> None:
    """Verify that stream_history returns a generator."""
    record = MedicalRecord()

    stream = record.stream_history()

    assert inspect.isgenerator(stream)

def test_stream_history_iteration() -> None:
    """Verify that streamed history can be iterated."""
    record = MedicalRecord()

    record.append_visit(
        "2026-09-15",
        "D001",
        "Fever",
        "Observation.",
    )

    record.append_visit(
        "2026-09-16",
        "D002",
        "Infection",
        "Treatment started.",
    )

    streamed_visits = list(record.stream_history())

    assert len(streamed_visits) == 2
    assert streamed_visits[0].diagnosis == "Fever"
    assert streamed_visits[1].diagnosis == "Infection"

def test_stream_history_empty() -> None:
    """Verify that streaming an empty history produces no visits."""
    record = MedicalRecord()

    streamed_visits = list(record.stream_history())

    assert streamed_visits == []

def stream_history_by_doctor(
    self,
    doctor_id: str,
) -> Iterator[Visit]:
    """Lazily stream visits handled by the specified doctor."""
    for visit in self._visits:
        if visit.doctor_id == doctor_id:
            yield visit

def test_filtered_stream_history() -> None:
    """Verify that history can be lazily streamed for one doctor."""
    record = MedicalRecord()

    record.append_visit(
        "2026-09-15",
        "D001",
        "Fever",
        "Observation.",
    )

    record.append_visit(
        "2026-09-16",
        "D002",
        "Cough",
        "Medication prescribed.",
    )

    record.append_visit(
        "2026-09-17",
        "D001",
        "Infection",
        "Follow-up.",
    )

    streamed_visits = list(
        record.stream_history_by_doctor("D001")
    )

    assert len(streamed_visits) == 2
    assert streamed_visits[0].doctor_id == "D001"
    assert streamed_visits[1].doctor_id == "D001"


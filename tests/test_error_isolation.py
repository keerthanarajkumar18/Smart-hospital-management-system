import pytest

from hospital.exceptions import (
    InvalidBillingError,
    PatientNotFoundError,
    SlotUnavailableError,
)
from hospital.service import HospitalService


def create_hospital(tmp_path, monkeypatch):
    """Create a hospital with one doctor and one patient."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        [
            "2026-09-16 10:00",
            "2026-09-16 11:00",
        ],
    )

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    return hospital

def test_scheduling_error_does_not_crash_test(
    tmp_path,
    monkeypatch,
):
    """Test that an invalid scheduling operation raises an error."""

    hospital = create_hospital(
        tmp_path,
        monkeypatch,
    )

    with pytest.raises(SlotUnavailableError):
        hospital.book_appointment(
            "A001",
            "P001",
            "D001",
            "2026-09-16 15:00",
        )

def test_double_booking_raises_exception(
    tmp_path,
    monkeypatch,
):
    """Test that double booking raises the correct exception."""

    hospital = create_hospital(
        tmp_path,
        monkeypatch,
    )

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    with pytest.raises(SlotUnavailableError):
        hospital.book_appointment(
            "A002",
            "P001",
            "D001",
            "2026-09-16 10:00",
        )

def test_missing_patient_raises_exception(
    tmp_path,
    monkeypatch,
):
    """Test that an unknown patient raises the correct exception."""

    hospital = create_hospital(
        tmp_path,
        monkeypatch,
    )

    with pytest.raises(PatientNotFoundError):
        hospital.book_appointment(
            "A001",
            "P999",
            "D001",
            "2026-09-16 10:00",
        )

def test_malformed_billing_input_raises_exception(
    tmp_path,
    monkeypatch,
):
    """Test that malformed billing input is rejected."""

    hospital = create_hospital(
        tmp_path,
        monkeypatch,
    )

    with pytest.raises(InvalidBillingError):
        hospital.generate_bill(
            "P001",
            500,
            "Blood Test",
            {},
        )

def test_emergency_works_after_scheduling_failure(
    tmp_path,
    monkeypatch,
):
    """Test that scheduling failure does not block emergencies."""

    hospital = create_hospital(
        tmp_path,
        monkeypatch,
    )

    # Cause a scheduling failure.
    with pytest.raises(SlotUnavailableError):
        hospital.book_appointment(
            "A001",
            "P001",
            "D001",
            "2026-09-16 15:00",
        )

    # Register another patient.
    hospital.register_patient(
        "P002",
        "Alice",
        25,
        "Female",
        "8888888888",
    )

    # Emergency admission should still work.
    result = hospital.admit_emergency(
        "P002",
        1,
    )

    assert result is True
    assert hospital.emergency_queue.is_empty() is False
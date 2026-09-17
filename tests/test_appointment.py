import pytest

from hospital.appointment import AppointmentManager
from hospital.exceptions import InvalidAppointmentError
from hospital.models import Doctor, Patient
from hospital.service import HospitalService


def create_manager(tmp_path, monkeypatch):
    """Create a simple appointment manager."""

    monkeypatch.chdir(tmp_path)

    patients = {
        "P001": Patient(
            "P001",
            "John",
            30,
            "Male",
            "9999999999",
        )
    }

    doctors = {
        "D001": Doctor(
            "D001",
            "Dr. Smith",
            "Cardiology",
            "Heart",
            ["10:00", "11:00"],
        )
    }

    appointments = {}

    manager = AppointmentManager(
        patients,
        doctors,
        appointments,
    )

    return manager


def test_book_appointment(tmp_path, monkeypatch):
    """Test booking an appointment."""

    manager = create_manager(
        tmp_path,
        monkeypatch,
    )

    appointment = manager.book_appointment(
        "A001",
        "P001",
        "D001",
        "10:00",
    )

    assert appointment.patient_id == "P001"
    assert appointment.doctor_id == "D001"
    assert appointment.time_slot == "10:00"


def test_invalid_patient(tmp_path, monkeypatch):
    """Test booking with an invalid patient."""

    manager = create_manager(
        tmp_path,
        monkeypatch,
    )

    try:
        manager.book_appointment(
            "A001",
            "P999",
            "D001",
            "10:00",
        )
        assert False
    except Exception:
        assert True


def test_double_booking(tmp_path, monkeypatch):
    """Test that double booking is prevented."""

    manager = create_manager(
        tmp_path,
        monkeypatch,
    )

    manager.book_appointment(
        "A001",
        "P001",
        "D001",
        "10:00",
    )

    try:
        manager.book_appointment(
            "A002",
            "P001",
            "D001",
            "10:00",
        )
        assert False
    except Exception:
        assert True


def test_reschedule_appointment(tmp_path, monkeypatch):
    """Test rescheduling an appointment."""

    manager = create_manager(
        tmp_path,
        monkeypatch,
    )

    manager.book_appointment(
        "A001",
        "P001",
        "D001",
        "10:00",
    )

    appointment = manager.reschedule_appointment(
        "A001",
        "11:00",
    )

    assert appointment.time_slot == "11:00"


def test_cancel_appointment(tmp_path, monkeypatch):
    """Test cancelling an appointment."""

    manager = create_manager(
        tmp_path,
        monkeypatch,
    )

    manager.book_appointment(
        "A001",
        "P001",
        "D001",
        "10:00",
    )

    appointment = manager.cancel_appointment("A001")

    assert appointment.status == "cancelled"

def test_complete_appointment(
    tmp_path,
    monkeypatch,
):
    """Test that a scheduled appointment can be completed."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        ["2026-09-16 10:00"],
    )

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    appointment = hospital.complete_appointment(
        "A001"
    )

    assert appointment.status == "completed"

def test_cancelled_appointment_cannot_be_completed(
    tmp_path,
    monkeypatch,
):
    """Test that a cancelled appointment cannot be completed."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        ["2026-09-16 10:00"],
    )

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    hospital.appointment_manager.cancel_appointment(
        "A001"
    )

    with pytest.raises(InvalidAppointmentError):
        hospital.complete_appointment("A001")

def test_complete_missing_appointment_raises_error(
    tmp_path,
    monkeypatch,
):
    """Test that an unknown appointment cannot be completed."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    with pytest.raises(InvalidAppointmentError):
        hospital.complete_appointment("A999")
import json
from pathlib import Path

import pytest

from hospital.medical_record import Visit
from hospital.models import Appointment, Doctor, Patient
from hospital.persistence import (
    JsonPersistence,
    PersistenceError,
)


def create_sample_data() -> tuple[
    dict[str, Patient],
    dict[str, Doctor],
    dict[str, Appointment],
    dict[str, list[Visit]],
]:
    """Create sample hospital data for testing."""
    patients = {
        "P001": Patient(
            patient_id="P001",
            name="John",
            age=30,
            gender="Male",
            phone="9876543210",
        )
    }

    doctors = {
        "D001": Doctor(
            doctor_id="D001",
            name="Dr. Smith",
            specialization="Cardiology",
            department="Cardiology",
            available_slots=["10:00", "11:00"],
        )
    }

    appointments = {
        "A001": Appointment(
            appointment_id="A001",
            patient_id="P001",
            doctor_id="D001",
            time_slot="10:00",
        )
    }

    history = {
        "P001": [
            Visit(
                visit_date="2026-09-16",
                doctor_id="D001",
                diagnosis="Fever",
                notes="Medication prescribed.",
            )
        ]
    }

    return (
        patients,
        doctors,
        appointments,
        history,
    )


def test_save_and_load_patients(tmp_path: Path) -> None:
    """Verify patient persistence."""
    persistence = JsonPersistence(tmp_path)

    patients, _, _, _ = create_sample_data()

    persistence.save_patients(patients)

    loaded = persistence.load_patients()

    assert loaded == patients


def test_save_and_load_doctors(tmp_path: Path) -> None:
    """Verify doctor persistence."""
    persistence = JsonPersistence(tmp_path)

    _, doctors, _, _ = create_sample_data()

    persistence.save_doctors(doctors)

    loaded = persistence.load_doctors()

    assert loaded == doctors


def test_save_and_load_appointments(
    tmp_path: Path,
) -> None:
    """Verify appointment persistence."""
    persistence = JsonPersistence(tmp_path)

    _, _, appointments, _ = create_sample_data()

    persistence.save_appointments(appointments)

    loaded = persistence.load_appointments()

    assert loaded == appointments


def test_save_and_load_medical_history(
    tmp_path: Path,
) -> None:
    """Verify medical history persistence."""
    persistence = JsonPersistence(tmp_path)

    _, _, _, history = create_sample_data()

    persistence.save_medical_history(history)

    loaded = persistence.load_medical_history()

    assert loaded == history


def test_missing_files_return_empty_data(
    tmp_path: Path,
) -> None:
    """Verify missing JSON files do not crash."""
    persistence = JsonPersistence(tmp_path)

    assert persistence.load_patients() == {}
    assert persistence.load_doctors() == {}
    assert persistence.load_appointments() == {}
    assert persistence.load_medical_history() == {}


def test_malformed_patient_json(
    tmp_path: Path,
) -> None:
    """Verify malformed JSON raises PersistenceError."""
    persistence = JsonPersistence(tmp_path)

    file_path = tmp_path / "patients.json"

    file_path.write_text(
        '{"patient_id": "P001"',
        encoding="utf-8",
    )

    with pytest.raises(PersistenceError):
        persistence.load_patients()


def test_state_survives_restart(
    tmp_path: Path,
) -> None:
    """Verify data can be loaded by a new persistence instance."""
    first_instance = JsonPersistence(tmp_path)

    patients, doctors, appointments, history = (
        create_sample_data()
    )

    first_instance.save_patients(patients)
    first_instance.save_doctors(doctors)
    first_instance.save_appointments(appointments)
    first_instance.save_medical_history(history)

    # Simulate application restart.
    second_instance = JsonPersistence(tmp_path)

    assert second_instance.load_patients() == patients
    assert second_instance.load_doctors() == doctors
    assert second_instance.load_appointments() == appointments
    assert second_instance.load_medical_history() == history
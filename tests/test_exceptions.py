import pytest

from hospital.exceptions import (
    DoctorNotFoundError,
    HospitalError,
    InvalidAppointmentError,
    InvalidBillingError,
    PatientNotFoundError,
    SlotUnavailableError,
)


def test_patient_not_found_error() -> None:
    """Verify PatientNotFoundError can be raised and caught."""
    with pytest.raises(PatientNotFoundError):
        raise PatientNotFoundError("Patient not found.")


def test_doctor_not_found_error() -> None:
    """Verify DoctorNotFoundError can be raised and caught."""
    with pytest.raises(DoctorNotFoundError):
        raise DoctorNotFoundError("Doctor not found.")


def test_slot_unavailable_error() -> None:
    """Verify SlotUnavailableError can be raised and caught."""
    with pytest.raises(SlotUnavailableError):
        raise SlotUnavailableError("Slot unavailable.")


def test_invalid_appointment_error() -> None:
    """Verify InvalidAppointmentError can be raised and caught."""
    with pytest.raises(InvalidAppointmentError):
        raise InvalidAppointmentError("Invalid appointment.")


def test_invalid_billing_error() -> None:
    """Verify InvalidBillingError can be raised and caught."""
    with pytest.raises(InvalidBillingError):
        raise InvalidBillingError("Invalid billing information.")


def test_all_errors_inherit_from_hospital_error() -> None:
    """Verify all custom errors inherit from HospitalError."""
    errors = [
        PatientNotFoundError,
        DoctorNotFoundError,
        SlotUnavailableError,
        InvalidAppointmentError,
        InvalidBillingError,
    ]

    for error_type in errors:
        assert issubclass(error_type, HospitalError)
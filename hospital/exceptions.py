"""Custom exception hierarchy for the hospital management system."""


class HospitalError(Exception):
    """Base exception for all hospital management system errors."""

class PatientNotFoundError(HospitalError):
    """Raised when a requested patient does not exist."""

class DoctorNotFoundError(HospitalError):
    """Raised when a requested doctor does not exist."""

class SlotUnavailableError(HospitalError):
    """Raised when a requested doctor appointment slot is unavailable."""

class InvalidAppointmentError(HospitalError):
    """Raised when appointment information or an appointment operation is invalid."""

class InvalidBillingError(HospitalError):
    """Raised when billing information is invalid."""


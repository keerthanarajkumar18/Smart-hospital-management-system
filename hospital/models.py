"""Core domain models for the hospital management system."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Patient:
    """Represent a registered hospital patient."""

    patient_id: str
    name: str
    age: int
    gender: str
    phone: str
    medical_history: Any = None


@dataclass
class Doctor:
    """Represent a doctor and their available appointment slots."""

    doctor_id: str
    name: str
    specialization: str
    department: str
    available_slots: list[str] = field(default_factory=list)


@dataclass
class Appointment:
    """Represent a scheduled appointment between a patient and doctor."""

    appointment_id: str
    patient_id: str
    doctor_id: str
    time_slot: str
    status: str = "scheduled"
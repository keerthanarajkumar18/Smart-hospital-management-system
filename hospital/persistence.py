"""JSON persistence for the hospital management system."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from hospital.medical_record import Visit
from hospital.models import Appointment, Doctor, Patient


class PersistenceError(Exception):
    """Raised when JSON persistence operations fail."""


class JsonPersistence:
    """Save and load hospital data using JSON files."""

    def __init__(self, data_directory: str | Path) -> None:
        """Initialize the persistence layer."""
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _save_json(
        self,
        filename: str,
        data: Any,
    ) -> None:
        """Save data to a JSON file."""
        file_path = self.data_directory / filename

        try:
            with file_path.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                )
        except (OSError, TypeError) as exc:
            raise PersistenceError(
                f"Unable to save {filename}."
            ) from exc

    def _load_json(
        self,
        filename: str,
    ) -> Any:
        """Load data from a JSON file."""
        file_path = self.data_directory / filename

        if not file_path.exists():
            if filename == "medical_history.json":
                return {}
            return []

        try:
            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)
        except json.JSONDecodeError as exc:
            raise PersistenceError(
                f"Malformed JSON in {filename}."
            ) from exc
        except OSError as exc:
            raise PersistenceError(
                f"Unable to read {filename}."
            ) from exc

    def save_patients(
        self,
        patients: dict[str, Patient],
    ) -> None:
        """Save patients to JSON."""
        data = [
            asdict(patient)
            for patient in patients.values()
        ]

        self._save_json(
            "patients.json",
            data,
        )

    def load_patients(self) -> dict[str, Patient]:
        """Load patients from JSON."""
        data = self._load_json("patients.json")

        return {
            item["patient_id"]: Patient(**item)
            for item in data
        }

    def save_doctors(
        self,
        doctors: dict[str, Doctor],
    ) -> None:
        """Save doctors to JSON."""
        data = [
            asdict(doctor)
            for doctor in doctors.values()
        ]

        self._save_json(
            "doctors.json",
            data,
        )

    def load_doctors(self) -> dict[str, Doctor]:
        """Load doctors from JSON."""
        data = self._load_json("doctors.json")

        return {
            item["doctor_id"]: Doctor(**item)
            for item in data
        }

    def save_appointments(
        self,
        appointments: dict[str, Appointment],
    ) -> None:
        """Save appointments to JSON."""
        data = [
            asdict(appointment)
            for appointment in appointments.values()
        ]

        self._save_json(
            "appointments.json",
            data,
        )

    def load_appointments(
        self,
    ) -> dict[str, Appointment]:
        """Load appointments from JSON."""
        data = self._load_json("appointments.json")

        return {
            item["appointment_id"]: Appointment(**item)
            for item in data
        }

    def save_medical_history(
        self,
        medical_history: dict[str, list[Visit]],
    ) -> None:
        """Save medical histories to JSON."""
        data = {
            patient_id: [
                asdict(visit)
                for visit in visits
            ]
            for patient_id, visits in medical_history.items()
        }

        self._save_json(
            "medical_history.json",
            data,
        )

    def load_medical_history(
        self,
    ) -> dict[str, list[Visit]]:
        """Load medical histories from JSON."""
        data = self._load_json("medical_history.json")

        return {
            patient_id: [
                Visit(**visit)
                for visit in visits
            ]
            for patient_id, visits in data.items()
        }
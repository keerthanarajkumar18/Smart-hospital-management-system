"""Medical record management for the hospital system."""
import os
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator

@dataclass(frozen=True) #frozen=True means once a visit is created, its fields cannot be changed.
class Visit:
    """Represent one visit in a patient's medical history."""

    visit_date: str
    doctor_id: str
    diagnosis: str
    notes: str

class MedicalRecordFile:
    """Safely write medical records to a file."""

    def __init__(
        self,
        file_path: str | Path,
        visits: list[Visit],
    ) -> None:
        """Initialize the file context manager."""
        self.file_path = Path(file_path)
        self.visits = visits
        self.temp_path: Path | None = None

    def __enter__(self) -> "MedicalRecordFile":
        """Prepare a temporary file for safe writing."""
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=self.file_path.parent,
        )

        temp_file.close()
        self.temp_path = Path(temp_file.name)

        return self

    def write_records(self) -> None:
        """Write all medical records to the temporary file."""
        if self.temp_path is None:
            raise RuntimeError(
                "MedicalRecordFile must be used with a context manager."
            )

        with self.temp_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            for visit in self.visits:
                file.write(
                    f"{visit.visit_date}|"
                    f"{visit.doctor_id}|"
                    f"{visit.diagnosis}|"
                    f"{visit.notes}\n"
                )

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool:
        """Replace the original file only when writing succeeds."""
        if self.temp_path is None:
            return False

        try:
            if exc_type is None:
                os.replace(
                    self.temp_path,
                    self.file_path,
                )
            else:
                self.temp_path.unlink(
                    missing_ok=True,
                )
        except Exception:
            self.temp_path.unlink(
                missing_ok=True,
            )
            raise

        return False

class MedicalRecord:
    """Maintain an append-only history of patient visits."""

    def __init__(self) -> None:
        """Initialize an empty medical record."""
        self._visits: list[Visit] = []

    def append_visit(
        self,
        visit_date: str,
        doctor_id: str,
        diagnosis: str,
        notes: str,
    ) -> None:
        """Append a new visit to the patient's medical history."""
        visit = Visit(
            visit_date=visit_date,
            doctor_id=doctor_id,
            diagnosis=diagnosis,
            notes=notes,
        )

        self._visits.append(visit)

    def get_history(self) -> list[Visit]:
        """Return the complete medical history."""
        return list(self._visits)

    def get_history_by_doctor(self, doctor_id: str) -> list[Visit]:
        """Return visits handled by the specified doctor."""
        return [
            visit
            for visit in self._visits
            if visit.doctor_id == doctor_id
        ]

    def stream_history_by_doctor(
        self,
        doctor_id: str,
    ) -> Iterator[Visit]:
        """Lazily stream visits handled by the specified doctor."""
        for visit in self._visits:
            if visit.doctor_id == doctor_id:
                yield visit

    def stream_history(self) -> Iterator[Visit]:
        """Lazily stream all visits in chronological insertion order."""
        yield from self._visits

    def __len__(self) -> int:
        """Return the number of visits in the medical history."""
        return len(self._visits)

    def get_history_by_date(
    self,
    visit_date: str,
    ) -> list[Visit]:
        """Return visits recorded on the specified date."""

        return [
            visit
            for visit in self._visits
            if visit.visit_date == visit_date
        ]

    def stream_history_by_date(
    self,
    visit_date: str,
    ) -> Iterator[Visit]:
        """Lazily stream visits from the specified date."""

        for visit in self._visits:
            if visit.visit_date == visit_date:
                yield visit
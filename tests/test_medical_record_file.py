from pathlib import Path

import pytest

from hospital.medical_record import MedicalRecord, MedicalRecordFile


def create_record() -> MedicalRecord:
    """Create a sample medical record for testing."""
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

    return record


def test_successful_write(tmp_path: Path) -> None:
    """Verify that medical records are written successfully."""
    record = create_record()

    file_path = tmp_path / "history.txt"

    with MedicalRecordFile(
        file_path,
        record.get_history(),
    ) as file:
        file.write_records()

    assert file_path.exists()

    content = file_path.read_text(encoding="utf-8")

    assert "2026-09-15|D001|Fever|Observation." in content
    assert "2026-09-16|D002|Infection|Treatment started." in content


def test_successful_write_replaces_old_file(
    tmp_path: Path,
) -> None:
    """Verify that successful writing replaces existing content."""
    record = create_record()

    file_path = tmp_path / "history.txt"

    file_path.write_text(
        "OLD CONTENT\n",
        encoding="utf-8",
    )

    with MedicalRecordFile(
        file_path,
        record.get_history(),
    ) as file:
        file.write_records()

    content = file_path.read_text(encoding="utf-8")

    assert "OLD CONTENT" not in content
    assert "Fever" in content


def test_failed_write_preserves_original_file(
    tmp_path: Path,
) -> None:
    """Verify that a failed write does not modify the original file."""
    record = create_record()

    file_path = tmp_path / "history.txt"

    original_content = "ORIGINAL CONTENT\n"

    file_path.write_text(
        original_content,
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError):
        with MedicalRecordFile(
            file_path,
            record.get_history(),
        ) as file:
            file.write_records()

            raise RuntimeError(
                "Simulated write failure"
            )

    assert file_path.read_text(
        encoding="utf-8"
    ) == original_content


def test_failed_write_does_not_leave_temporary_file(
    tmp_path: Path,
) -> None:
    """Verify that temporary files are cleaned up after failure."""
    record = create_record()

    file_path = tmp_path / "history.txt"

    file_path.write_text(
        "ORIGINAL CONTENT\n",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError):
        with MedicalRecordFile(
            file_path,
            record.get_history(),
        ) as file:
            file.write_records()

            raise RuntimeError(
                "Simulated write failure"
            )

    files = list(tmp_path.iterdir())

    assert files == [file_path]

def test_empty_records_create_empty_file(tmp_path):
    """Test writing an empty medical record."""

    file_path = tmp_path / "medical_history.txt"

    with MedicalRecordFile(file_path, []) as record_file:
        record_file.write_records()

    assert file_path.exists()
    assert file_path.read_text() == ""
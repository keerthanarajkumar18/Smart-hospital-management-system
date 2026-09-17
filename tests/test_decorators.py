from hospital.decorators import audit_log
from hospital.logger import HospitalLogger


class DemoService:
    """Simple class for testing the audit decorator."""

    def __init__(self):
        self.logger = HospitalLogger()

    @audit_log
    def book_appointment(self, user):
        """Test appointment operation."""
        return "Appointment booked"


def test_audit_log_records_operation(tmp_path, monkeypatch):
    """Test that the decorator creates an audit log."""

    monkeypatch.chdir(tmp_path)

    service = DemoService()

    result = service.book_appointment("Receptionist")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert result == "Appointment booked"
    assert "AUDIT" in content
    assert "Receptionist" in content
    assert "book_appointment" in content

def test_audit_records_user(tmp_path, monkeypatch):
    """Test that the user is recorded."""

    monkeypatch.chdir(tmp_path)

    service = DemoService()

    service.book_appointment("Doctor")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "Doctor" in content

def test_audit_records_operation(tmp_path, monkeypatch):
    """Test that the operation name is recorded."""

    monkeypatch.chdir(tmp_path)

    service = DemoService()

    service.book_appointment("Receptionist")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "book_appointment" in content

def test_audit_returns_function_result(tmp_path, monkeypatch):
    """Test that the decorated function still returns its result."""

    monkeypatch.chdir(tmp_path)

    service = DemoService()

    result = service.book_appointment("Receptionist")

    assert result == "Appointment booked"

def test_audit_entry_is_created(tmp_path, monkeypatch):
    """Test that an audit entry is written."""

    monkeypatch.chdir(tmp_path)

    service = DemoService()

    service.book_appointment("Receptionist")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "AUDIT" in content


from hospital.logger import HospitalLogger


def test_logger_creates_log_file(tmp_path, monkeypatch):
    """Test that the log file is created."""

    monkeypatch.chdir(tmp_path)

    logger = HospitalLogger()
    logger.patient_registered("P001")

    log_file = tmp_path / "logs" / "hospital.log"

    assert log_file.exists()


def test_patient_registration_is_logged(tmp_path, monkeypatch):
    """Test that patient registration is logged."""

    monkeypatch.chdir(tmp_path)

    logger = HospitalLogger()
    logger.patient_registered("P001")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "Patient registered: P001" in content


def test_appointment_events_are_logged(tmp_path, monkeypatch):
    """Test that appointment events are logged."""

    monkeypatch.chdir(tmp_path)

    logger = HospitalLogger()

    logger.appointment_booked("A001", "P001", "D001")
    logger.appointment_rescheduled("A001", "11:00")
    logger.appointment_cancelled("A001")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "Appointment booked: A001" in content
    assert "Appointment rescheduled: A001" in content
    assert "Appointment cancelled: A001" in content


def test_emergency_and_billing_are_logged(tmp_path, monkeypatch):
    """Test that emergency and billing events are logged."""

    monkeypatch.chdir(tmp_path)

    logger = HospitalLogger()

    logger.emergency_admitted("P002", 1)
    logger.billing_generated("P001", 1500.00)

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "Emergency admitted: P002" in content
    assert "Billing generated: Patient: P001" in content


def test_error_is_logged(tmp_path, monkeypatch):
    """Test that errors are logged."""

    monkeypatch.chdir(tmp_path)

    logger = HospitalLogger()
    logger.error("Patient P999 was not found.")

    log_file = tmp_path / "logs" / "hospital.log"
    content = log_file.read_text()

    assert "ERROR" in content
    assert "Patient P999 was not found." in content
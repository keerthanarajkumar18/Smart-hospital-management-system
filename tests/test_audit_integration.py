from hospital.service import HospitalService


def test_booking_creates_audit_log(
    tmp_path,
    monkeypatch,
):
    """Test that booking creates an audit log."""

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
        user="Receptionist",
    )

    log_file = tmp_path / "logs" / "hospital.log"

    content = log_file.read_text()

    assert "AUDIT" in content
    assert "Receptionist" in content
    assert "book_appointment" in content

def test_emergency_creates_audit_log(
    tmp_path,
    monkeypatch,
):
    """Test that emergency admission creates an audit log."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.admit_emergency(
        "P001",
        1,
        user="Emergency Desk",
    )

    log_file = tmp_path / "logs" / "hospital.log"

    content = log_file.read_text()

    assert "AUDIT" in content
    assert "Emergency Desk" in content
    assert "admit_emergency" in content

def test_billing_creates_audit_log(
    tmp_path,
    monkeypatch,
):
    """Test that billing creates an audit log."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.generate_bill(
        "P001",
        500,
        {"Blood Test": 200},
        {"ECG": 300},
        user="Billing Desk",
    )

    log_file = tmp_path / "logs" / "hospital.log"

    content = log_file.read_text()

    assert "AUDIT" in content
    assert "Billing Desk" in content
    assert "generate_bill" in content


from hospital.service import HospitalService


def create_hospital():
    """Create a hospital service for testing."""

    hospital = HospitalService()

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        ["10:00", "11:00"],
    )

    return hospital


def test_register_patient():
    """Test patient registration."""

    hospital = create_hospital()

    patient = hospital.register_patient(
        "P009",
        "John",
        30,
        "Male",
        "9976325899",
    )

    assert patient.name == "John"
    assert "P009" in hospital.patients


def test_book_appointment(tmp_path, monkeypatch):
    """Test booking an appointment."""

    monkeypatch.chdir(tmp_path)

    hospital = create_hospital()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    appointment = hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "10:00",
    )

    assert appointment.patient_id == "P001"
    assert "A001" in hospital.appointments


def test_admit_emergency(tmp_path, monkeypatch):
    """Test emergency admission."""

    monkeypatch.chdir(tmp_path)

    hospital = create_hospital()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    result = hospital.admit_emergency(
        "P001",
        1,
    )

    assert result is True
    assert hospital.emergency_queue.is_empty() is False


def test_generate_bill(tmp_path, monkeypatch):
    """Test bill generation."""

    monkeypatch.chdir(tmp_path)

    hospital = create_hospital()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    bill = hospital.generate_bill(
        "P001",
        500,
        {"Blood Test": 200},
        {"X-Ray": 300},
    )

    assert bill.total == 1000

def test_get_reports(tmp_path, monkeypatch):
    """Test hospital reports."""

    monkeypatch.chdir(tmp_path)

    hospital = create_hospital()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    reports = hospital.get_reports()

    assert "patients_seen_per_day" in reports
    assert "doctor_utilization" in reports
    assert "revenue_collected" in reports
    assert "average_emergency_wait_time" in reports
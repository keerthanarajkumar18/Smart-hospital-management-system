from hospital.models import Appointment, Doctor, Patient
from hospital.reports import ReportService
from hospital.billing import Bill
from hospital.service import HospitalService


def create_report_service():
    """Create sample data for report testing."""

    patients = {
        "P001": Patient(
            "P001",
            "John",
            30,
            "Male",
            "9999999999",
        ),
        "P002": Patient(
            "P002",
            "Alice",
            25,
            "Female",
            "8888888888",
        ),
    }

    doctors = {
        "D001": Doctor(
            "D001",
            "Dr. Smith",
            "Cardiology",
            "Heart",
            [],
        ),
        "D002": Doctor(
            "D002",
            "Dr. Jones",
            "Neurology",
            "Brain",
            [],
        ),
    }

    appointments = {
        "A001": Appointment(
            "A001",
            "P001",
            "D001",
            "2026-09-16 10:00",
            "completed",
        ),
        "A002": Appointment(
            "A002",
            "P002",
            "D001",
            "2026-09-16 11:00",
            "completed",
        ),
        "A003": Appointment(
            "A003",
            "P001",
            "D002",
            "2026-09-17 10:00",
            "completed",
        ),
        "A004": Appointment(
            "A004",
            "P002",
            "D001",
            "2026-09-16 12:00",
            "cancelled",
        ),
    }

    bills = {
        "P001": Bill(
            500,
            {"Blood Test": 200},
            {},
            700,
        ),
        "P002": Bill(
            500,
            {},
            {"X-Ray": 300},
            800,
        ),
    }

    emergency_records = []

    return ReportService(
        patients,
        doctors,
        appointments,
        bills,
        emergency_records,
    )

def test_doctor_utilization():
    """Test doctor appointment utilization."""

    service = create_report_service()

    result = service.doctor_utilization()

    assert result["D001"] == 2
    assert result["D002"] == 1

def test_doctor_utilization():
    """Test doctor appointment count."""

    doctors = {
        "D001": Doctor(
            "D001",
            "Dr. Smith",
            "Cardiology",
            "Heart",
            [],
        )
    }

    appointments = {
        "A001": Appointment(
            "A001",
            "P001",
            "D001",
            "10:00",
            "scheduled",
        ),
        "A002": Appointment(
            "A002",
            "P002",
            "D001",
            "11:00",
            "completed",
        ),
    }

    report = ReportService(
        {},
        doctors,
        appointments,
        {},
        [],
    )

    result = report.doctor_utilization()

    assert result["D001"] == 2


def test_revenue_collected():
    """Test total hospital revenue."""

    class SimpleBill:
        """Simple bill used for testing."""

        def __init__(self, total):
            self.total = total

    bills = {
        "P001": SimpleBill(1000),
        "P002": SimpleBill(1500),
    }

    report = ReportService(
        {},
        {},
        {},
        bills,
        [],
    )

    result = report.revenue_collected()

    assert result == 2500


def test_average_emergency_wait_time():
    """Test average emergency waiting time."""

    emergency_records = [
        {
            "patient_id": "P001",
            "severity": 1,
            "arrival_time": "2026-09-16T08:00:00",
            "served_time": "2026-09-16T08:10:00",
        },
        {
            "patient_id": "P002",
            "severity": 2,
            "arrival_time": "2026-09-16T08:00:00",
            "served_time": "2026-09-16T08:30:00",
        },
    ]

    report = ReportService(
        {},
        {},
        {},
        {},
        emergency_records,
    )

    result = report.average_emergency_wait_time()

    assert result == "00:20:00"


def test_all_reports():
    """Test structured report output."""

    report = ReportService(
        {},
        {},
        {},
        {},
        [],
    )

    result = report.get_all_reports(
        "2026-09-16"
    )

    assert "patients_seen_per_day" in result
    assert "doctor_utilization" in result
    assert "revenue_collected" in result
    assert "average_emergency_wait_time" in result

def test_patients_seen_per_day_with_no_completed_appointments():
    """Test daily patient count when no patients were seen."""

    service = create_report_service()

    result = service.patients_seen_per_day(
        "2026-09-18"
    )

    assert result == 0

def test_completed_appointment_is_counted_as_patient_seen(
    tmp_path,
    monkeypatch,
):
    """Test that completed appointments count as patients seen."""

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
    )

    hospital.complete_appointment("A001")

    reports = hospital.get_reports(
        "2026-09-16"
    )

    assert reports["patients_seen_per_day"] == 1
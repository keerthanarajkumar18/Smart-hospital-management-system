import csv

from hospital.service import HospitalService


def test_daily_report_csv_is_created(
    tmp_path,
    monkeypatch,
):
    """Test that daily_report.csv is created."""

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
    )

    file_path = hospital.export_daily_report(
        "2026-09-16"
    )

    assert file_path.exists()
    assert file_path.name == "daily_report.csv"

def test_daily_report_csv_contains_reports(
    tmp_path,
    monkeypatch,
):
    """Test that CSV contains all required reports."""

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
    )

    file_path = hospital.export_daily_report(
        "2026-09-16"
    )

    with file_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.reader(file)
        )

    assert rows[0] == [
        "Report",
        "Value",
    ]

    assert rows[1][0] == "Patients Seen"
    assert rows[2][0] == "Doctor Utilization"
    assert rows[3][0] == "Revenue Collected"
    assert rows[4][0] == "Average Wait Time"

def test_daily_report_csv_contains_revenue(
    tmp_path,
    monkeypatch,
):
    """Test that CSV contains the correct revenue."""

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
    )

    file_path = hospital.export_daily_report(
        "2026-09-16"
    )

    with file_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.reader(file)
        )

    revenue_row = rows[3]

    assert revenue_row[0] == "Revenue Collected"
    assert float(revenue_row[1]) == 1000.0

def test_daily_report_csv_can_be_read(
    tmp_path,
    monkeypatch,
):
    """Test that the generated CSV can be opened and read."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    file_path = hospital.export_daily_report(
        "2026-09-16"
    )

    with file_path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.reader(file)

        rows = list(reader)

    assert len(rows) == 5
    assert rows[0] == [
        "Report",
        "Value",
    ]


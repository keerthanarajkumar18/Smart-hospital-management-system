from hospital.service import HospitalService


def test_full_hospital_day(tmp_path, monkeypatch):
    """Test scheduled and emergency workflow together."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    # --------------------------------------------------
    # 1. Add doctors
    # --------------------------------------------------

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        [
            "2026-09-16 10:00",
            "2026-09-16 11:00",
        ],
    )

    hospital.add_doctor(
        "D002",
        "Dr. Jones",
        "Neurology",
        "Brain",
        [
            "2026-09-16 10:00",
            "2026-09-16 11:00",
        ],
    )

    # --------------------------------------------------
    # 2. Register patients
    # --------------------------------------------------

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.register_patient(
        "P002",
        "Alice",
        25,
        "Female",
        "8888888888",
    )

    hospital.register_patient(
        "P003",
        "Robert",
        45,
        "Male",
        "7777777777",
    )

    # --------------------------------------------------
    # 3. Book scheduled appointments
    # --------------------------------------------------

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    hospital.book_appointment(
        "A002",
        "P002",
        "D002",
        "2026-09-16 10:00",
    )

    assert hospital.appointments["A001"].status == "scheduled"
    assert hospital.appointments["A002"].status == "scheduled"

    # --------------------------------------------------
    # 4. Emergency patients arrive
    # --------------------------------------------------

    hospital.admit_emergency(
        "P003",
        1,
    )

    hospital.admit_emergency(
        "P002",
        2,
    )

    # --------------------------------------------------
    # 5. Emergencies are processed first
    # --------------------------------------------------

    first = hospital.process_emergency()
    second = hospital.process_emergency()

    assert first.patient_id == "P003"
    assert second.patient_id == "P002"

    # Emergency queue should now be empty
    assert hospital.emergency_queue.is_empty()

    # --------------------------------------------------
    # 6. Scheduled appointments continue
    # --------------------------------------------------

    completed = hospital.complete_appointment("A001")

    assert completed.status == "completed"

    # --------------------------------------------------
    # 7. Medical history is updated
    # --------------------------------------------------

    hospital.add_medical_history(
        "P003",
        "2026-09-16",
        "D001",
        "Chest pain",
        "ECG recommended.",
    )

    # --------------------------------------------------
    # 8. Generate bill
    # --------------------------------------------------

    bill = hospital.generate_bill(
        "P003",
        500,
        {"Blood Test": 200},
        {"ECG": 300},
    )

    assert bill.total == 1000

    # --------------------------------------------------
    # 9. Generate reports
    # --------------------------------------------------

    reports = hospital.get_reports(
        "2026-09-16"
    )

    assert reports["patients_seen_per_day"] == 1
    assert reports["revenue_collected"] == 1000

def test_emergency_is_served_before_scheduled_appointment(
    tmp_path,
    monkeypatch,
):
    """Verify emergency patients are processed before scheduled patients."""

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
        "Scheduled Patient",
        30,
        "Male",
        "9999999999",
    )

    hospital.register_patient(
        "P002",
        "Emergency Patient",
        40,
        "Female",
        "8888888888",
    )

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    hospital.admit_emergency(
        "P002",
        1,
    )

    # Emergency is processed first.
    emergency_patient = hospital.process_emergency()

    assert emergency_patient.patient_id == "P002"

    # Scheduled appointment still remains scheduled.
    assert hospital.appointments["A001"].status == "scheduled"

    # Scheduled appointment can then be completed.
    hospital.complete_appointment("A001")

    assert hospital.appointments["A001"].status == "completed"


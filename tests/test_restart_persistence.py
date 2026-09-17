from hospital.service import HospitalService


def test_patient_persists_after_restart(
    tmp_path,
    monkeypatch,
):
    """Verify patients survive a service restart."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    # Simulate application restart.
    restarted_hospital = HospitalService()

    assert "P001" in restarted_hospital.patients

    patient = restarted_hospital.patients["P001"]

    assert patient.name == "John"
    assert patient.age == 30

def test_doctor_persists_after_restart(
    tmp_path,
    monkeypatch,
):
    """Verify doctors survive a service restart."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

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

    restarted_hospital = HospitalService()

    assert "D001" in restarted_hospital.doctors

    doctor = restarted_hospital.doctors["D001"]

    assert doctor.name == "Dr. Smith"
    assert doctor.specialization == "Cardiology"
    assert doctor.department == "Heart"
    assert "2026-09-16 10:00" in doctor.available_slots

def test_appointment_persists_after_restart(
    tmp_path,
    monkeypatch,
):
    """Verify appointments survive a service restart."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.add_doctor(
        "D001",
        "Dr. Smith",
        "Cardiology",
        "Heart",
        ["2026-09-16 10:00"],
    )

    hospital.book_appointment(
        "A001",
        "P001",
        "D001",
        "2026-09-16 10:00",
    )

    restarted_hospital = HospitalService()

    assert "A001" in restarted_hospital.appointments

    appointment = restarted_hospital.appointments["A001"]

    assert appointment.patient_id == "P001"
    assert appointment.doctor_id == "D001"
    assert appointment.time_slot == "2026-09-16 10:00"
    assert appointment.status == "scheduled"

def test_medical_history_persists_after_restart(
    tmp_path,
    monkeypatch,
):
    """Verify medical history survives a service restart."""

    monkeypatch.chdir(tmp_path)

    hospital = HospitalService()

    hospital.register_patient(
        "P001",
        "John",
        30,
        "Male",
        "9999999999",
    )

    hospital.add_medical_history(
        "P001",
        "2026-09-16",
        "D001",
        "Fever",
        "Patient advised to rest.",
    )

    restarted_hospital = HospitalService()

    assert "P001" in restarted_hospital.medical_records

    history = (
        restarted_hospital
        .medical_records["P001"]
        .get_history()
    )

    assert len(history) == 1
    assert history[0].doctor_id == "D001"
    assert history[0].diagnosis == "Fever"
    assert history[0].notes == "Patient advised to rest."


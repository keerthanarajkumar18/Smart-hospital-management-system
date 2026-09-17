from hospital.models import Appointment, Doctor, Patient


def test_patient_creation() -> None:
    """Verify that a patient can be created."""
    patient = Patient(
        patient_id="P001",
        name="John",
        age=35,
        gender="Male",
        phone="9876543210",
    )

    assert patient.patient_id == "P001"
    assert patient.name == "John"
    assert patient.age == 35


def test_doctor_creation() -> None:
    """Verify that a doctor can be created."""
    doctor = Doctor(
        doctor_id="D001",
        name="Dr. Kumar",
        specialization="Cardiology",
        department="Cardiology",
    )

    assert doctor.doctor_id == "D001"
    assert doctor.specialization == "Cardiology"


def test_appointment_creation() -> None:
    """Verify that an appointment can be created."""
    appointment = Appointment(
        appointment_id="A001",
        patient_id="P001",
        doctor_id="D001",
        time_slot="10:00",
    )

    assert appointment.appointment_id == "A001"
    assert appointment.patient_id == "P001"
    assert appointment.status == "scheduled"

def test_doctors_have_independent_slot_lists() -> None:
    """Verify that each doctor gets a separate slot list."""
    doctor1 = Doctor(
        doctor_id="D001",
        name="Dr. Kumar",
        specialization="Cardiology",
        department="Cardiology",
    )

    doctor2 = Doctor(
        doctor_id="D002",
        name="Dr. Priya",
        specialization="Neurology",
        department="Neurology",
    )

    doctor1.available_slots.append("09:00")

    assert doctor1.available_slots == ["09:00"]
    assert doctor2.available_slots == []

def test_patient_medical_history_defaults_to_none() -> None:
    """Verify that a patient starts without a medical record reference."""
    patient = Patient(
        patient_id="P002",
        name="Alice",
        age=28,
        gender="Female",
        phone="9123456780",
    )

    assert patient.medical_history is None
"""Console application for the hospital management system."""

from hospital.exceptions import HospitalError
from hospital.service import HospitalService
from hospital.billing import (StandardBilling, InsuranceBilling,)
from hospital.exceptions import (PatientNotFoundError, InvalidBillingError,)

def display_menu() -> None:
    """Display the main application menu."""

    print("\n" + "=" * 50)
    print("       SMART HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 50)

    print("1. Register Patient")
    print("2. Add Doctor")
    print("3. Book Appointment")
    print("4. Reschedule Appointment")
    print("5. Cancel Appointment")
    print("6. Admit Emergency")
    print("7. Process Emergency")
    print("8. Complete Appointment")
    print("9. Add Medical History")
    print("10. View Medical History")
    print("11. Generate Bill")
    print("12. View Reports")
    print("13. Export Daily Report")
    print("14. Process Notification")
    print("15. List Doctors")
    print("16. List Appointments")
    print("17. List Patients")
    print("0. Exit")


def register_patient(
    hospital: HospitalService,
) -> None:
    """Get patient information and register the patient."""

    patient_id = input("Patient ID: ")
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    phone = input("Phone: ")

    hospital.register_patient(
        patient_id,
        name,
        age,
        gender,
        phone,
    )

    print("Patient registered successfully.")


def add_doctor(
    hospital: HospitalService,
) -> None:
    """Get doctor information and add the doctor."""

    doctor_id = input("Doctor ID: ")
    name = input("Doctor name: ")
    specialization = input("Specialization: ")
    department = input("Department: ")

    slots_input = input(
        "Available slots (comma separated): "
    )

    slots = [
        slot.strip()
        for slot in slots_input.split(",")
        if slot.strip()
    ]

    hospital.add_doctor(
        doctor_id,
        name,
        specialization,
        department,
        slots,
    )

    print("Doctor added successfully.")


def book_appointment(
    hospital: HospitalService,
) -> None:
    """Get appointment information and book an appointment."""

    appointment_id = input("Appointment ID: ")
    patient_id = input("Patient ID: ")
    doctor_id = input("Doctor ID: ")
    time_slot = input("Time slot: ")

    appointment = hospital.book_appointment(
        appointment_id,
        patient_id,
        doctor_id,
        time_slot,
    )

    print(
        f"Appointment {appointment.appointment_id} "
        "booked successfully."
    )


def reschedule_appointment(
    hospital: HospitalService,
) -> None:
    """Reschedule an existing appointment."""

    appointment_id = input("Appointment ID: ")
    new_slot = input("New time slot: ")

    hospital.reschedule_appointment(
        appointment_id,
        new_slot,
    )

    print("Appointment rescheduled successfully.")


def cancel_appointment(
    hospital: HospitalService,
) -> None:
    """Cancel an existing appointment."""

    appointment_id = input("Appointment ID: ")

    hospital.cancel_appointment(
        appointment_id,
    )

    print("Appointment cancelled successfully.")


def admit_emergency(
    hospital: HospitalService,
) -> None:
    """Admit an emergency patient."""

    patient_id = input("Patient ID: ")
    severity = int(
        input("Severity (1 = highest): ")
    )

    hospital.admit_emergency(
        patient_id,
        severity,
    )

    print("Emergency patient added to priority queue.")


def process_emergency(
    hospital: HospitalService,
) -> None:
    """Process the highest-priority emergency."""

    patient = hospital.process_emergency()

    if patient is None:
        print("No emergency patients waiting.")
        return

    print(
        f"Emergency processed for patient: "
        f"{patient.patient_id}"
    )


def complete_appointment(
    hospital: HospitalService,
) -> None:
    """Complete a scheduled appointment."""

    appointment_id = input("Appointment ID: ")

    hospital.complete_appointment(
        appointment_id,
    )

    print("Appointment completed successfully.")


def add_medical_history(
    hospital: HospitalService,
) -> None:
    """Add a medical visit to patient history."""

    patient_id = input("Patient ID: ")
    visit_date = input("Visit date (YYYY-MM-DD): ")
    doctor_id = input("Doctor ID: ")
    diagnosis = input("Diagnosis: ")
    notes = input("Notes: ")

    hospital.add_medical_history(
        patient_id,
        visit_date,
        doctor_id,
        diagnosis,
        notes,
    )

    print("Medical history added successfully.")


def view_medical_history(
    hospital: HospitalService,
) -> None:
    """Display a patient's medical history."""

    patient_id = input("Patient ID: ")

    if patient_id not in hospital.patients:
        print("Error: Patient not found.")
        return

    if patient_id not in hospital.medical_records:
        print("No medical history found.")
        return

    print("\n1. View full history")
    print("2. View history by date")

    choice = input(
        "Enter choice: "
    ).strip()

    record = hospital.medical_records[
        patient_id
    ]

    if choice == "1":
        history = record.get_history()

    elif choice == "2":
        date = input(
            "Enter date (YYYY-MM-DD): "
        ).strip()

        history = record.get_history_by_date(
            date
        )

    else:
        print("Invalid choice.")
        return

    if not history:
        print("No medical history found.")
        return

    print("\nMedical History")
    print("=" * 60)

    for visit in history:
        print(f"Date       : {visit.visit_date}")
        print(f"Doctor     : {visit.doctor_id}")
        print(f"Diagnosis  : {visit.diagnosis}")
        print(f"Notes      : {visit.notes}")
        print("-" * 60)

def generate_bill(hospital):
    """Collect billing details and generate a patient bill."""

    print("\n--- Generate Bill ---")

    patient_id = input("Enter patient ID: ").strip()

    consultation_charge = float(
        input("Enter consultation charge: ")
    )

    test_charges = {}
    test_count = int(
        input("Enter number of tests: ")
    )

    for _ in range(test_count):
        test_name = input("Enter test name: ").strip()
        test_amount = float(
            input(f"Enter charge for {test_name}: ")
        )
        test_charges[test_name] = test_amount

    procedure_charges = {}
    procedure_count = int(
        input("Enter number of procedures: ")
    )

    for _ in range(procedure_count):
        procedure_name = input(
            "Enter procedure name: "
        ).strip()

        procedure_amount = float(
            input(f"Enter charge for {procedure_name}: ")
        )

        procedure_charges[procedure_name] = procedure_amount

    print("\nBilling Type:")
    print("1. Standard")
    print("2. Insurance")

    billing_choice = input(
        "Enter billing type: "
    ).strip()

    if billing_choice == "1":
        billing_type = "standard"
        discount_rate = 0.0

    elif billing_choice == "2":
        billing_type = "insurance"

        discount_percent = float(
            input("Enter insurance discount percentage: ")
        )

        discount_rate = discount_percent / 100

    else:
        print("Invalid billing type.")
        return

    bill = hospital.generate_bill(
        patient_id,
        consultation_charge,
        test_charges,
        procedure_charges,
        billing_type=billing_type,
        discount_rate=discount_rate,
    )

    print("\n--- Bill Generated ---")
    print(bill.summary())

def parse_charges(
    value: str,
) -> dict[str, float]:
    """Convert name:amount input into a dictionary."""

    if not value.strip():
        return {}

    charges = {}

    for item in value.split(","):
        name, amount = item.split(":", 1)

        charges[name.strip()] = float(
            amount.strip()
        )

    return charges


def view_reports(
    hospital: HospitalService,
) -> None:
    """Display hospital reports."""

    date = input(
        "Date (YYYY-MM-DD): "
    )

    reports = hospital.get_reports(date)

    print("\nHospital Reports")
    print("-" * 50)

    print(
        "Patients seen:",
        reports["patients_seen_per_day"],
    )

    print(
        "Doctor utilization:",
        reports["doctor_utilization"],
    )

    print(
        "Revenue collected:",
        reports["revenue_collected"],
    )

    print(
        "Average emergency wait time:",
        reports["average_emergency_wait_time"],
    )


def export_daily_report(
    hospital: HospitalService,
) -> None:
    """Export the daily report to CSV."""

    date = input(
        "Date (YYYY-MM-DD): "
    )

    file_path = hospital.export_daily_report(
        date
    )

    print(
        f"Report exported to: {file_path}"
    )


def process_notification(
    hospital: HospitalService,
) -> None:
    """Process the next notification."""

    message = hospital.notifications.process_notification()

    if message is None:
        print("No notifications waiting.")
        return

    print(f"Notification: {message}")

def list_doctors(
    hospital: HospitalService,
) -> None:
    """Display all registered doctors."""

    if not hospital.doctors:
        print("\nNo doctors registered.")
        return

    print("\nRegistered Doctors")
    print("=" * 70)

    for doctor in hospital.doctors.values():
        print(f"Doctor ID      : {doctor.doctor_id}")
        print(f"Name            : {doctor.name}")
        print(f"Specialization  : {doctor.specialization}")
        print(f"Department      : {doctor.department}")

        if doctor.available_slots:
            print("Available Slots :")
            for slot in doctor.available_slots:
                print(f"  - {slot}")
        else:
            print("Available Slots : None")

        print("-" * 70)

def list_appointments(
    hospital: HospitalService,
) -> None:
    """Display all appointments."""

    if not hospital.appointments:
        print("\nNo appointments found.")
        return

    print("\nAppointments")
    print("=" * 80)

    for appointment in hospital.appointments.values():
        patient = hospital.patients.get(
            appointment.patient_id
        )

        doctor = hospital.doctors.get(
            appointment.doctor_id
        )

        patient_name = (
            patient.name
            if patient
            else "Unknown"
        )

        doctor_name = (
            doctor.name
            if doctor
            else "Unknown"
        )

        print(
            f"Appointment ID : {appointment.appointment_id}"
        )
        print(
            f"Patient        : "
            f"{appointment.patient_id} - {patient_name}"
        )
        print(
            f"Doctor         : "
            f"{appointment.doctor_id} - {doctor_name}"
        )
        print(
            f"Time           : {appointment.time_slot}"
        )
        print(
            f"Status         : {appointment.status}"
        )
        print("-" * 80)

def list_patients(
    hospital: HospitalService,
) -> None:
    """Display all registered patients."""

    if not hospital.patients:
        print("\nNo patients registered.")
        return

    print("\n" + "=" * 60)
    print("                    PATIENT LIST")
    print("=" * 60)

    for patient in hospital.patients.values():
        print(f"Patient ID    : {patient.patient_id}")
        print(f"Name          : {patient.name}")
        print(f"Age           : {patient.age}")
        print(f"Gender        : {patient.gender}")
        print(f"Phone         : {patient.phone}")
        print("-" * 60)

def main() -> None:
    """Run the interactive hospital console."""

    hospital = HospitalService()

    while True:
        display_menu()

        choice = input(
            "\nEnter your choice: "
        ).strip()

        try:
            if choice == "1":
                register_patient(hospital)

            elif choice == "2":
                add_doctor(hospital)

            elif choice == "3":
                book_appointment(hospital)

            elif choice == "4":
                reschedule_appointment(hospital)

            elif choice == "5":
                cancel_appointment(hospital)

            elif choice == "6":
                admit_emergency(hospital)

            elif choice == "7":
                process_emergency(hospital)

            elif choice == "8":
                complete_appointment(hospital)

            elif choice == "9":
                add_medical_history(hospital)

            elif choice == "10":
                view_medical_history(hospital)

            elif choice == "11":
                generate_bill(hospital)

            elif choice == "12":
                view_reports(hospital)

            elif choice == "13":
                export_daily_report(hospital)

            elif choice == "14":
                process_notification(hospital)

            elif choice == "15":
                list_doctors(hospital)

            elif choice == "16":
                list_appointments(hospital)

            elif choice == "17":
                list_patients(hospital)

            elif choice == "0":
                print(
                    "Exiting Hospital Management System."
                )
                break

            else:
                print("Invalid choice.")

        except (ValueError, HospitalError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
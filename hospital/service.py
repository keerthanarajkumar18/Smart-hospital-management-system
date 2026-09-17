"""Main hospital service."""

from hospital.appointment import AppointmentManager
from hospital.billing import StandardBilling
from hospital.billing import InsuranceBilling
from hospital.emergency import EmergencyQueue
from hospital.exceptions import InvalidBillingError
from hospital.exceptions import PatientNotFoundError
from hospital.logger import HospitalLogger
from hospital.medical_record import MedicalRecord
from hospital.models import Doctor, Patient
from hospital.notifications import NotificationManager
from hospital.persistence import JsonPersistence
from hospital.reports import ReportService
from hospital.decorators import audit_log
from datetime import datetime


class HospitalService:
    """Main service for managing hospital operations."""

    def __init__(self):
        """Create the hospital management system."""

        # Persistence
        self.persistence = JsonPersistence("data")

        # Patient registry
        self.patients = self.persistence.load_patients()

        # Doctor registry
        self.doctors = self.persistence.load_doctors()

        # Appointment registry
        self.appointments = self.persistence.load_appointments()

        # Billing records
        self.bills = {}

        # Emergency queue
        self.emergency_queue = EmergencyQueue()

        # Emergency Records
        self.emergency_records = []

        # Medical records
        self.medical_records = {}

        saved_history = (
            self.persistence.load_medical_history()
        )

        for patient_id, visits in saved_history.items():
            record = MedicalRecord()

            for visit in visits:
                record.append_visit(
                    visit.visit_date,
                    visit.doctor_id,
                    visit.diagnosis,
                    visit.notes,
                )

            self.medical_records[patient_id] = record

        # Billing strategy
        self.billing_strategy = StandardBilling()

        # Logger
        self.logger = HospitalLogger()

        # Notification queue
        self.notifications = NotificationManager()

        # Appointment manager
        self.appointment_manager = AppointmentManager(
            self.patients,
            self.doctors,
            self.appointments,
            "data",
        )

        self.report_service = ReportService(
            self.patients,
            self.doctors,
            self.appointments,
            self.bills,
            self.emergency_records,
        )

    def register_patient(
        self,
        patient_id,
        name,
        age,
        gender,
        phone,
    ):
        """Register a new patient."""

        if patient_id in self.patients:
            raise ValueError(
                "Patient already exists."
            )

        patient = Patient(
            patient_id,
            name,
            age,
            gender,
            phone,
        )

        self.patients[patient_id] = patient

        # Create medical record for patient
        self.medical_records[patient_id] = MedicalRecord()

        # Save patients
        self.persistence.save_patients(
            self.patients
        )

        self.logger.patient_registered(
            patient_id
        )

        return patient

    def add_doctor(
        self,
        doctor_id,
        name,
        specialization,
        department,
        available_slots,
    ):
        """Add a doctor to the hospital."""

        doctor = Doctor(
            doctor_id,
            name,
            specialization,
            department,
            available_slots,
        )

        self.doctors[doctor_id] = doctor

        self.persistence.save_doctors(
            self.doctors
        )

        return doctor


    @audit_log
    def book_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        time_slot,
        user="Receptionist",
    ):
        """Book a patient appointment."""

        return self.appointment_manager.book_appointment(
            appointment_id,
            patient_id,
            doctor_id,
            time_slot,
        )

    @audit_log
    def admit_emergency(
        self,
        patient_id,
        severity,
        user="Emergency Desk",
    ):
        """Add a patient to the emergency queue."""
        arrival_time = datetime.now().isoformat()

        self.emergency_records.append(
            {
                "patient_id": patient_id,
                "severity": severity,
                "arrival_time": arrival_time,
                "served_time": None,
            }
        ) 

        if patient_id not in self.patients:
            raise PatientNotFoundError(
                "Patient not found."
            )

        self.emergency_queue.push(
            self.patients[patient_id],
            severity,
        )

        self.logger.emergency_admitted(
            patient_id,
            severity,
        )

        return True

    @audit_log
    def generate_bill(
        self,
        patient_id,
        consultation_charge,
        test_charges,
        procedure_charges,
        billing_type="standard",
        discount_rate=0.0,
        user="Billing Desk",
    ):
        """Generate a bill for a patient."""

        if patient_id not in self.patients:
            raise PatientNotFoundError(
                "Patient not found."
            )

        if billing_type == "standard":
            self.billing_strategy = StandardBilling()

        elif billing_type == "insurance":
            self.billing_strategy = InsuranceBilling(
                discount_rate
            )

        else:
            raise InvalidBillingError(
                "Invalid billing type."
            )

        bill = self.billing_strategy.calculate_bill(
            consultation_charge,
            test_charges,
            procedure_charges,
        )

        self.bills[patient_id] = bill

        self.logger.billing_generated(
            patient_id,
            bill.total,
        )

        return bill

    def get_reports(
        self,
        date: str | None = None,
    ) -> dict:
        """Return hospital reports for a given date."""

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        return self.report_service.get_all_reports(date)

    def process_emergency(self):
        """Process the highest-priority emergency patient."""

        if self.emergency_queue.is_empty():
            return None

        entry = self.emergency_queue.pop()

        served_time = datetime.now().isoformat()

        for record in self.emergency_records:
            if (
                record["patient_id"] == entry.patient.patient_id
                and record["served_time"] is None
            ):
                record["served_time"] = served_time
                break

        self.logger.logger.info(
            "Emergency processed: %s | Severity: %d",
            entry.patient.patient_id,
            entry.severity,
        )

        return entry.patient

    def add_medical_history(
    self,
    patient_id,
    visit_date,
    doctor_id,
    diagnosis,
    notes,
    ):
        """Add a medical visit to a patient's history."""

        if patient_id not in self.patients:
            raise PatientNotFoundError(
                "Patient not found."
            )

        if patient_id not in self.medical_records:
            self.medical_records[patient_id] = MedicalRecord()

        self.medical_records[patient_id].append_visit(
            visit_date,
            doctor_id,
            diagnosis,
            notes,
        )

        self.persistence.save_medical_history(
            {
                patient_id: self.medical_records[patient_id].get_history()
            }
        )

        self.logger.logger.info(
            "Medical history added: Patient: %s",
            patient_id,
        )

    def get_medical_history(
    self,
    patient_id: str,
    ):
        """Return the medical history of a patient."""

        if patient_id not in self.patients:
            raise PatientNotFoundError(
                "Patient not found."
            )

        if patient_id not in self.medical_records:
            return []

        return self.medical_records[
            patient_id
        ].get_history()

    def export_daily_report(
    self,
    date: str,
    ):
        """Export daily hospital reports to CSV."""

        return self.report_service.export_daily_report(
            date
        )

    def reschedule_appointment(
    self,
    appointment_id: str,
    new_slot: str,
    ):
        """Reschedule an existing appointment."""

        return self.appointment_manager.reschedule_appointment(
            appointment_id,
            new_slot,
        )

    def cancel_appointment(
    self,
    appointment_id: str,
    ):
        """Cancel an existing appointment."""

        return self.appointment_manager.cancel_appointment(
            appointment_id,
        )

    def complete_appointment(
    self,
    appointment_id: str,
    ):
        """Mark an appointment as completed."""

        return self.appointment_manager.complete_appointment(
            appointment_id
        )

    def set_billing_strategy(
    self,
    discount_rate: float,
    ) -> None:
        """Set insurance billing with the given discount rate."""

        self.billing_strategy = InsuranceBilling(
            discount_rate
        )
"""Appointment management for the hospital system."""

from hospital.exceptions import (
    DoctorNotFoundError,
    InvalidAppointmentError,
    PatientNotFoundError,
    SlotUnavailableError,
)
from hospital.logger import HospitalLogger
from hospital.models import Appointment, Doctor, Patient
from hospital.notifications import NotificationManager
from hospital.persistence import JsonPersistence


class AppointmentManager:
    """Manage hospital appointments."""

    def __init__(
        self,
        patients,
        doctors,
        appointments,
        data_directory="data",
    ):
        """Initialize appointment management."""

        self.patients = patients
        self.doctors = doctors
        self.appointments = appointments

        self.logger = HospitalLogger()
        self.notifications = NotificationManager()
        self.persistence = JsonPersistence(data_directory)

    def book_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        time_slot,
    ):
        """Book an appointment."""

        # Check patient
        if patient_id not in self.patients:
            raise PatientNotFoundError(
                "Patient not found."
            )

        # Check doctor
        if doctor_id not in self.doctors:
            raise DoctorNotFoundError(
                "Doctor not found."
            )

        doctor = self.doctors[doctor_id]

        # Check time slot
        if time_slot not in doctor.available_slots:
            raise SlotUnavailableError(
                "Time slot is not available."
            )

        # Check duplicate appointment ID
        if appointment_id in self.appointments:
            raise InvalidAppointmentError(
                "Appointment already exists."
            )

        # Check double booking
        for appointment in self.appointments.values():
            if (
                appointment.doctor_id == doctor_id
                and appointment.time_slot == time_slot
                and appointment.status == "scheduled"
            ):
                raise SlotUnavailableError(
                    "Doctor is already booked for this slot."
                )

        # Create appointment
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            time_slot=time_slot,
        )

        self.appointments[appointment_id] = appointment

        # Remove slot from doctor's availability
        doctor.available_slots.remove(time_slot)

        # Save changes
        self.persistence.save_appointments(
            self.appointments
        )

        self.persistence.save_doctors(
            self.doctors
        )

        # Log appointment
        self.logger.appointment_booked(
            appointment_id,
            patient_id,
            doctor_id,
        )

        # Queue notifications
        self.notifications.queue_confirmation(
            appointment_id,
            patient_id,
        )

        self.notifications.queue_reminder(
            appointment_id,
            patient_id,
        )

        return appointment

    def reschedule_appointment(
        self,
        appointment_id,
        new_slot,
    ):
        """Change the time of an appointment."""

        if appointment_id not in self.appointments:
            raise InvalidAppointmentError(
                "Appointment not found."
            )

        appointment = self.appointments[appointment_id]

        if appointment.status != "scheduled":
            raise InvalidAppointmentError(
                "Only scheduled appointments can be rescheduled."
            )

        doctor = self.doctors[appointment.doctor_id]

        if new_slot not in doctor.available_slots:
            raise SlotUnavailableError(
                "New time slot is not available."
            )

        # Return old slot
        doctor.available_slots.append(
            appointment.time_slot
        )

        # Remove new slot
        doctor.available_slots.remove(new_slot)

        # Update appointment
        appointment.time_slot = new_slot

        # Save changes
        self.persistence.save_appointments(
            self.appointments
        )

        self.persistence.save_doctors(
            self.doctors
        )

        self.logger.appointment_rescheduled(
            appointment_id,
            new_slot,
        )

        return appointment

    def cancel_appointment(self, appointment_id):
        """Cancel an appointment."""

        if appointment_id not in self.appointments:
            raise InvalidAppointmentError(
                "Appointment not found."
            )

        appointment = self.appointments[appointment_id]

        if appointment.status == "cancelled":
            raise InvalidAppointmentError(
                "Appointment is already cancelled."
            )

        doctor = self.doctors[appointment.doctor_id]

        # Return slot to doctor
        if appointment.time_slot not in doctor.available_slots:
            doctor.available_slots.append(
                appointment.time_slot
            )

        # Change status
        appointment.status = "cancelled"

        # Save changes
        self.persistence.save_appointments(
            self.appointments
        )

        self.persistence.save_doctors(
            self.doctors
        )

        self.logger.appointment_cancelled(
            appointment_id
        )

        return appointment

    def complete_appointment(
    self,
    appointment_id: str,
    ):
        """Mark a scheduled appointment as completed."""

        if appointment_id not in self.appointments:
            raise InvalidAppointmentError(
                "Appointment not found."
            )

        appointment = self.appointments[appointment_id]

        if appointment.status != "scheduled":
            raise InvalidAppointmentError(
                "Only scheduled appointments can be completed."
            )

        appointment.status = "completed"

        self.persistence.save_appointments(
            self.appointments
        )

        self.logger.logger.info(
            "Appointment completed: %s",
            appointment_id,
        )

        return appointment
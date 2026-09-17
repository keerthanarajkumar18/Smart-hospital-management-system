"""Logging for the hospital management system."""

import logging
from pathlib import Path


class HospitalLogger:
    """Handle hospital application logging."""

    def __init__(self):
        """Create the hospital log file."""

        log_directory = Path("logs")
        log_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logger = logging.getLogger("hospital")
        self.logger.setLevel(logging.INFO)

        # Remove old handlers
        for handler in self.logger.handlers:
            handler.close()

        self.logger.handlers.clear()

        # Create log file
        file_handler = logging.FileHandler(
            "logs/hospital.log",
            encoding="utf-8"
        )

        # Set log format
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)

    def patient_registered(self, patient_id):
        """Log patient registration."""

        self.logger.info(
            "Patient registered: %s",
            patient_id
        )

    def appointment_booked(
        self,
        appointment_id,
        patient_id,
        doctor_id
    ):
        """Log appointment booking."""

        self.logger.info(
            "Appointment booked: %s | Patient: %s | Doctor: %s",
            appointment_id,
            patient_id,
            doctor_id
        )

    def appointment_rescheduled(
        self,
        appointment_id,
        new_slot
    ):
        """Log appointment rescheduling."""

        self.logger.info(
            "Appointment rescheduled: %s | New slot: %s",
            appointment_id,
            new_slot
        )

    def appointment_cancelled(self, appointment_id):
        """Log appointment cancellation."""

        self.logger.info(
            "Appointment cancelled: %s",
            appointment_id
        )

    def emergency_admitted(
        self,
        patient_id,
        severity
    ):
        """Log emergency admission."""

        self.logger.info(
            "Emergency admitted: %s | Severity: %d",
            patient_id,
            severity
        )

    def billing_generated(
        self,
        patient_id,
        amount
    ):
        """Log bill generation."""

        self.logger.info(
            "Billing generated: Patient: %s | Amount: ₹%.2f",
            patient_id,
            amount
        )

    def error(self, message):
        """Log an application error."""

        self.logger.error(message)
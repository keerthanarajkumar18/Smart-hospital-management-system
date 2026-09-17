
"""Report calculations for the hospital management system."""

from datetime import datetime
from typing import Any
import csv
from pathlib import Path

class ReportService:
    """Generate reports from hospital data."""

    def __init__(
        self,
        patients: dict,
        doctors: dict,
        appointments: dict,
        bills: dict,
        emergency_records: list[dict],
    ) -> None:
        """Initialize the report service."""

        self.patients = patients
        self.doctors = doctors
        self.appointments = appointments
        self.bills = bills
        self.emergency_records = emergency_records

    def patients_seen_per_day(
    self,
    date: str,
    ) -> int:
        """Return the number of completed appointments on a date."""

        # Select only completed appointments for the given date.
        selected_appointments = filter(
            lambda appointment: (
                appointment.time_slot.startswith(date)
                and appointment.status == "completed"
            ),
            self.appointments.values(),
        )

        # Convert selected appointments into patient IDs.
        patient_ids = map(
            lambda appointment: appointment.patient_id,
            selected_appointments,
        )

        # Count the patients.
        return len(list(patient_ids))

    
    def doctor_utilization(self) -> dict[str, int]:
        """Return the number of appointments handled by each doctor."""

        utilization: dict[str, int] = {}

        for doctor_id in self.doctors:

            selected_appointments = filter(
                lambda appointment: (
                    appointment.doctor_id == doctor_id
                    and appointment.status != "cancelled"
                ),
                self.appointments.values(),
            )

            appointment_ids = map(
                lambda appointment: appointment.appointment_id,
                selected_appointments,
            )

            utilization[doctor_id] = len(
                list(appointment_ids)
            )

        return utilization


    def revenue_collected(self) -> float:
        """Return the total revenue from all generated bills."""

        total = 0.0

        for bill in self.bills.values():
            total += bill.total

        return total

    def average_emergency_wait_time(self) -> float:
        """Return the average emergency waiting time in minutes."""

        completed_records = filter(
            lambda record: record["served_time"] is not None,
            self.emergency_records,
        )

        wait_times = map(
            lambda record: (
                datetime.fromisoformat(record["served_time"])
                - datetime.fromisoformat(record["arrival_time"])
            ).total_seconds() / 60,
            completed_records,
        )

        wait_times = list(wait_times)

        if not wait_times:
            return 0.0

        average_minutes = sum(wait_times) / len(wait_times)

        total_seconds = int(average_minutes * 60)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_all_reports(
        self,
        date: str,
    ) -> dict[str, Any]:
        """Return all hospital reports in structured form."""

        return {
            "patients_seen_per_day": self.patients_seen_per_day(
                date
            ),
            "doctor_utilization": self.doctor_utilization(),
            "revenue_collected": self.revenue_collected(),
            "average_emergency_wait_time": (
                self.average_emergency_wait_time()
            ),
        }

    def export_daily_report(
    self,
    date: str,
    output_directory: str | Path = "reports",
    ) -> Path:
        """Export daily hospital reports to a CSV file."""

        output_directory = Path(output_directory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = output_directory / "daily_report.csv"

        reports = self.get_all_reports(date)

        with file_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                ["Report", "Value"]
            )

            writer.writerow(
                [
                    "Patients Seen",
                    reports["patients_seen_per_day"],
                ]
            )

            writer.writerow(
                [
                    "Doctor Utilization",
                    reports["doctor_utilization"],
                ]
            )

            writer.writerow(
                [
                    "Revenue Collected",
                    reports["revenue_collected"],
                ]
            )

            writer.writerow(
                [
                    "Average Wait Time",
                    reports["average_emergency_wait_time"],
                ]
            )

        return file_path    



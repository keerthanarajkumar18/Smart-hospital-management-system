"""Notification queue for the hospital management system."""

from queue import Queue

from hospital.logger import HospitalLogger


class NotificationManager:
    """Manage appointment notifications using a queue."""

    def __init__(self):
        """Create an empty notification queue."""

        self.queue = Queue()
        self.logger = HospitalLogger()

    def queue_confirmation(self, appointment_id, patient_id):
        """Add an appointment confirmation to the queue."""

        message = (
            f"Appointment {appointment_id} "
            f"confirmed for patient {patient_id}"
        )

        self.queue.put(message)

        self.logger.logger.info(
            "Notification queued: %s",
            message
        )

    def queue_reminder(self, appointment_id, patient_id):
        """Add an appointment reminder to the queue."""

        message = (
            f"Reminder for appointment {appointment_id} "
            f"for patient {patient_id}"
        )

        self.queue.put(message)

        self.logger.logger.info(
            "Notification queued: %s",
            message
        )

    def process_notification(self):
        """Get and process the next notification."""

        if self.queue.empty():
            return None

        message = self.queue.get()

        self.logger.logger.info(
            "Notification processed: %s",
            message
        )

        return message

    def is_empty(self):
        """Check whether the notification queue is empty."""

        return self.queue.empty()
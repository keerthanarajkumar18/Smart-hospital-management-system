from hospital.notifications import NotificationManager


def test_confirmation():
    """Test appointment confirmation."""

    manager = NotificationManager()

    manager.queue_confirmation("A001", "P001")

    assert manager.is_empty() is False


def test_reminder():
    """Test appointment reminder."""

    manager = NotificationManager()

    manager.queue_reminder("A001", "P001")

    assert manager.is_empty() is False


def test_notification_order():
    """Test that notifications come out in order."""

    manager = NotificationManager()

    manager.queue_confirmation("A001", "P001")
    manager.queue_reminder("A001", "P001")

    first = manager.process_notification()
    second = manager.process_notification()

    assert first == "Appointment A001 confirmed for patient P001"
    assert second == "Reminder for appointment A001 for patient P001"


def test_empty_queue():
    """Test an empty notification queue."""

    manager = NotificationManager()

    result = manager.process_notification()

    assert result is None


def test_notification_logging(tmp_path, monkeypatch):
    """Test that notifications are written to the log."""

    monkeypatch.chdir(tmp_path)

    manager = NotificationManager()

    manager.queue_confirmation("A001", "P001")
    manager.process_notification()

    log_file = tmp_path / "logs" / "hospital.log"

    content = log_file.read_text()

    assert "Notification queued" in content
    assert "Notification processed" in content
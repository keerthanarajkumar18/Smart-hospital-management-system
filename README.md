# Smart Hospital Management System

## 1. Project Overview

The **Smart Hospital Management System** is a Python-based application developed using **Object-Oriented Programming (OOP)** principles.

The system manages important hospital operations such as:

* Patient registration
* Doctor registration and available appointment slots
* Appointment booking, rescheduling and cancellation
* Emergency patient admission and priority handling
* Medical history management
* Hospital billing - standard and insurance-based billing
* Appointment confirmation and reminder notifications
* Hospital activity logging
* Daily hospital reports
* JSON-based data persistence
* CSV-based daily report generation

The application follows a modular design where different responsibilities are handled by separate classes and modules.

### Main Features

#### Patient Management

Patients can be registered with:

* Patient ID
* Name
* Age
* Gender
* Phone number

Patient information is stored persistently in JSON files.

#### Doctor Management

Doctors are registered with:

* Doctor ID
* Name
* Specialization
* Department
* Available appointment slots

Booked appointment slots are removed from the available slot list.

#### Appointment Management

The system supports:

* Booking appointments
* Rescheduling appointments
* Cancelling appointments
* Completing appointments
* Preventing double booking
* Validating patient and doctor IDs
* Validating appointment slots

Appointment information is stored in JSON format.

#### Emergency Management

Emergency patients are handled separately using a **priority queue implemented with Python's heapq module**.

Emergency priority is determined by:

1. Severity
2. Arrival order when severity is the same

Therefore, higher-priority emergency cases are processed before lower-priority cases.

#### Medical Records

The system maintains an append-only medical history for each patient.

Each visit contains:

* Visit date
* Doctor ID
* Diagnosis
* Notes

The system supports:

* Viewing complete history
* Filtering history by doctor
* Filtering history by date
* Lazily streaming history using generators

Medical history is persisted in JSON format.

#### Billing

The billing system uses the **Strategy Design Pattern**.

Two billing strategies are available:

* StandardBilling
* InsuranceBilling

A bill contains:

* Consultation charge
* Test charges
* Procedure charges
* Discount(Insurance Based)
* Final total

For insurance billing, the discount is calculated from the subtotal:

```text
Discount = Subtotal × Discount Rate
Final Total = Subtotal − Discount
```

#### Notifications

Appointment confirmations and reminders are placed into a notification queue.

Notifications can be processed one at a time from the queue.

#### Logging

The Python logging module is used to record important system activities such as:

* Patient registration
* Appointment booking, rescheduling and cancellation
* Emergency admission
* Billing
* Notification processing
* Audit information

#### Reports

The system generates reports for:

* Patients seen per day
* Doctor utilization
* Revenue collected
* Average emergency waiting time

Daily reports can also be exported to CSV.

---

# 2. Folder Structure

```text
smart-hospital-management/
│
├── hospital/
│   ├── __init__.py
│   ├── models.py
│   ├── exceptions.py
│   ├── emergency.py
│   ├── medical_record.py
│   ├── billing.py
│   ├── persistence.py
│   ├── logger.py
│   ├── decorators.py
│   ├── notifications.py
│   ├── appointment.py
│   ├── reports.py
│   └── service.py
│
├── data/
│   ├── patients.json
│   ├── doctors.json
│   ├── appointments.json
│   └── medical_history.json
│
├── reports/
│   └── daily_report.csv
│
├── logs/
│   └── hospital.log
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_exceptions.py
│   ├── test_emergency.py
│   ├── test_medical_record.py
│   ├── test_billing.py
│   ├── test_persistence.py
│   ├── test_logger.py
│   ├── test_decorators.py
│   ├── test_notifications.py
│   ├── test_appointment.py
│   ├── test_service.py
│   ├── test_reports.py
│   ├── test_restart_persistence.py
│   └── test_end_to_end.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Folder Explanation

| Folder/File         | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `hospital/`         | Contains the application's core Python modules             |
| `models.py`         | Defines `Patient`, `Doctor`, and `Appointment` data models |
| `exceptions.py`     | Defines the custom exception hierarchy                     |
| `emergency.py`      | Implements the emergency priority queue                    |
| `medical_record.py` | Manages patient medical history and safe record writing    |
| `billing.py`        | Implements billing strategies and bill calculation         |
| `persistence.py`    | Handles JSON data storage and loading                      |
| `logger.py`         | Provides application logging                               |
| `decorators.py`     | Contains the `@audit_log` decorator                        |
| `notifications.py`  | Manages appointment notifications                          |
| `appointment.py`    | Handles appointment operations                             |
| `reports.py`        | Generates hospital reports and CSV output                  |
| `service.py`        | Provides the main `HospitalService`                        |
| `data/`             | Stores persistent JSON data                                |
| `reports/`          | Stores generated CSV reports                               |
| `logs/`             | Stores application log files                               |
| `tests/`            | Contains automated pytest tests                            |
| `main.py`           | Provides the interactive console application               |
| `requirements.txt`  | Contains pinned Python dependencies                        |
| `.gitignore`        | Prevents generated/unwanted files from being committed     |

---

# 3. Python Version and Dependencies

## Python Version

The project is developed using:

```text
Python 3.13
```

Check the installed version with:

```powershell
python --version
```

Example:

```text
Python 3.13.x
```

## Dependencies

The project uses the following external dependency:

```text
pytest
```

Python standard-library modules are also used, including:

* `dataclasses`
* `heapq`
* `itertools`
* `json`
* `logging`
* `queue`
* `csv`
* `pathlib`
* `datetime`
* `tempfile`
* `os`
* `functools`
* `inspect`

The standard-library modules do not need to be installed separately.

The exact installed dependency versions are pinned in:

```text
requirements.txt
```

---

# 4. Setup

## Step 1: Clone or open the project

Open the project directory:

```powershell
cd smart-hospital-management
```

## Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

## Step 3: Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should show something similar to:

```text
(.venv) PS C:\...\smart-hospital-management>
```

## Step 4: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

## Step 5: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install pytest and generate it with:

```powershell
python -m pip install pytest
python -m pip freeze > requirements.txt
```

---

# 5. Running the Application

Start the interactive console application using:

```powershell
python main.py
```

The application displays a menu similar to:

```text
==================================================
       SMART HOSPITAL MANAGEMENT SYSTEM
==================================================

1. Register Patient
2. Add Doctor
3. Book Appointment
4. Reschedule Appointment
5. Cancel Appointment
6. Admit Emergency
7. Process Emergency
8. Complete Appointment
9. Add Medical History
10. View Medical History
11. Generate Bill
12. View Reports
13. Export Daily Report
14. Process Notification
15. List Patients
16. List Doctors
17. List Appointments
0. Exit

Enter your choice:
```
---

# 6. Data Persistence

The application automatically stores important data in the `data/` directory.

### Patient Data

```text
data/patients.json
```

### Doctor Data

```text
data/doctors.json
```

### Appointment Data

```text
data/appointments.json
```

### Medical History

```text
data/medical_history.json
```

Because these files are persisted, patient, doctor, appointment, and medical-history information can be loaded again when the application is restarted.

For example:

```text
Run application
      ↓
Register patient
      ↓
Data saved to patients.json
      ↓
Exit application
      ↓
Start application again
      ↓
Patient data loaded from JSON
```

---

# 7. Billing

Select:

```text
11. Generate Bill
```

The application asks for:

* Patient ID
* Consultation charge
* Number of tests
* Test names and charges
* Number of procedures
* Procedure names and charges
* Billing type

Billing types:

```text
1. Standard
2. Insurance
```

### Standard Billing

Standard billing applies the complete subtotal without a discount.

Example:

```text
Consultation: ₹500
Tests:        ₹1000
Procedures:   ₹500
Discount:     ₹0
Total:        ₹2000
```

### Insurance Billing

Insurance billing applies the selected discount percentage.

For example, with a 10% discount:

```text
Subtotal:     ₹2000
Discount:      ₹200
Final Total:  ₹1800
```

The actual calculation is performed by `InsuranceBilling`.

---

# 8. Emergency Processing

Emergency patients are inserted into a priority queue.

The queue uses:

```python
heapq
```

Priority is based on severity and arrival order.

Example:

```text
Patient     Severity
P001        3
P002        1
P003        2
P004        1
```

Processing order:

```text
P002
P004
P003
P001
```

For patients with the same severity, the patient who arrived earlier is processed first.

This keeps emergency processing separate from normal scheduled appointments.

---

# 9. Medical History

Select:

```text
10. View Medical History
```

The application can display the patient's complete history or filter visits by date.

Example:

```text
Patient: P001

Visit Date: 2026-09-15
Doctor: D001
Diagnosis: Fever
Notes: Temperature monitored.

Visit Date: 2026-09-16
Doctor: D002
Diagnosis: Infection
Notes: Medication prescribed.
```

When filtering by date:

```text
Enter date: 2026-09-16
```

only visits from that date are displayed.

---

# 10. Notifications

When an appointment is booked, the system can queue a confirmation notification.

For example:

```text
Appointment A001 confirmed for patient P001
```

Reminder notifications can also be queued.

Select:

```text
14. Process Notification
```

to process the next notification.

If the queue is empty:

```text
No notifications waiting.
```

---

# 11. Logging

Application events are recorded in:

```text
logs/hospital.log
```

Example log entries include:

```text
Patient registered: P001
Appointment booked: A001 | Patient: P001 | Doctor: D001
Emergency admitted: P002 | Severity: 1
Billing generated: Patient: P001 | Amount: ₹1800.00
```

The `@audit_log` decorator additionally records:

* Time
* User
* Operation

Example:

```text
AUDIT | Time: ... | User: Receptionist | Operation: book_appointment
```

---

# 12. Reports

Select:

```text
12. View Reports
```

The system reports:

### Patients Seen Per Day

Counts completed appointments for a specified date.

### Doctor Utilization

Shows the number of appointments handled by each doctor.

Example:

```text
D001: 5
D002: 3
```

### Revenue Collected

Calculates the total value of generated bills.

Example:

```text
Revenue collected: ₹8500.00
```

### Average Emergency Wait Time

Calculates the average waiting time of processed emergency patients.

The displayed value is represented in:

```text
HH:MM:SS
```

Example:

```text
Average emergency wait time: 00:00:02
```

---

# 13. CSV Report

Select:

```text
13. Export Daily Report
```

The report is generated in:

```text
reports/daily_report.csv
```

The CSV contains values such as:

```text
Report,Value
Patients Seen,2
Doctor Utilization,"{'D001': 2, 'D002': 1}"
Revenue Collected,3500.0
Average Wait Time,00:00:02
```

---

# 14. Error Handling

The system uses a custom exception hierarchy to prevent invalid operations from crashing the application.

Examples include:

```text
HospitalError
├── PatientNotFoundError
├── DoctorNotFoundError
├── SlotUnavailableError
├── InvalidAppointmentError
└── InvalidBillingError
```

Examples of handled errors:

* Registering a duplicate patient
* Booking an appointment for a missing patient
* Booking an unavailable slot
* Double-booking a slot
* Cancelling an invalid appointment

The console catches these exceptions and displays an appropriate error message.

---

# 15. Testing

The project uses **pytest** for automated testing.

Run all tests:

```powershell
pytest -v
```

Example:

```text
================ test session starts ================

tests/test_models.py ........
tests/test_emergency.py ......
tests/test_billing.py .........
tests/test_persistence.py .......
...

================= XX passed =================
```

A successful test run indicates that the implemented functionality is behaving according to the defined test cases.

Tests cover:

* Domain models
* Custom exceptions
* Emergency priority queue
* Medical records
* Billing strategies
* JSON persistence
* Logging
* Notifications
* Appointment management
* Hospital service
* Reports
* End-to-end hospital workflow

---

# 16. Interpreting Results

The console output can be used to verify individual hospital operations.

### Successful Patient Registration

```text
Patient registered successfully.
```

means the patient was added to the registry and persisted.

### Successful Appointment Booking

```text
Appointment booked successfully.
```

means the requested slot was available and the appointment was created.

### Emergency Processing

Emergency patients should be processed according to severity and arrival order.

### Billing Result

The final bill shows:

```text
Consultation
Tests
Procedures
Discount
Total
```

The `Total` represents the final amount after any applicable insurance discount.

### Reports

Reports provide a summary of hospital activity, including:

* Number of patients seen
* Doctor utilization
* Revenue
* Average emergency waiting time

### Test Results

A passing pytest result confirms that the corresponding automated test cases completed successfully.

---

# 17. Conclusion

The Smart Hospital Management System demonstrates how Python OOP and standard-library features can be combined to build a modular hospital application.

The project provides functionality for patient and doctor management, appointment scheduling, emergency prioritization, medical records, billing, notifications, logging, persistence, reporting, and automated testing.

The modular architecture also makes individual components easier to test, maintain, and extend.

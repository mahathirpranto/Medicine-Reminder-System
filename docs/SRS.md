# Software Requirements Specification (SRS)
## Medicine Reminder System

**Version:** 1.0  
**Purpose:** University web development coursework

## 1. Introduction
### 1.1 Purpose
This document defines the functional and non-functional requirements for Medicine Reminder System Version 1.0.

### 1.2 Scope
A browser-based application using HTML, CSS/Bootstrap, JavaScript, PHP, and MySQL, developed locally with XAMPP.

## 2. Overall Description
### 2.1 User Classes
- **Guest:** Can register or log in.
- **Registered user:** Manages personal medicines, reminders, and history.
- **Administrator:** Not required for Version 1.

### 2.2 Operating Environment
- Windows or another operating system supporting XAMPP or a compatible PHP/MySQL stack.
- A modern web browser.
- PHP server and MySQL database.

## 3. Interface Requirements
- Navigation: Dashboard, My Medicines, Reminders, History, and Profile.
- Forms display required fields and validation messages.
- Statuses distinguish upcoming, due, taken, skipped, and overdue.
- Responsive design for phone, tablet, and desktop.

## 4. Functional Requirements
- **SRS-F-01 — Registration:** Validate fields and unique email; store a password hash.
- **SRS-F-02 — Authentication:** Verify credentials and protect private pages using server-side sessions.
- **SRS-F-03 — Medicine CRUD:** Allow users to manage only medicine records they own.
- **SRS-F-04 — Reminders:** Allow reminder time, frequency, start date, and optional end date to be saved.
- **SRS-F-05 — Reminder display:** Show upcoming and due occurrences using the configured local time.
- **SRS-F-06 — Dose status:** Save taken/skipped status and recorded timestamp.
- **SRS-F-07 — History:** Show dose logs filtered by date and medicine.
- **SRS-F-08 — Validation:** Validate values, dates, and record ownership on the server.
- **SRS-F-09 — Logout:** End the authenticated session.

## 5. Data Requirements
Use primary and foreign keys. Store passwords as hashes. Initial tables:

| Table | Important fields | Purpose |
|---|---|---|
| `users` | `user_id` PK, `name`, `email`, `password_hash` | Account |
| `medicines` | `medicine_id` PK, `user_id` FK, `medicine_name`, `dosage_instructions`, `start_date`, `end_date` | Medicine list |
| `reminders` | `reminder_id` PK, `medicine_id` FK, `reminder_time`, `frequency` | Schedule rules |
| `dose_logs` | `log_id` PK, `reminder_id` FK, `scheduled_at`, `status`, `recorded_at` | Dose history |

## 6. Non-Functional Requirements
- **Security:** Prepared SQL statements, password hashing, sessions, ownership checks, and output escaping.
- **Performance:** Typical pages should load promptly for coursework-sized data.
- **Usability:** Readable text, clear messages, and keyboard-accessible controls.
- **Integrity:** Prevent invalid foreign keys and invalid date ranges.

## 7. Acceptance Tests

| Test | Action | Expected result |
|---|---|---|
| AT-01 | Register with valid details | Account created; password stored as hash. |
| AT-02 | Use wrong password | Access denied. |
| AT-03 | Add a medicine | Record appears in the user's list. |
| AT-04 | Try another user's record ID | Access denied. |
| AT-05 | Mark dose taken | Status and timestamp saved. |
| AT-06 | Open history | Past dose records appear. |

## 8. System Architecture Diagram
![Medicine Reminder System architecture diagram](system_architecture.png)

**Figure 1.** High-level architecture.

## 9. Constraints
- Reminder accuracy depends on implementation, device clock, browser permissions, and app availability.
- The system does not verify prescriptions or provide medical advice.
- Do not rely on the student project as the only reminder for critical medication.

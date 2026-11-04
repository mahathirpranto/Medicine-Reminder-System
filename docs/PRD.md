# Product Requirements Document (PRD)
## Medicine Reminder System

**Version:** 1.0  
**Purpose:** University web development coursework

## 1. Purpose
The Medicine Reminder System is a web application that helps users organize medication schedules they have received from a qualified healthcare professional. Users can manage medicine details, view scheduled reminders, record dose actions, and review history. The application does not diagnose conditions or prescribe medicines.

## 2. Problem Statement
People may forget scheduled doses or find it difficult to track several medicines. A clear schedule and dose-history dashboard can help them organize an existing routine.

## 3. Product Goals
- Securely store each user's medicine records.
- Set reminder times and frequencies for medicines.
- Show due and upcoming scheduled doses.
- Record a dose as taken or skipped.
- Display medication history and simple summaries.
- Support desktop and mobile screens.

## 4. Target Users
People who want help organizing a prescribed medication schedule. Version 1 supports individual accounts; caregiver sharing may be considered in a future release.

## 5. Scope
### Included in Version 1
- Registration, login, and logout.
- Add, view, edit, and delete medicine records.
- Set reminder time, frequency, start date, and optional end date.
- Dashboard for today's and upcoming reminders.
- Taken/skipped logging with timestamps.
- Medication history and basic completion summary.

### Not Included in Version 1
- Medical advice, diagnosis, or dosage recommendations.
- Automatic changes to a prescribed schedule.
- Emergency monitoring or guaranteed notifications.
- Online pharmacy or payment functions.

## 6. Functional Requirements
- **FR-01 — Account access:** Users can register, log in, and log out.
- **FR-02 — Medicine management:** Users can create, view, update, and delete their own records.
- **FR-03 — Reminder scheduling:** Users can set reminder times, frequency, and date range.
- **FR-04 — Dashboard:** The dashboard displays due, upcoming, taken, and skipped records.
- **FR-05 — Dose logging:** Users can record a dose as taken or skipped with a timestamp.
- **FR-06 — History:** Users can review their own past dose logs.
- **FR-07 — Privacy:** Users cannot access another user's records.

## 7. Non-Functional Requirements
- Hash passwords and validate access on the server.
- Protect private records and avoid exposing sensitive details.
- Use clear labels and responsive layouts.
- Validate input and handle errors safely.
- Keep code organized for future maintenance.

## 8. Success Criteria
- A user can register and log in.
- Medicine records can be added, edited, and deleted.
- Reminders appear according to the saved schedule.
- Dose actions are visible in history.
- Users cannot access records owned by other users.

## 9. Use Case Diagram
![Medicine Reminder System use-case diagram](use_case_diagram.png)

**Figure 1.** Main user interactions.

## 10. Assumptions and Risks
Users enter schedule information based on professional instructions. Browser alerts may require permission and an open browser; this project should not promise guaranteed alarms. Users should not rely on the app as the only reminder for critical medication.

# Technical Design Document (TDD)
## Medicine Reminder System

**Version:** 1.0  
**Purpose:** University web development coursework

## 1. Overview
Proposed stack: HTML, CSS/Bootstrap, JavaScript, PHP, MySQL, and XAMPP. The design separates the interface, server logic, and database.

## 2. System Architecture
![Medicine Reminder System architecture diagram](system_architecture.png)

**Figure 1.** Browser requests are handled by PHP, which validates permissions and accesses MySQL.

## 3. Suggested Repository Structure
```text
medicine-reminder-system/
├── docs/  # PRD, SRS, TDD, diagrams
├── public/
│   ├── css/style.css
│   ├── js/app.js
│   └── images/
├── includes/  # db.php, auth.php, header.php, footer.php
├── auth/      # register.php, login.php, logout.php
├── medicines/ # index.php, create.php, edit.php, delete.php
├── reminders/ # index.php, update_status.php
├── history/   # index.php
├── dashboard.php
└── database/schema.sql
```

## 4. Module Design
### Authentication
Register with PHP `password_hash()`; verify with `password_verify()`; protect private pages with session checks.

### Database
Use PDO or MySQLi prepared statements. Keep credentials in a local configuration file excluded from Git.

### Medicine Management
Provide create/read/update/delete operations and include the authenticated user's ownership condition in each query.

### Reminder Scheduler
Generate scheduled occurrences for active medicines using the configured local timezone.

### Dose Tracking
Store the scheduled occurrence, taken/skipped status, and action timestamp.

### Dashboard
Summarize active medicines, due reminders, upcoming reminders, and recent dose logs.

### History
Filter dose logs by date and medicine.

## 5. Entity Relationship Diagram
![Medicine Reminder System ER diagram](er_diagram.png)

**Figure 2.** One user can have many medicines; a medicine can have many reminders; a reminder can have many dose logs.

## 6. Database Design Notes
- `users.user_id` is the primary key; email should be unique.
- `medicines.user_id` references `users.user_id`.
- `reminders.medicine_id` references `medicines.medicine_id`.
- `dose_logs.reminder_id` references `reminders.reminder_id`.
- Use controlled values such as `taken` and `skipped` for dose status.
- Store times consistently and display them in the configured timezone.

## 7. Security Design
- Hash passwords with PHP `password_hash()` and verify with `password_verify()`.
- Use prepared statements for all SQL that includes user input.
- Regenerate session IDs after login.
- Check login and record ownership on every private request.
- Escape output and add CSRF protection to state-changing forms.
- Do not commit database passwords or API keys to GitHub.

## 8. Reminder Workflow
1. Load reminder rules for the logged-in user and active medicines.
2. Generate occurrences for the selected day and frequency.
3. Label each occurrence upcoming or due based on local time.
4. Let the user record taken or skipped.
5. Save the scheduled occurrence and action timestamp.
6. Explain that browser alerts may not work if the browser is closed.

## 9. Error Handling
- Show friendly validation messages.
- Log technical errors privately; do not expose stack traces.
- Redirect unauthenticated users to login.
- Prevent duplicate logs for the same scheduled occurrence.

## 10. Local Setup
1. Install XAMPP and start Apache and MySQL.
2. Create a MySQL database and import `database/schema.sql` when implemented.
3. Place the project under `htdocs`.
4. Configure the database connection locally.
5. Test authentication, ownership checks, reminders, and history before submitting.

## 11. Future Improvements
- Browser/push notifications with permission and limitations documented.
- Email reminders through a trusted service.
- Caregiver sharing with consent.
- Exportable reports and accessibility improvements.

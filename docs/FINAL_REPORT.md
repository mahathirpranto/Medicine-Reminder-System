Independent University, Bangladesh  
CSE309 Web Application & Internet  

# Final Project Submission Report

**Submitted by:**  
Name: Mahathir Islam Pranto  
Student ID: 2130537  
Section: 06  
Team Number: Individual Assessment  

**Project Title:** Medicine Reminder System  
**Vercel URL:** [https://2130537-s6.vercel.app](https://2130537-s6.vercel.app)  
**GitHub Repository:** [https://github.com/mahathirpranto/Medicine-Reminder-System](https://github.com/mahathirpranto/Medicine-Reminder-System)  

**Submitted To:**  
Sayef Reyadh  
Adjunct Lecturer  
Department of Computer Science & Engineering  
Independent University, Bangladesh  

**Semester:** Autumn 2026  
**Date of Submission:** 27-11-2026  

---

## Table of Contents
- [1. Executive Summary](#1-executive-summary)
  - [1.1 Project Overview](#11-project-overview)
  - [1.2 What Was Built Since the Mid Assessment](#12-what-was-built-since-the-mid-assessment)
  - [1.3 Live Links](#13-live-links)
- [Part A. Product Requirements (PRD)](#part-a-product-requirements-prd)
  - [A1. Problem Statement](#a1-problem-statement)
  - [A2. Users and Roles](#a2-users-and-roles)
  - [A3. Goals and Success Measures](#a3-goals-and-success-measures)
  - [A4. Scope and Non-Goals](#a4-scope-and-non-goals)
  - [A5. User Stories](#a5-user-stories)
- [Part B. Software Requirements (SRS)](#part-b-software-requirements-srs)
  - [B1. Introduction](#b1-introduction)
  - [B2. Functional Requirements](#b2-functional-requirements)
  - [B3. Non-Functional Requirements](#b3-non-functional-requirements)
  - [B4. Roles and Permission Matrix](#b4-roles-and-permission-matrix)
  - [B5. Use Cases](#b5-use-cases)
  - [B6. Acceptance Criteria](#b6-acceptance-criteria)
  - [B7. Traceability Matrix](#b7-traceability-matrix)
- [Part C. Technical Design (TDD)](#part-c-technical-design-tdd)
  - [C1. Technology Stack](#c1-technology-stack)
  - [C2. System Architecture](#c2-system-architecture)
  - [C3. Backend and Frontend Structure](#c3-backend-and-frontend-structure)
  - [C4. Data Model](#c4-data-model)
  - [C5. API Design](#c5-api-design)
  - [C6. JWT Authentication Design](#c6-jwt-authentication-design)
  - [C7. RBAC Design](#c7-rbac-design)
  - [C8. Admin Dashboard Design](#c8-admin-dashboard-design)
  - [C9. Security Design and Threats](#c9-security-design-and-threats)
  - [C10. Deployment on Vercel](#c10-deployment-on-vercel)
  - [C11. Testing](#c11-testing)
- [Part D. Evidence: Screenshots of the Running Application](#part-d-evidence-screenshots-of-the-running-application)
  - [D1. User Side](#d1-user-side)
  - [D2. Security Behaviour](#d2-security-behaviour)
  - [D3. Admin Dashboard](#d3-admin-dashboard)
  - [D4. Deployment](#d4-deployment)
  - [D5. Tests](#d5-tests)
- [Part E. Project Management and Conclusion](#part-e-project-management-and-conclusion)
  - [E1. How to Run and Test](#e1-how-to-run-and-test)
  - [E2. GitHub Work](#e2-github-work)
  - [E3. Limitations](#e3-limitations)
  - [E4. Future Work](#e4-future-work)
  - [E5. Sources, Libraries and Tools](#e5-sources-libraries-and-tools)
- [Appendix. Test Accounts and Video Demo](#appendix-test-accounts-and-video-demo)

---

## 1. Executive Summary

### 1.1 Project Overview
The **Medicine Reminder System** is a secure, cloud-hosted, full-stack healthcare web application engineered to solve medication non-adherence by providing patients with scheduled reminders, daily dose adherence logging (taken vs. skipped), and comprehensive intake history tracking. Designed with rigorous privacy standards, the system isolates each patient's medical records while providing administrators with a central monitoring dashboard to oversee platform health, user activity, and dosage compliance metrics.  
**Tech Stack:** React 19 with TypeScript and Tailwind CSS (Frontend), FastAPI and SQLAlchemy (Backend REST API), Supabase PostgreSQL 17 (Cloud Database), deployed seamlessly on Vercel.

### 1.2 What Was Built Since the Mid Assessment
Since the mid assessment (which featured only basic unauthenticated CRUD operations), the application was transformed into an enterprise-grade, secure, multi-tenant system:
- **JWT Authentication with Refresh and Logout:** Implemented dual-token authentication utilizing short-lived 15-minute stateless JWT access tokens alongside 7-day cryptographically secure refresh tokens stored hashed in a dedicated `user_sessions` database table, featuring instant server-side revocation on logout and automatic silent token renewal.
- **Hierarchical Role-Based Access Control (RBAC):** Established discrete permission tiers (`patient`, secondary `admin`, and `super_admin`) with strict query-level user isolation ensuring patients can neither view nor tamper with other users' prescriptions, protected by reusable FastAPI dependency checkers.
- **Comprehensive Admin Dashboard:** Developed an administrative oversight portal featuring real-time aggregated system statistics (active users, total medicines, doses logged today), searchable and filterable user tables, role elevation/demotion, and user deletion safeguards.
- **Hierarchical Admin Protection:** Enforced code-level immutability safeguarding the Main System Administrator (`admin@example.com`) against demotion, role alteration, or deletion by secondary administrators (e.g., `vatista@example.com`).
- **Cloud Infrastructure & Serverless Deployment:** Migrated from local storage to Supabase PostgreSQL 17 via transaction connection pooling with SQLAlchemy `NullPool` architecture, fully orchestrated and live on Vercel monorepo infrastructure.

### 1.3 Live Links

*Table 1: Project URLs and Live Artifacts*

| Resource | URL | Description |
|---|---|---|
| **Production Application (Vercel)** | [https://2130537-s6.vercel.app](https://2130537-s6.vercel.app) | Live deployed user and administrator web application |
| **GitHub Repository** | [https://github.com/mahathirpranto/Medicine-Reminder-System](https://github.com/mahathirpranto/Medicine-Reminder-System) | Version-controlled source code repository with commits & PRs |
| **Interactive API Documentation** | [https://2130537-s6.vercel.app/api/docs](https://2130537-s6.vercel.app/api/docs) | Live interactive Swagger UI for all REST API endpoints |
| **OpenAPI Specification Schema** | [https://2130537-s6.vercel.app/api/openapi.json](https://2130537-s6.vercel.app/api/openapi.json) | Machine-readable JSON contract of the backend service |
| **Video Demonstration** | [https://youtu.be/placeholder-demo-video](https://youtu.be/placeholder-demo-video) | 5–8 minute end-to-end demonstration on the live Vercel URL |

*(Note: Test credentials are omitted from this file per security guidelines and are detailed exclusively in the PDF submission Appendix).*

---

## Part A. Product Requirements (PRD)

### A1. Problem Statement
Prescription non-adherence is a major global public health challenge. According to healthcare research, over 50% of patients diagnosed with chronic medical conditions fail to take their prescribed medications as directed by their physicians. Forgetting scheduled doses, confusing complex multi-medication frequencies, and losing track of whether a pill was already consumed often lead to preventable treatment failures, emergency room readmissions, and severe complications.

Today, patients cope through fragile physical pillboxes, handwritten notepad logs, or generic smartphone alarms that fail to distinguish between different prescriptions, provide no permanent audit trail of adherence, and lack dosage verification. Healthcare providers and family caregivers remain blind to whether medications were taken correctly. A centralized, accessible, secure digital reminder and dose logging web application eliminates this confusion by providing timely schedule prompts, simple one-click adherence tracking, and historical logs while preserving strict patient privacy.

### A2. Users and Roles

*Table 2: Users and Roles*

| Role | Who They Are | Main Tasks | What They Must Never Be Able To Do |
|---|---|---|---|
| **Visitor** | Unauthenticated guest accessing the web application | Browse the landing page, view authentication options, register a new patient account, or log in. | Access protected medicine schedules, read personal dose logs, or invoke any `/api/medicines` or `/api/admin` endpoints. |
| **Patient (User)** | Registered user managing personal medication regimen | Create, view, update, and delete personal prescriptions; view today's schedule; record doses as taken/skipped; inspect dose history. | View or edit other patients' medications, view platform analytics, inspect other accounts, or access any `/api/admin` routes. |
| **Secondary Admin (e.g. Vatista)** | Platform operator or medical assistant granted administrative privileges | View system-wide health statistics; inspect registered users list; monitor system dose compliance counts; manage patient statuses. | Demote, alter the role of, or delete the Main System Administrator; promote themselves to super_admin; read private dose notes of other users. |
| **Main System Administrator** | Primary system administrator (`super_admin` / `admin@example.com`) | Complete system oversight; manage all user accounts; elevate or demote secondary admins; purge obsolete accounts; inspect platform health. | Be demoted or deleted by any user or secondary admin through any portal route or API call. |

### A3. Goals and Success Measures

*Table 3: Goals and Success Measures*

| Goal ID | Strategic Goal | Measurable / Testable Success Measure | Verification Method |
|---|---|---|---|
| **G-01** | Eliminate cross-tenant data leakage | **Zero cross-user data exposure:** 100% of queries filter by authenticated `user_id`. Direct ID lookup for another user's medicine returns `404 Not Found`. | Automated security test in `test_auth.py` verifying User B cannot read User A's medicine. |
| **G-02** | Short-lived, revocable authentication | **15-minute token expiry & instant revocation:** Access tokens expire in 15 minutes; revoking a refresh token via `/api/auth/logout` rejects subsequent refresh requests immediately with `401 Unauthorized`. | Automated test verifying expired/revoked token rejection in `test_auth.py`. |
| **G-03** | Rapid schedule retrieval | **Sub-500ms response time:** Today's medication schedule (`GET /api/medicines/schedule/today`) loads in under 500ms on the deployed Vercel cloud environment. | Network panel inspection and cloud latency benchmark. |
| **G-04** | Seamless dose logging | **One-click dose confirmation:** Patients can record a dose as taken or skipped with an automatic UTC timestamp in under 2 clicks from the dashboard. | Manual verification on live dashboard UI. |
| **G-05** | Administrative immutability | **100% Main Admin self-protection:** Secondary admins attempting to change the Main Admin's role or delete the account receive HTTP `403 Forbidden`. | Automated RBAC test in `test_rbac.py` asserting 403 on attempted demotion. |
| **G-06** | Reliable cloud persistence | **Zero data loss on cold restarts:** All user accounts, sessions, medicines, and logs persist reliably across Vercel serverless cold starts. | Verified using Supabase PostgreSQL 17 cloud connection pooler. |

### A4. Scope and Non-Goals

#### In Scope
- User registration, secure login, password hashing using `bcrypt` (12 rounds).
- Dual-token JWT architecture (stateless 15-minute access token, stateful 7-day refresh token in `user_sessions`).
- Complete CRUD operations for medication records (name, dosage, frequency, reminder times, start/end dates, status).
- Today's intelligent dose scheduler computing active daily medications and adherence status.
- One-click dose logging (`taken`, `skipped`, `missed`) with UTC timestamps and optional clinical notes.
- Historical dose log timeline with filtering.
- Hierarchical Role-Based Access Control (`patient`, `admin`, `super_admin`) with admin self-protection.
- Dedicated Admin Portal displaying real-time platform statistics, user directories, role assignment, and user deletion.
- Production deployment on Vercel with PostgreSQL database integration via Supabase.

#### Out of Scope (Non-Goals)
- **Medical Prescribing or Diagnosis:** The system organizes schedules already given by physicians; it does not prescribe doses or diagnose ailments.
- **Hardware Dispenser Integration:** No physical IoT pillbox integration in Version 1.0.
- **SMS / Cellular Telephony Gateways:** SMS reminders require third-party paid carriers (Twilio); notifications are web-based.
- **E-Commerce / Pharmacy Ordering:** Direct purchasing or refills through online pharmacies is excluded.

#### Assumptions and Constraints
- **Device Clock & Timezone:** Dose calculations rely on standard ISO timestamps and browser local time for display.
- **Hosting Environment:** Vercel serverless functions have a 10-second execution timeout; database connections must use connection pooling (`NullPool`) to avoid exhausting connection limits.
- **Modern Browsers:** Target browsers are modern evergreen engines (Chrome, Firefox, Edge, Safari).

### A5. User Stories

*Table 4: User Stories*

| Story ID | Role | Action | Intended Benefit |
|---|---|---|---|
| **US-01** | Visitor | Register with email, full name, and strong password | Create a personal account to track my medications securely. |
| **US-02** | Visitor | Log in with valid credentials | Receive access and refresh tokens to access my private dashboard. |
| **US-03** | Patient | Add a new medicine with dosage, frequency, and times | Keep an accurate record of my daily prescription routine. |
| **US-04** | Patient | View today's schedule on my dashboard | Instantly identify which medications are due right now. |
| **US-05** | Patient | Click "Take" or "Skip" on a scheduled dose | Log my medication compliance in real time with an automatic timestamp. |
| **US-06** | Patient | Open my Dose History modal | Review past adherence history to discuss with my doctor during visits. |
| **US-07** | Patient | Log out from any device | Revoke my refresh token so unauthorized individuals cannot access my health data. |
| **US-08** | Patient | Attempt to fetch another patient's medicine by ID | Ensure my medical data is strictly private and cannot be spied on by others. |
| **US-09** | Admin | View platform statistics on the admin dashboard | Monitor platform engagement, total active medicines, and today's compliance. |
| **US-10** | Admin | Inspect the complete registered user directory | Audit registered patient accounts and view medicine volume per user. |
| **US-11** | Secondary Admin | Attempt to demote or alter the Main Administrator | Be blocked with HTTP 403 to prevent administrative takeover or privilege escalation. |
| **US-12** | Main Admin | Delete an abusive or inactive user account | Permanently purge unnecessary accounts and associated records to maintain clean data. |

---

## Part B. Software Requirements (SRS)

### B1. Introduction
This Software Requirements Specification (SRS) formally defines the functional and non-functional requirements for the **Medicine Reminder System (Version 2.0)**.  
**Intended Readers:** Course Instructors, Academic Examiners, Peer Developers, and System Architects.  

*Definitions:*
- **JWT (JSON Web Token):** An open standard (RFC 7519) compact URL-safe token format used to transmit claims securely between parties.
- **Access Token:** A short-lived, digitally signed JWT containing authorization claims passed via the `Authorization: Bearer <token>` header.
- **Refresh Token:** A cryptographically random opaque string used to obtain fresh access tokens without requiring repeated user credential prompts.
- **RBAC (Role-Based Access Control):** An access management paradigm restricting system access based on assigned user roles.
- **User Session:** A database record tracking active refresh tokens, associated device/client identity, expiration time, and revocation status.
- **Audit Logging:** Systematically recording user actions, role changes, and security events for compliance and anomaly detection.

*Standards & References:*
- RFC 7519: JSON Web Token (JWT)
- OWASP Application Security Verification Standard (ASVS) v4.0
- RFC 6749: The OAuth 2.0 Authorization Framework
- FastAPI Technical Reference & Starlette Documentation

### B2. Functional Requirements

#### B2.1 Authentication & Session Management (FR-AUTH)

*Table 5: Functional Requirements — Authentication*

| Requirement ID | Requirement Description |
|---|---|
| **FR-AUTH-01** | The system shall register a new user account given a valid email, full name, and password, storing passwords only as salted bcrypt hashes (12 rounds). |
| **FR-AUTH-02** | The system shall reject duplicate user registrations with identical normalized (lowercase) email addresses with HTTP 400 Bad Request. |
| **FR-AUTH-03** | The system shall authenticate valid credentials and issue a 15-minute stateless JWT access token and a 7-day cryptographic refresh token. |
| **FR-AUTH-04** | The system shall reject login requests containing invalid passwords or non-existent email addresses with generic HTTP 401 Unauthorized responses. |
| **FR-AUTH-05** | The system shall store a SHA-256 hash of every issued refresh token in the `user_sessions` database table along with its exact UTC expiration timestamp. |
| **FR-AUTH-06** | The system shall provide an endpoint `/api/auth/refresh` that validates the supplied refresh token against the database session and issues a new access token. |
| **FR-AUTH-07** | The system shall immediately reject refresh attempts referencing expired, modified, or previously revoked refresh tokens with HTTP 401 Unauthorized. |
| **FR-AUTH-08** | The system shall provide an endpoint `/api/auth/logout` that marks the active session record as revoked (`is_revoked = True`). |
| **FR-AUTH-09** | The system shall return the public profile of the authenticated user via `/api/users/me` when supplied with a valid Bearer token. |
| **FR-AUTH-10** | The system shall reject any request missing an `Authorization` header with HTTP 401 Unauthorized on protected routes. |

#### B2.2 Role-Based Access Control (FR-RBAC)

*Table 6: Functional Requirements — Role-Based Access Control*

| Requirement ID | Requirement Description |
|---|---|
| **FR-RBAC-01** | The system shall assign the default role of `patient` to all self-registered accounts. |
| **FR-RBAC-02** | The system shall recognize three distinct authorization roles: `patient`, `admin`, and `super_admin`. |
| **FR-RBAC-03** | The system shall enforce role checks on the backend using reusable FastAPI dependencies (`require_admin`, `require_super_admin`). |
| **FR-RBAC-04** | The system shall return HTTP 403 Forbidden whenever a `patient` attempts to access administrative endpoints under `/api/admin/*`. |
| **FR-RBAC-05** | The system shall enforce query-level ownership checks on all medicine and dose operations, automatically scoping results to `Medicine.user_id == current_user.id`. |
| **FR-RBAC-06** | The system shall return HTTP 404 Not Found when a user attempts to read, edit, or delete a medicine record belonging to another user. |
| **FR-RBAC-07** | The system shall block secondary administrators from altering, demoting, or modifying the Main System Administrator (`admin@example.com`), returning HTTP 403 Forbidden. |
| **FR-RBAC-08** | The system shall restrict user account deletion exclusively to the Main System Administrator, blocking secondary administrators with HTTP 403 Forbidden. |

#### B2.3 Admin Oversight & Governance (FR-ADM)

*Table 7: Functional Requirements — Administration*

| Requirement ID | Requirement Description |
|---|---|
| **FR-ADM-01** | The system shall provide aggregated system statistics via `GET /api/admin/stats` including total users, patients, admins, medicines, active medicines, and doses taken today. |
| **FR-ADM-02** | The system shall provide a complete directory of all registered users via `GET /api/admin/users`, including each user's assigned role, registration timestamp, and medicine counts. |
| **FR-ADM-03** | The system shall enable administrators to update user roles between `patient` and `admin` via `PUT /api/admin/users/{user_id}/role`. |
| **FR-ADM-04** | The system shall prevent administrators from demoting or altering their own role via the admin interface to avoid accidental lockout. |
| **FR-ADM-05** | The system shall allow the Main System Administrator to permanently delete a user and all cascade-associated records via `DELETE /api/admin/users/{user_id}`. |
| **FR-ADM-06** | The system shall block deletion attempts directed at the Main System Administrator with HTTP 403 Forbidden. |
| **FR-ADM-07** | The system shall prevent administrators from deleting their own account via the admin portal with HTTP 400 Bad Request. |

#### B2.4 Domain Requirements — Medicine & Dose Tracking (FR-DOMAIN)

*Table 8: Functional Requirements — Domain Resources*

| Requirement ID | Requirement Description |
|---|---|
| **FR-DOMAIN-01** | The system shall allow authenticated patients to create medicine records containing medicine name, dosage, frequency, reminder time, start date, and end date. |
| **FR-DOMAIN-02** | The system shall retrieve only active and configured medicines belonging to the authenticated user via `GET /api/medicines`. |
| **FR-DOMAIN-03** | The system shall allow patients to update existing medicine records they own via `PUT /api/medicines/{id}`. |
| **FR-DOMAIN-04** | The system shall allow patients to permanently delete medicine records they own via `DELETE /api/medicines/{id}`. |
| **FR-DOMAIN-05** | The system shall compute today's medication schedule via `GET /api/medicines/schedule/today`, checking date ranges and scheduled reminder times against today's date. |
| **FR-DOMAIN-06** | The system shall allow patients to log a dose action (`taken`, `skipped`, or `missed`) with an optional note via `POST /api/medicines/{id}/doses`. |
| **FR-DOMAIN-07** | The system shall retrieve the chronological history of logged doses for the authenticated patient via `GET /api/medicines/doses/history`. |
| **FR-DOMAIN-08** | The system shall dynamically reflect logged doses in today's schedule, displaying an indicator (`is_fully_taken = true`) when all scheduled doses for the day have been completed. |

### B3. Non-Functional Requirements

*Table 9: Non-Functional Requirements*

| Metric | Category | Specification / Target | Verification Method |
|---|---|---|---|
| **NFR-SEC-01** | Security | Cryptographic secrets (JWT Secret, Database URLs) must be supplied solely via environment variables; never hardcoded in source control. | Static scan of git commit history & codebase. |
| **NFR-SEC-02** | Security | Passwords hashed using bcrypt with work factor 12. Refresh tokens hashed using SHA-256 before database persistence. | Code audit of `auth.py`. |
| **NFR-SEC-03** | Security | Authentication errors must return uniform generic error messages ("Invalid email or password") to prevent user enumeration. | Automated test asserting identical 401 error message for wrong password and non-existent email. |
| **NFR-PERF-01** | Performance | API endpoints must respond within 500ms under standard operational conditions. | Vercel production analytics and network waterfall. |
| **NFR-PERF-02** | Performance | Serverless backend must utilize SQLAlchemy `NullPool` to prevent pool exhaustion on serverless cold starts. | Database connection monitor in Supabase dashboard. |
| **NFR-USA-01** | Usability | Responsive design supporting mobile (375px+), tablet, and desktop viewports with zero horizontal scrolling. | Responsive browser testing across standard breakpoints. |
| **NFR-USA-02** | Usability | The frontend must display visual loading spinners during asynchronous network requests and actionable toast error alerts on failure. | UI inspection during simulated network throttling. |
| **NFR-REL-01** | Reliability | 100% data persistence across serverless cold boots and container recycling via managed PostgreSQL 17. | Multi-day uptime monitoring and database audit. |
| **NFR-MAINT-01**| Maintainability | Centralized authentication and RBAC dependency injection pattern ensuring all authorization logic resides in a single module (`auth.py`). | Code architectural review. |

### B4. Roles and Permission Matrix

*Table 10: Endpoint Groups Against Roles*

| Endpoint Group | Visitor | Patient (User) | Secondary Admin (Vatista) | Main System Admin |
|---|---|---|---|---|
| `POST /api/auth/signup` | Yes | Yes | Yes | Yes |
| `POST /api/auth/login` | Yes | Yes | Yes | Yes |
| `POST /api/auth/refresh` | Yes | Yes | Yes | Yes |
| `POST /api/auth/logout` | No | Yes | Yes | Yes |
| `GET /api/users/me` | No | Yes (Own) | Yes (Own) | Yes (Own) |
| `GET /api/medicines` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `POST /api/medicines` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `PUT /api/medicines/{id}` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `DELETE /api/medicines/{id}` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `GET /api/medicines/schedule/today` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `POST /api/medicines/{id}/doses` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `GET /api/medicines/doses/history` | No | Yes (Own records) | Yes (Own records) | Yes (Own records) |
| `GET /api/admin/stats` | No | No (403) | Yes | Yes |
| `GET /api/admin/users` | No | No (403) | Yes | Yes |
| `PUT /api/admin/users/{id}/role` | No | No (403) | Yes (Patients only) | Yes (All accounts except Main Admin) |
| `DELETE /api/admin/users/{id}` | No | No (403) | No (403) | Yes (Except Main Admin & Self) |

*Table 11: Granular Role Capabilities*

| Role Capability | Patient | Secondary Admin | Main System Admin |
|---|---|---|---|
| Self-Registration & Login | Yes | Yes | Yes |
| Manage Personal Prescription List | Yes | Yes | Yes |
| Log Personal Dose Adherence | Yes | Yes | Yes |
| View System Aggregate Analytics | No | Yes | Yes |
| View Platform User Directory | No | Yes | Yes |
| Promote Patient to Admin | No | Yes | Yes |
| Demote Fellow Admin to Patient | No | No | Yes |
| Promote Admin to Super Admin | No | No | Yes |
| Delete Patient Accounts | No | No | Yes |
| Alter Main System Administrator | No | No | No (Blocked by code) |

*Table 12: Admin Hierarchical Rules*

| Protection Rule | Secondary Admin Behavior | Main Admin Behavior | Enforcement Mechanism |
|---|---|---|---|
| **Self-Demotion Prevention** | Cannot demote self from admin panel | Cannot demote self from admin panel | Checked in `update_user_role` handler |
| **Main Admin Tampering** | HTTP 403 Forbidden: "Cannot modify, demote, or alter role of Main Admin" | Blocked: Main Admin role cannot be reduced | Guard clause in `backend/routers/admin.py` |
| **Account Deletion Authority** | HTTP 403 Forbidden: "Only Main Admin has authority to delete users" | Permitted for non-admin accounts | Role check `is_main_admin_user(admin)` |
| **Self-Deletion Safeguard** | HTTP 400 Bad Request: "Cannot delete own account" | HTTP 400 Bad Request: "Cannot delete own account" | `user_id == admin.id` validation |

### B5. Use Cases

```mermaid
flowchart LR
    Visitor((Visitor))
    Patient((Patient))
    SecAdmin((Secondary Admin))
    MainAdmin((Main Admin))

    subgraph Auth Module
        UC1[UC-01: Log In & Refresh Session]
        UC2[UC-02: Log Out & Revoke Session]
    end

    subgraph Domain Module
        UC3[UC-03: Create Medicine Schedule]
        UC4[UC-04: Log Dose Taken / Skipped]
    end

    subgraph Security & RBAC Module
        UC5[UC-05: Denied Cross-Tenant Access]
        UC6[UC-06: Secondary Admin Blocked from Demoting Main Admin]
    end

    subgraph Admin Governance
        UC7[UC-07: Inspect System Stats & User Directory]
        UC8[UC-08: Main Admin Purges Inactive User]
    end

    Visitor --> UC1
    Patient --> UC1
    Patient --> UC2
    Patient --> UC3
    Patient --> UC4
    Patient -.->|Forbidden| UC5
    SecAdmin --> UC7
    SecAdmin -.->|Blocked 403| UC6
    MainAdmin --> UC7
    MainAdmin --> UC8
```

*Figure 1: Use Case Diagram for Medicine Reminder System.*

*Table 13: Detailed Use Case Descriptions*

| Use Case ID & Title | Primary Actor | Preconditions | Main Success Flow (Steps) | Alternative / Error Flows | Postconditions |
|---|---|---|---|---|---|
| **UC-01: Authenticate and Refresh Session** | Visitor / Patient | Registered account exists with password. | 1. User submits email and password.<br>2. System verifies bcrypt hash.<br>3. System issues access token (15m) and refresh token (7d).<br>4. Client makes API requests with Bearer token.<br>5. Upon 401 expiry, client calls `/api/auth/refresh`.<br>6. Server returns fresh access token. | **E1 (Wrong Password):** Returns HTTP 401 Unauthorized.<br>**E2 (Expired/Revoked Refresh):** Returns HTTP 401; user redirected to login. | Active authenticated session maintained seamlessly. |
| **UC-02: Record Daily Dose Action** | Patient | Patient is logged in; medicine exists active for today. | 1. Patient opens Dashboard.<br>2. Patient views today's schedule.<br>3. Patient clicks "Take Dose" for morning slot.<br>4. Client sends `POST /api/medicines/{id}/doses`.<br>5. Server creates `dose_logs` row with status="taken".<br>6. Dashboard updates schedule card to show completed state. | **E1 (Unauthorized):** Returns HTTP 401 if token expired.<br>**E2 (Medicine Not Found):** Returns HTTP 404 if invalid ID. | Dose adherence recorded with timestamp; visible in history. |
| **UC-03: Create New Medicine Schedule** | Patient | Authenticated patient on Dashboard. | 1. Patient clicks "+ Add Medicine".<br>2. Patient enters name, dosage, frequency, reminder time, start/end dates.<br>3. Client sends `POST /api/medicines`.<br>4. Backend validates fields, assigns `user_id = current_user.id`, persists to PostgreSQL.<br>5. Backend returns HTTP 201 Created.<br>6. Medicine card renders on patient dashboard. | **E1 (Validation Error):** Missing required fields returns HTTP 422 Unprocessable Entity. | Medicine record stored and visible solely to creating user. |
| **UC-04: Denied Cross-Tenant Access Attempt** | Patient B | Patient B is logged in; Patient A has created Medicine #42. | 1. Patient B attempts `GET /api/medicines/42`.<br>2. Backend queries `Medicine` filtering by `id == 42` AND `user_id == Patient B.id`.<br>3. Query yields no result.<br>4. Backend returns HTTP 404 Not Found.<br>5. Patient B learns nothing about the existence or contents of Patient A's prescription. | **Alt Flow:** Patient B attempts `PUT` or `DELETE` on ID 42; server returns HTTP 404 Not Found. | Cross-tenant privacy maintained; zero data leakage. |
| **UC-05: Secondary Admin Demotion Blocked** | Secondary Admin (Vatista) | Vatista is logged in with `admin` role. | 1. Vatista opens Admin Dashboard.<br>2. Vatista locates Main Admin (`admin@example.com`).<br>3. Vatista attempts `PUT /api/admin/users/{main_admin_id}/role` to change role to `patient`.<br>4. Backend detects `target_is_main_admin == True`.<br>5. Backend raises HTTP 403 Forbidden with detail message.<br>6. Main Admin role remains untouched. | **Alt Flow:** Vatista attempts to promote self to `super_admin`; backend rejects with HTTP 403 Forbidden. | Main System Administrator remains fully protected. |
| **UC-06: Purge Inactive Account** | Main System Admin | Main Admin logged in with `super_admin` / `is_main_admin = True`. | 1. Main Admin navigates to User Management.<br>2. Main Admin clicks "Delete" on inactive test account.<br>3. Main Admin confirms deletion prompt.<br>4. Client issues `DELETE /api/admin/users/{target_id}`.<br>5. Backend verifies caller is Main Admin and target is not Main Admin or self.<br>6. Cascade deletion executes, purging user, sessions, medicines, and dose logs.<br>7. Backend returns HTTP 200 OK. | **E1 (Secondary Admin Attempt):** Returns HTTP 403 Forbidden.<br>**E2 (Self-Delete Attempt):** Returns HTTP 400 Bad Request. | Target user and all associated records permanently purged. |

### B6. Acceptance Criteria

*Table 14: Acceptance Criteria (Given-When-Then)*

| Test Case ID | Scenario | Given (Initial State) | When (Action Triggered) | Then (Expected Outcome) |
|---|---|---|---|---|
| **AC-01** | Token Expiration Response | An access token whose 15-minute validity period has elapsed. | Client makes a request to `GET /api/medicines` with the expired token in the `Authorization` header. | Server rejects request with `401 Unauthorized` and header `WWW-Authenticate: Bearer`. |
| **AC-02** | Tampered Token Signature | An access token whose payload was modified or signed with a wrong secret. | Client makes a request to any protected endpoint. | Server rejects request with `401 Unauthorized: Could not validate credentials`. |
| **AC-03** | User Data Isolation | User A owns Medicine #10; User B is authenticated with their own valid token. | User B makes a request to `GET /api/medicines/10`. | Server returns `404 Not Found`. User A's medicine is completely hidden. |
| **AC-04** | RBAC Admin Protection | User is authenticated with the default `patient` role. | User attempts to access `GET /api/admin/stats` or `GET /api/admin/users`. | Server returns `403 Forbidden: Access forbidden: This action requires role 'admin'`. |
| **AC-05** | Main Admin Immutability | Secondary Admin (Vatista) is authenticated with the `admin` role. | Vatista sends `PUT /api/admin/users/{admin_id}/role` with `role="patient"`. | Server rejects request with `403 Forbidden: You cannot modify, demote, or alter the Main System Administrator`. |
| **AC-06** | Revoked Refresh Token Reuse | A refresh token that was previously invalidated via `/api/auth/logout`. | Client sends `POST /api/auth/refresh` with the invalidated refresh token. | Server rejects request with `401 Unauthorized: This refresh token has been revoked`. |
| **AC-07** | Admin Self-Deletion Guard | Main System Administrator is authenticated with ID #1. | Main Admin sends `DELETE /api/admin/users/1`. | Server rejects request with `400 Bad Request: Administrators cannot delete their own account`. |

### B7. Traceability Matrix

*Table 15: Traceability Matrix*

| Requirement ID | Backend Endpoint / Frontend Screen | Automated Test | Evidence Screenshot |
|---|---|---|---|
| **FR-AUTH-01** | `POST /api/auth/signup` / `AuthPage.tsx` | `test_auth.py::test_signup` | **S1** (Signup form validation) |
| **FR-AUTH-03** | `POST /api/auth/login` / `AuthPage.tsx` | `test_auth.py::test_login` | **S1** (Login & auth error states) |
| **FR-AUTH-06** | `POST /api/auth/refresh` / `authApi.ts` | `test_auth.py::test_refresh` | **S8** (Refresh request & token renewal) |
| **FR-AUTH-08** | `POST /api/auth/logout` / `Dashboard.tsx` | `test_auth.py::test_logout` | **S4** (Session list & logout revoke) |
| **FR-AUTH-09** | `GET /api/users/me` / `Dashboard.tsx` | `test_auth.py::test_me` | **S3** (User profile page) |
| **FR-RBAC-04** | `GET /api/admin/*` / `AdminOverviewModal.tsx` | `test_rbac.py::test_patient_forbidden` | **S6** (Action denied by RBAC: 403 Forbidden) |
| **FR-RBAC-05** | `GET /api/medicines` / `MedicineList.tsx` | `test_auth.py::test_user_isolation` | **S2** (Dashboard showing only user's records) |
| **FR-RBAC-07** | `PUT /api/admin/users/{id}/role` | `test_rbac.py::test_vatista_cannot_demote` | **S13** (Admin protection guard message) |
| **FR-RBAC-08** | `DELETE /api/admin/users/{id}` | `test_rbac.py::test_vatista_cannot_delete` | **S13** (User management actions) |
| **FR-ADM-01** | `GET /api/admin/stats` / `AdminOverviewModal.tsx` | `test_rbac.py::test_stats` | **S10** (Admin overview statistics) |
| **FR-ADM-02** | `GET /api/admin/users` / `AdminOverviewModal.tsx` | `test_rbac.py::test_users_list` | **S11** (User directory with role filters) |
| **FR-DOMAIN-01**| `POST /api/medicines` / `MedicineForm.tsx` | `test_crud.py::test_create` | **S2** (Add Medicine modal) |
| **FR-DOMAIN-05**| `GET /api/medicines/schedule/today` / `Dashboard.tsx` | `test_doses.py::test_schedule` | **S2** (Today's medication schedule) |
| **FR-DOMAIN-06**| `POST /api/medicines/{id}/doses` / `Dashboard.tsx` | `test_doses.py::test_log_dose` | **S2** (Dose logged taken/skipped) |
| **FR-DOMAIN-07**| `GET /api/medicines/doses/history` / `DoseHistoryModal.tsx` | `test_doses.py::test_history` | **S2** (Dose history modal) |

---

## Part C. Technical Design (TDD)

### C1. Technology Stack

*Table 16: Technology Stack*

| Component | Technology | Version | Rationale for Selection |
|---|---|---|---|
| **Frontend Framework** | React | 19.0.0 | Component-based dynamic rendering, fast Virtual DOM, declarative state management. |
| **Language (Frontend)** | TypeScript | 5.5.3 | Static type safety, strict interface contracts matching backend Pydantic schemas. |
| **Build Tool** | Vite | 5.4.1 | Instant Hot Module Replacement (HMR), optimized production Rollup bundling. |
| **Styling & Icons** | Tailwind CSS + Lucide React | 3.4.1 | Utility-first responsive design, consistent design tokens, lightweight SVG icons. |
| **Backend Framework** | FastAPI | 0.115.0+ | Modern high-performance Python ASGI web framework with native async support. |
| **Data Validation** | Pydantic v2 | 2.9.0+ | Strict schema validation, automatic serialization, auto-generated OpenAPI documentation. |
| **Object-Relational Mapping** | SQLAlchemy | 2.0.35+ | Robust database abstraction, declarative models, connection pooling optimization. |
| **Cloud Database** | PostgreSQL (Supabase) | 17.0 | Enterprise relational database, ACID compliance, AWS Sydney cloud availability. |
| **Password Hashing** | bcrypt | 4.2.0 | Proven adaptive password hashing standard with 12 salt rounds resisting GPU attacks. |
| **JWT Library** | PyJWT | 2.9.0 | Industry-standard implementation of RFC 7519 for secure stateless token generation. |
| **Testing Suite** | Starlette TestClient / Pytest | 0.38.0+ | Fast integration testing against simulated HTTP server without external socket overhead. |
| **Deployment Platform** | Vercel | Production | High-availability global edge deployment supporting Python serverless functions & React SPA. |

### C2. System Architecture

```mermaid
flowchart TD
    subgraph Client Tier
        Browser["Web Browser (Patient / Admin)"]
    end

    subgraph Edge Tier - Vercel Cloud
        FrontendSPA["React 19 SPA (Vite Static Build)"]
        APIProxy["Vercel Serverless Function Engine"]
    end

    subgraph Backend Services Tier
        FastAPIApp["FastAPI REST API Service"]
        AuthModule["Auth & RBAC Middleware"]
        RouterAuth["/api/auth & /api/users"]
        RouterMed["/api/medicines & /api/doses"]
        RouterAdmin["/api/admin"]
    end

    subgraph Database Tier - Cloud Supabase Sydney
        PgPooler["Supabase Transaction Pooler (Port 6543/5432)"]
        PostgresDB[(PostgreSQL 17 Database)]
        TableUsers[("users")]
        TableSessions[("user_sessions")]
        TableMedicines[("medicines")]
        TableLogs[("dose_logs")]
    end

    Browser -->|"1. HTTPS Requests / Assets"| FrontendSPA
    Browser -->|"2. API Calls + Bearer Access Token"| APIProxy
    APIProxy -->|"3. ASGI Event Forwarding"| FastAPIApp
    FastAPIApp -->|"4. Authorization & Role Verification"| AuthModule
    AuthModule --> RouterAuth
    AuthModule --> RouterMed
    AuthModule --> RouterAdmin
    RouterAuth & RouterMed & RouterAdmin -->|"5. SQL Queries via SQLAlchemy"| PgPooler
    PgPooler -->|"6. Transactional State Execution"| PostgresDB
    PostgresDB --- TableUsers
    PostgresDB --- TableSessions
    PostgresDB --- TableMedicines
    PostgresDB --- TableLogs
```

*Figure 2: System Architecture Diagram.*

**Arrow Descriptions:**
1. **Arrow 1 (Browser to Frontend SPA):** The client's web browser retrieves compiled HTML, JavaScript chunks, CSS, and static assets from Vercel's global Content Delivery Network (CDN) edge network. This provides sub-50ms static asset delivery and renders the React single-page application.
2. **Arrow 2 (Browser to API Proxy):** The client application transmits asynchronous HTTP requests to `/api/*` endpoints, including JSON payloads and the `Authorization: Bearer <access_token>` header for protected resources.
3. **Arrow 3 (API Proxy to FastAPI App):** Vercel routes `/api/*` traffic via rewrites defined in `vercel.json` to the serverless Python ASGI runtime (`backend/main.py`), initializing cold starts on demand.
4. **Arrow 4 (FastAPI to Auth Module):** Incoming requests traverse FastAPI's dependency injection chain where `get_current_user` decodes the token claims and validates signatures before reaching route handlers.
5. **Arrow 5 (Routers to Supabase Pooler):** Authorized operations execute parameterized SQL queries through SQLAlchemy ORM, routed over TLS to Supabase's transaction connection pooler on port 6543/5432.
6. **Arrow 6 (Pooler to PostgreSQL 17):** The connection pooler manages physical PostgreSQL socket connections to execute transactions across `users`, `user_sessions`, `medicines`, and `dose_logs` tables without serverless socket exhaustion.

### C3. Backend and Frontend Structure

#### Backend Directory Structure (2 Levels)
```text
backend/
├── main.py                  # Application entrypoint, CORS configuration, router mounting, lifespan
├── database.py              # Engine setup, Supabase pooler URL normalization, NullPool config, Base
├── models.py                # SQLAlchemy declarative models (User, UserSession, Medicine, DoseLog)
├── schemas.py               # Pydantic v2 schemas for request validation and response serialization
├── auth.py                  # JWT creation/decoding, bcrypt password hashing, RBAC role dependencies
├── crud.py                  # Query logic for medicines, schedules, and dose adherence logging
├── requirements.txt         # Pinned Python package dependencies for Vercel build environment
├── routers/                 # Modular API route controllers
│   ├── auth.py              # Endpoints for signup, login, refresh, logout, and profile (/me)
│   ├── medicines.py         # Endpoints for medicine CRUD, today's schedule, and dose logging
│   └── admin.py             # Endpoints for system stats, user list, role management, user deletion
└── test_*.py                # Automated test suites (test_auth, test_rbac, test_crud, test_doses)
```

#### Frontend Directory Structure (2 Levels)
```text
frontend/
├── index.html               # Single-page application root HTML template
├── vite.config.ts           # Vite configuration with build targets and API proxy definitions
├── src/
│   ├── main.tsx             # Application bootstrap, DOM rendering, React root initialization
│   ├── App.tsx              # Root component orchestrating global AuthProvider and view routing
│   ├── index.css            # Tailwind CSS directives, typography, and animation styling
│   ├── types.ts             # TypeScript interface definitions for User, Medicine, Schedule, Dose
│   ├── context/             # React Context state management
│   │   └── AuthContext.tsx  # Central authentication state (user, tokens, login, logout, refresh)
│   ├── services/            # Axios API client modules with interceptors
│   │   ├── authApi.ts       # Network requests for auth, token refresh, and user profile
│   │   └── medicineApi.ts   # Network requests for medicine CRUD, daily schedule, and dose logging
│   ├── pages/               # Top-level screen views
│   │   ├── AuthPage.tsx     # Combined login, registration, and role selection interface
│   │   └── Dashboard.tsx    # Primary patient interface with schedule, filters, and actions
│   └── components/          # Reusable UI component modules
│       ├── MedicineCard.tsx # Visual prescription card displaying reminder details and actions
│       ├── MedicineForm.tsx # Modal dialog for creating and editing medication records
│       ├── MedicineList.tsx # Searchable, filterable grid displaying active medication cards
│       ├── DoseHistoryModal.tsx # Chronological log modal showing past taken/skipped doses
│       └── AdminOverviewModal.tsx # Administrative oversight modal for statistics and user management
```

### C4. Data Model

```mermaid
erDiagram
    users ||--o{ user_sessions : "has active"
    users ||--o{ medicines : "owns"
    users ||--o{ dose_logs : "records"
    medicines ||--o{ dose_logs : "logs adherence for"

    users {
        int id PK "Auto-increment"
        string email UK "Unique, Indexed, Lowercase"
        string full_name "User Full Name"
        string hashed_password "bcrypt hash (12 rounds)"
        string role "patient | admin | super_admin"
        boolean is_main_admin "Primary admin flag"
        datetime created_at "Registration UTC timestamp"
    }

    user_sessions {
        int id PK "Auto-increment"
        int user_id FK "References users.id (CASCADE)"
        string token_hash UK "SHA-256 hash of refresh token"
        datetime expires_at "Expiration UTC timestamp"
        boolean is_revoked "Revocation flag"
        datetime created_at "Creation UTC timestamp"
    }

    medicines {
        int id PK "Auto-increment"
        int user_id FK "References users.id (CASCADE)"
        string medicine_name "Prescription title (Indexed)"
        string dosage "e.g. 500mg, 1 tablet"
        string frequency "e.g. Twice daily"
        string reminder_time "e.g. 08:00 AM, 08:00 PM"
        string start_date "YYYY-MM-DD"
        string end_date "YYYY-MM-DD"
        boolean status "Active (True) / Inactive (False)"
    }

    dose_logs {
        int id PK "Auto-increment"
        int medicine_id FK "References medicines.id (CASCADE)"
        int user_id FK "References users.id (CASCADE)"
        string dose_time "Scheduled slot, e.g. 08:00 AM"
        datetime taken_at "Recorded action UTC timestamp"
        string status "taken | skipped | missed"
        text notes "Optional clinical notes"
    }
```

*Figure 3: Entity-Relationship Diagram.*

#### Table Column Schemas

*Table 17: Table Schema — `users`*

| Column | Type | Keys | Constraints & Defaults | Description |
|---|---|---|---|---|
| `id` | `INTEGER` | PK | Auto-increment, Not Null | Unique identifier for user account |
| `email` | `VARCHAR` | UK | Unique, Indexed, Not Null | Normalized user login email |
| `full_name` | `VARCHAR` | - | Not Null | User's full display name |
| `hashed_password`| `VARCHAR` | - | Not Null | Salted bcrypt password hash |
| `role` | `VARCHAR` | - | Default: `'patient'`, Not Null | Assigned authorization role |
| `is_main_admin` | `BOOLEAN` | - | Default: `FALSE`, Not Null | Immutable Main Admin flag |
| `created_at` | `TIMESTAMP` | - | Default: `datetime.utcnow`, Not Null | Account registration timestamp |

*Table 18: Table Schema — `user_sessions`*

| Column | Type | Keys | Constraints & Defaults | Description |
|---|---|---|---|---|
| `id` | `INTEGER` | PK | Auto-increment, Not Null | Unique session record ID |
| `user_id` | `INTEGER` | FK | References `users.id`, Cascade Delete | Associated user identifier |
| `token_hash` | `VARCHAR` | UK | Unique, Indexed, Not Null | SHA-256 hash of refresh token |
| `expires_at` | `TIMESTAMP` | - | Not Null | Absolute UTC expiry timestamp (7 days) |
| `is_revoked` | `BOOLEAN` | - | Default: `FALSE`, Not Null | Instant logout invalidation flag |
| `created_at` | `TIMESTAMP` | - | Default: `datetime.utcnow`, Not Null | Session initialization timestamp |

*Table 19: Table Schema — `medicines`*

| Column | Type | Keys | Constraints & Defaults | Description |
|---|---|---|---|---|
| `id` | `INTEGER` | PK | Auto-increment, Not Null | Unique identifier for medicine record |
| `user_id` | `INTEGER` | FK | References `users.id`, Cascade Delete | Owning patient account ID |
| `medicine_name` | `VARCHAR` | - | Indexed, Not Null | Commercial or generic drug name |
| `dosage` | `VARCHAR` | - | Not Null | Quantity/unit (e.g., "500 mg") |
| `frequency` | `VARCHAR` | - | Not Null | Intake schedule (e.g., "Twice daily") |
| `reminder_time` | `VARCHAR` | - | Not Null | Time strings (e.g., "08:00 AM, 08:00 PM")|
| `start_date` | `VARCHAR` | - | Not Null | Prescribed start date (YYYY-MM-DD) |
| `end_date` | `VARCHAR` | - | Not Null | Prescribed end date (YYYY-MM-DD) |
| `status` | `BOOLEAN` | - | Default: `TRUE`, Not Null | Active therapy indicator |

*Table 20: Table Schema — `dose_logs`*

| Column | Type | Keys | Constraints & Defaults | Description |
|---|---|---|---|---|
| `id` | `INTEGER` | PK | Auto-increment, Not Null | Unique dose log event identifier |
| `medicine_id` | `INTEGER` | FK | References `medicines.id`, Cascade | Associated medicine record ID |
| `user_id` | `INTEGER` | FK | References `users.id`, Cascade Delete | Associated patient ID |
| `dose_time` | `VARCHAR` | - | Not Null | Scheduled time slot string |
| `taken_at` | `TIMESTAMP` | - | Default: `datetime.utcnow`, Not Null | Exact UTC action execution timestamp |
| `status` | `VARCHAR` | - | Default: `'taken'`, Not Null | Adherence status: taken, skipped, missed|
| `notes` | `TEXT` | - | Nullable | Optional user observations or side-effects |

### C5. API Design

The API uses standard JSON request/response formats with error payloads following `{ "detail": "Descriptive error message" }`. All endpoints are prefixed under `/api` (with aliases mounted directly for backwards compatibility).

*Table 21: Complete REST API Endpoints Specification*

| Method | Path | Auth Required | Required Role | Request Body | Success Status | Error Statuses | Description |
|---|---|---|---|---|---|---|---|
| `POST` | `/api/auth/signup` | No | None | `UserSignup` | `201 Created` | `400`, `422` | Register account and issue initial token pair |
| `POST` | `/api/auth/login` | No | None | `UserLogin` | `200 OK` | `401`, `422` | Authenticate credentials and issue token pair |
| `POST` | `/api/auth/refresh` | No | None | `RefreshRequest` | `200 OK` | `401`, `422` | Issue fresh access token from valid refresh token |
| `POST` | `/api/auth/logout` | No | None | `RefreshRequest` | `200 OK` | `422` | Invalidate refresh token session record |
| `GET` | `/api/users/me` | Yes | Authenticated | None | `200 OK` | `401` | Retrieve currently authenticated user profile |
| `GET` | `/api/medicines` | Yes | Authenticated | None | `200 OK` | `401` | Retrieve medicines owned by authenticated user |
| `POST` | `/api/medicines` | Yes | Authenticated | `MedicineCreate`| `201 Created` | `401`, `422` | Create new medicine linked to user ID |
| `GET` | `/api/medicines/{id}` | Yes | Authenticated | None | `200 OK` | `401`, `404` | Get specific medicine (enforces user ownership)|
| `PUT` | `/api/medicines/{id}` | Yes | Authenticated | `MedicineUpdate`| `200 OK` | `401`, `404`, `422` | Update owned medicine record |
| `DELETE`| `/api/medicines/{id}` | Yes | Authenticated | None | `200 OK` | `401`, `404` | Delete owned medicine record |
| `GET` | `/api/medicines/schedule/today` | Yes | Authenticated | None | `200 OK` | `401` | Retrieve computed daily schedule & adherence |
| `POST` | `/api/medicines/{id}/doses` | Yes | Authenticated | `DoseLogCreate` | `201 Created` | `401`, `404`, `422` | Record dose action (taken, skipped, missed) |
| `GET` | `/api/medicines/doses/history` | Yes | Authenticated | None | `200 OK` | `401` | Retrieve recent dose adherence log history |
| `GET` | `/api/admin/stats` | Yes | `admin`, `super_admin` | None | `200 OK` | `401`, `403` | Retrieve system aggregate health metrics |
| `GET` | `/api/admin/users` | Yes | `admin`, `super_admin` | None | `200 OK` | `401`, `403` | Retrieve registered user directory & counts |
| `PUT` | `/api/admin/users/{id}/role` | Yes | `admin`, `super_admin` | `UserRoleUpdate`| `200 OK` | `401`, `403`, `404` | Update user role with hierarchical safeguards |
| `DELETE`| `/api/admin/users/{id}` | Yes | `super_admin` | None | `200 OK` | `400`, `401`, `403`, `404` | Permanently purge user account & records |
| `GET` | `/api/health` | No | None | None | `200 OK` | None | Health check endpoint returning system status |

### C6. JWT Authentication Design

```mermaid
sequenceDiagram
    autonumber
    actor User as Patient / Admin
    participant Browser as Web Browser (React SPA)
    participant API as FastAPI Backend (/api/*)
    participant DB as Supabase PostgreSQL

    Note over User,DB: Phase 1: Authentication & Token Issuance
    User->>Browser: Enters email & password
    Browser->>API: POST /api/auth/login {email, password}
    API->>DB: Query User by email
    DB-->>API: Return User row & hashed_password
    API->>API: Verify bcrypt.checkpw(plain, hash)
    API->>API: Generate 15m JWT Access Token
    API->>API: Generate 7d Opaque Refresh Token + SHA-256 Hash
    API->>DB: INSERT INTO user_sessions (user_id, token_hash, expires_at)
    DB-->>API: Confirm session saved
    API-->>Browser: Return {access_token, refresh_token, user}

    Note over User,DB: Phase 2: Protected Request Execution
    Browser->>API: GET /api/medicines (Headers: Bearer <access_token>)
    API->>API: Verify JWT signature & expiration (HS256)
    API->>DB: SELECT * FROM medicines WHERE user_id = sub
    DB-->>API: Return user's private records
    API-->>Browser: HTTP 200 OK [medicines list]

    Note over User,DB: Phase 3: Token Expiration & Silent Refresh
    Browser->>API: GET /api/medicines (Expired Token)
    API-->>Browser: HTTP 401 Unauthorized (Token expired)
    Browser->>API: POST /api/auth/refresh {refresh_token}
    API->>API: Hash refresh token with SHA-256
    API->>DB: SELECT * FROM user_sessions WHERE token_hash = hash
    DB-->>API: Return session (is_revoked = false, expires_at > now)
    API->>API: Mint new 15m JWT Access Token
    API-->>Browser: HTTP 200 OK {access_token}
    Browser->>API: Re-execute original request with new access token
    API-->>Browser: HTTP 200 OK [medicines list]

    Note over User,DB: Phase 4: Logout & Session Invalidation
    User->>Browser: Clicks "Log Out"
    Browser->>API: POST /api/auth/logout {refresh_token}
    API->>DB: UPDATE user_sessions SET is_revoked = true WHERE token_hash = hash
    DB-->>API: Confirmed
    API-->>Browser: HTTP 200 OK "Session revoked"
    Browser->>Browser: Clear local storage tokens & redirect to /login
```

*Figure 4: JWT Authentication, Refresh, and Session Lifecycle Sequence Diagram.*

*Table 22: JWT Access Token Claims Structure*

| Claim Key | Standard / Custom | Example Value | Description |
|---|---|---|---|
| `sub` | RFC 7519 Subject | `"42"` | Unique user identifier (as string) |
| `email` | Custom Claim | `"patient@example.com"` | User's registered email address |
| `role` | Custom Claim | `"patient"` | Assigned RBAC role (`patient`, `admin`, `super_admin`) |
| `is_main_admin` | Custom Claim | `false` | Boolean flag indicating supreme admin privileges |
| `type` | Custom Claim | `"access"` | Token discriminator preventing refresh token confusion |
| `iat` | RFC 7519 Issued At | `1732567200` | Unix epoch timestamp of token generation |
| `exp` | RFC 7519 Expiration | `1732568100` | Unix epoch timestamp of expiration (exactly 15 minutes) |

#### Token Lifetimes and Storage Rationale
- **Access Token Lifetime (15 Minutes):** A short lifespan limits the exposure window if an access token is intercepted via network sniffing or cross-site scripting (XSS). Because access tokens are stateless, revocation cannot occur until expiration; 15 minutes balances security and performance without overloading the database.
- **Refresh Token Lifetime (7 Days):** A 7-day lifespan allows users to remain logged in during continuous active use without frequent re-authentication prompts, while requiring periodic credential verification.
- **Client Storage & Risk Mitigation:** Tokens are managed by the frontend `AuthContext`. Storing access tokens in application memory and refresh tokens in secure browser storage avoids CSRF vulnerabilities inherent in ambient cookie authentication while Axios interceptors handle silent 401 recovery.
- **Server Verification on Every Request:**
  1. Signature verification using the server's `JWT_SECRET` and `HS256`.
  2. Expiration check (`exp > now`).
  3. Token type validation (`type == "access"`).
  4. Active user existence check in PostgreSQL (`User.id == sub`).
- **Frontend 401 Recovery Workflow:** The Axios interceptor intercepts 401 responses, pauses queued requests, calls `/api/auth/refresh` once, updates authorization headers with the renewed token, and replays failed calls. If refresh returns 401, the session is cleared and the user is redirected to the login view.

### C7. RBAC Design

```mermaid
flowchart TD
    Req[Incoming HTTP Request] --> HasToken{Bearer Token Present?}
    HasToken -- No --> Ret401[Return HTTP 401 Unauthorized]
    HasToken -- Yes --> VerifyJWT{Valid Signature & Exp?}
    VerifyJWT -- No --> Ret401
    VerifyJWT -- Yes --> FetchUser{User Exists in DB?}
    FetchUser -- No --> Ret401
    FetchUser -- Yes --> CheckRole{Endpoint Requires Admin?}
    CheckRole -- No --> EnforceOwner[Enforce Query-Level Ownership]
    CheckRole -- Yes --> IsAdmin{Role in admin, super_admin?}
    IsAdmin -- No --> Ret403[Return HTTP 403 Forbidden]
    IsAdmin -- Yes --> IsMainAdminOp{Target is Main Admin?}
    IsMainAdminOp -- Yes & Caller != Main --> Ret403
    IsMainAdminOp -- No --> ExecuteAdmin[Execute Admin Handler]
    EnforceOwner --> ExecuteUser[Execute Domain Handler]
```

*Figure 5: RBAC Request Authorization Flow.*

#### Reusable Role Dependency Code Excerpt
The following implementation from `backend/auth.py` demonstrates the factory pattern for role validation:

```python
def require_role(allowed_roles: list[str]):
    """
    Factory for role-based authorization dependencies.
    Verifies that the authenticated user's role is within allowed_roles.
    Raises HTTP 403 Forbidden if unauthorized.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = getattr(current_user, "role", "patient") or "patient"
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: This action requires one of: {', '.join(allowed_roles)}. Your role is '{user_role}'.",
            )
        return current_user

    return role_checker

# Pre-configured role dependencies
require_admin = require_role(["admin", "super_admin"])
require_super_admin = require_role(["super_admin"])
```

#### Query-Level Ownership Enforcement
Rather than querying a record and checking ownership after retrieval (which risks authorization bypasses), all database operations enforce ownership directly in the SQL `WHERE` clause:

```python
# Query directly scoped to authenticated user ID
medicine = (
    db.query(Medicine)
    .filter(Medicine.id == medicine_id, Medicine.user_id == current_user.id)
    .first()
)
if not medicine:
    raise HTTPException(status_code=404, detail="Medicine not found")
```
This ensures a user attempting to access an unauthorized record receives an identical `404 Not Found`, giving zero information about whether the resource exists.

### C8. Admin Dashboard Design

```mermaid
flowchart TD
    AdminUser((Admin User)) --> OpenModal[Click 'Admin Portal' in Header]
    OpenModal --> AdminModal[AdminOverviewModal Component]
    
    subgraph Overview View
        AdminModal --> LoadStats[GET /api/admin/stats]
        LoadStats --> StatCards["Metric Cards: Total Users, Patients, Admins, Active Medicines, Doses Today"]
    end

    subgraph Directory View
        AdminModal --> LoadUsers[GET /api/admin/users]
        LoadUsers --> FilterControls["Search by Name/Email & Filter by Role (All/Admin/Patient)"]
        FilterControls --> UserTable["User Records: Email, Role, Medicines Count, Actions"]
    end

    subgraph Management Actions
        UserTable --> PromoteAction["Promote to Admin (PUT /api/admin/users/{id}/role)"]
        UserTable --> DemoteAction["Demote to Patient (PUT /api/admin/users/{id}/role)"]
        UserTable --> DeleteAction["Delete Account (DELETE /api/admin/users/{id})"]
    end
```

*Figure 6: Admin Dashboard Navigation and Data Flow.*

*Table 23: Admin Portal Specifications*

| View Component | Endpoints Called | Filters & Controls | Actions Executed | Safeguards & Security Rules |
|---|---|---|---|---|
| **System Overview** | `GET /api/admin/stats` | Automatic refresh on modal open | Visualizes key health indicators | Read-only; available to all admin roles. |
| **User Directory** | `GET /api/admin/users` | Real-time text search; Role dropdown filter | Paginated table rendering registered users | Passwords hidden; returns aggregated medicine count. |
| **Role Modification**| `PUT /api/admin/users/{id}/role` | Modal select dropdown (`patient`, `admin`) | Updates user role in database | Secondary admins cannot alter Main Admin; cannot demote self. |
| **User Purge** | `DELETE /api/admin/users/{id}` | Confirmation modal prompt | Cascade deletes user and all records | Exclusive to Main Admin; cannot delete Main Admin or self. |

### C9. Security Design and Threats

*Table 24: Security Threats, Defenses, and Code Implementation*

| Security Threat | Attack Vector / Risk | Defensive Strategy | Implementation Location |
|---|---|---|---|
| **Password Database Breach** | Offline dictionary / rainbow table attacks | Salted bcrypt hashing with 12 rounds. Plaintext is never written to disk or memory dumps. | `backend/auth.py` (`hash_password`, `verify_password`) |
| **Stolen Access Token** | Interception of stateless Bearer token | Short 15-minute token lifetime limits exposure; requires active refresh token to renew. | `backend/auth.py` (`ACCESS_TOKEN_EXPIRE_MINUTES = 15`) |
| **Stolen Refresh Token** | Attacker attempts to maintain perpetual session | Refresh tokens stored as SHA-256 hashes; instant invalidation via `/api/auth/logout`. | `backend/routers/auth.py` (`user_sessions` table) |
| **Brute-Force Credential Attack**| Automated credential stuffing against `/login` | Constant-time password verification; uniform generic 401 error message for wrong password or user. | `backend/routers/auth.py` (`login` handler) |
| **Privilege Escalation** | Patient attempts administrative operations | Role validation via `require_admin` dependency; token tampering invalidates cryptographic signature. | `backend/auth.py` (`require_role`) |
| **Cross-Tenant Data Tampering**| Insecure Direct Object References (IDOR) | Ownership enforcement directly in database `WHERE` clause (`Medicine.user_id == current_user.id`). | `backend/crud.py`, `backend/routers/medicines.py` |
| **Cross-Site Scripting (XSS)** | Malicious JavaScript injection | React automatic JSX context escaping; strict TypeScript string typing. | `frontend/src/components/*` |
| **Cross-Site Request Forgery** | Ambient credential exploitation | Bearer token authorization header required; standard forms cannot automatically attach custom headers. | `frontend/src/services/authApi.ts` |
| **SQL Injection (SQLi)** | Malicious SQL syntax in search/form inputs | 100% parameterized queries generated via SQLAlchemy ORM; no raw concatenated SQL strings. | `backend/database.py`, `backend/crud.py` |
| **Admin Takeover** | Secondary admin demotes or deletes system owner | Strict code-level immutability rules protecting `admin@example.com` and `is_main_admin = True`. | `backend/routers/admin.py` (`update_user_role`, `delete_user`)|
| **Secrets in Repository** | Leaked database credentials or signing keys | All sensitive variables loaded from `.env` via `python-dotenv` and Vercel Environment Variables. | `backend/database.py`, `backend/auth.py` |
| **Over-Posting / Mass Assignment**| Injecting arbitrary columns (e.g. `role="admin"`) | Strict Pydantic models whitelist allowed input fields; extra fields are rejected or stripped. | `backend/schemas.py` |

### C10. Deployment on Vercel

```mermaid
flowchart LR
    subgraph Vercel Production Environment
        EdgeRouting["Vercel Edge Gateway (2130537-s6.vercel.app)"]
        StaticCDN["Static Asset CDN (React 19 SPA)"]
        ServerlessPy["Serverless Python Runtime (backend/main.py)"]
    end

    subgraph Supabase Cloud
        Pooler["Connection Pooler (aws-0-ap-southeast-2.pooler.supabase.com:6543)"]
        Postgres17["PostgreSQL 17 Database Engine"]
    end

    EdgeRouting -->|"/assets/*, /"| StaticCDN
    EdgeRouting -->|"/api/*, /auth/*"| ServerlessPy
    ServerlessPy -->|"SQL via SQLAlchemy NullPool"| Pooler
    Pooler --> Postgres17
```

*Figure 7: Vercel Cloud Serverless Deployment Architecture.*

*Table 25: Production Environment Variables*

| Variable Name | Required Scope | Purpose / Description | Value Format |
|---|---|---|---|
| `DATABASE_URL` | Vercel Backend / Production | PostgreSQL connection pooler string with credentials and SSL parameters | `postgresql://user:pass@host:6543/postgres?sslmode=require` |
| `JWT_SECRET` | Vercel Backend / Production | Cryptographic secret key used for signing and verifying HS256 JWTs | High-entropy 64-character random string |
| `VITE_API_URL` | Vercel Frontend / Production | Base URL for frontend Axios client calls (empty string for relative routing)| `""` (relative paths routed via `vercel.json`) |

#### Redeployment and Build Configuration
The project is configured as a monorepo in `vercel.json`:
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/dist`
- **Rewrites Configuration:** Directs `/api/(.*)` requests to `backend/main.py`, while all remaining non-file routes fall back to `/index.html` to support client-side routing.
- **Redeployment Procedure:** Pushing a commit to `origin/main` automatically triggers a zero-downtime production deployment on Vercel.

### C11. Testing

The testing strategy combines comprehensive automated integration testing against the backend REST API with systematic manual end-to-end verification on the deployed production environment.

*Table 26: Automated Test Suite Execution Results*

| Test Name | Suite File | Requirement Checked | Status | Key Verification Output |
|---|---|---|---|---|
| `test_signup_success` | `test_auth.py` | FR-AUTH-01 | **PASS** | Account created, bcrypt hash verified, token pair issued |
| `test_duplicate_email_rejected`| `test_auth.py` | FR-AUTH-02 | **PASS** | Duplicate registration returns HTTP 400 Bad Request |
| `test_wrong_password_rejected` | `test_auth.py` | FR-AUTH-04 | **PASS** | Invalid credentials return generic HTTP 401 Unauthorized |
| `test_user_profile_me` | `test_auth.py` | FR-AUTH-09 | **PASS** | Valid Bearer token returns authenticated user profile |
| `test_refresh_session` | `test_auth.py` | FR-AUTH-06 | **PASS** | Valid refresh token issues fresh access token |
| `test_user_data_isolation` | `test_auth.py` | FR-RBAC-05 | **PASS** | User B cannot view User A's medicine; direct ID returns 404 |
| `test_logout_and_revocation` | `test_auth.py` | FR-AUTH-08 | **PASS** | Session revoked; revoked refresh token reuse returns 401 |
| `test_unauthenticated_admin` | `test_rbac.py` | FR-AUTH-10 | **PASS** | Accessing `/api/admin/stats` without token returns 401 |
| `test_patient_admin_forbidden` | `test_rbac.py` | FR-RBAC-04 | **PASS** | Patient role accessing admin endpoints returns 403 Forbidden |
| `test_secondary_admin_access` | `test_rbac.py` | FR-ADM-01 | **PASS** | Vatista accesses stats and users directory with 200 OK |
| `test_vatista_cannot_demote` | `test_rbac.py` | FR-RBAC-07 | **PASS** | Vatista altering Main Admin returns 403 Forbidden |
| `test_vatista_cannot_delete` | `test_rbac.py` | FR-RBAC-08 | **PASS** | Vatista deleting Main Admin returns 403 Forbidden |
| `test_main_admin_delete_user` | `test_rbac.py` | FR-ADM-05 | **PASS** | Main Admin successfully deletes target test account |
| `test_admin_self_delete_guard`| `test_rbac.py` | FR-ADM-07 | **PASS** | Admin deleting self returns HTTP 400 Bad Request |
| `test_crud_medicine_lifecycle` | `test_crud.py` | FR-DOMAIN-01..04 | **PASS** | Complete Create, Read, Update, Delete cycle verified |
| `test_today_schedule_computed` | `test_doses.py` | FR-DOMAIN-05 | **PASS** | Active medicines filtered for current date schedule |
| `test_log_dose_action` | `test_doses.py` | FR-DOMAIN-06 | **PASS** | Dose recorded as "taken" with UTC timestamp |
| `test_dose_history_retrieval` | `test_doses.py` | FR-DOMAIN-07 | **PASS** | Chronological dose log history retrieved successfully |

---

## Part D. Evidence: Screenshots of the Running Application

> **Note on Submission Format:** Per the instructor's guidelines, actual graphical screenshots with the browser address bar visible must be embedded in the submitted PDF report. The placeholders below identify the exact evidence item, requirements verified, and expected visual proof.

### D1. User Side
- **[S1: Signup and Login Page]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-AUTH-01`, `FR-AUTH-04`  
  *Caption:* Login interface displaying validation error handling when invalid credentials or weak passwords are submitted.
- **[S2: Main Feature Page of Logged-In User]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-RBAC-05`, `FR-DOMAIN-02`, `FR-DOMAIN-05`  
  *Caption:* Patient dashboard showing today's medication schedule, active prescriptions, and dose action buttons ("Take", "Skip"). Only records owned by the logged-in user are visible.
- **[S3: User Profile & Authentication Verification]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-AUTH-09`  
  *Caption:* User profile display verifying current session metadata and email identity returned by `GET /api/users/me`.
- **[S4: Session Logout & Revocation]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-AUTH-08`  
  *Caption:* Patient initiating logout; refresh token revoked in `user_sessions` and client state reset to unauthenticated.
- **[S5: Multi-Tenant Role Representation]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-RBAC-01`, `FR-RBAC-02`  
  *Caption:* Display showing user interface adapted to the assigned role (`patient` vs. `admin` portal badge).
- **[S6: Action Denied by RBAC (403 Forbidden)]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-RBAC-04`  
  *Caption:* Network console proving HTTP 403 Forbidden response when a regular patient attempts to request `/api/admin/stats`.

### D2. Security Behaviour
- **[S7: Expired Token Returning 401 Unauthorized]**  
  *URL:* `https://2130537-s6.vercel.app/api/medicines`  
  *Requirement Verified:* `AC-01`, `FR-AUTH-07`  
  *Caption:* Browser DevTools Network tab showing `Authorization: Bearer [MASKED]` header and server response `401 Unauthorized` upon access token expiration.
- **[S8: Silent Token Refresh Request]**  
  *URL:* `https://2130537-s6.vercel.app/api/auth/refresh`  
  *Requirement Verified:* `FR-AUTH-06`  
  *Caption:* Network tab showing successful `POST /api/auth/refresh` returning a fresh 15-minute access token without user interruption.
- **[S9: Blocked Reuse of Revoked Token]**  
  *URL:* `https://2130537-s6.vercel.app/api/auth/refresh`  
  *Requirement Verified:* `AC-06`, `FR-AUTH-08`  
  *Caption:* DevTools showing HTTP 401 response with message `"This refresh token has been revoked"` when an invalidated token is reused.

### D3. Admin Dashboard
- **[S10: System Overview Statistics]**  
  *URL:* `https://2130537-s6.vercel.app` (Admin Portal)  
  *Requirement Verified:* `FR-ADM-01`  
  *Caption:* Admin dashboard displaying real-time metrics: Total Users, Patients, Admins, Active Medicines, and Doses Taken Today.
- **[S11: Users Directory with Search and Filters]**  
  *URL:* `https://2130537-s6.vercel.app` (Admin Portal)  
  *Requirement Verified:* `FR-ADM-02`  
  *Caption:* User management table showing registered accounts, role tags, creation dates, and prescription counts with dynamic search filtering.
- **[S12: User Detail & Medication Metrics]**  
  *URL:* `https://2130537-s6.vercel.app` (Admin Portal)  
  *Requirement Verified:* `FR-ADM-02`  
  *Caption:* Expanded row view showing individual patient adherence rates and active medication counts.
- **[S13: Admin Role Protection & Hierarchy Guard]**  
  *URL:* `https://2130537-s6.vercel.app` (Admin Portal)  
  *Requirement Verified:* `FR-RBAC-07`, `AC-05`  
  *Caption:* Error toast alert and DevTools showing HTTP 403 Forbidden when Secondary Admin (Vatista) attempts to alter the Main Administrator.
- **[S14: User Account Management & Role Promotion]**  
  *URL:* `https://2130537-s6.vercel.app` (Admin Portal)  
  *Requirement Verified:* `FR-ADM-03`  
  *Caption:* Main Admin successfully elevating a patient to the `admin` role with updated status badge in the UI.
- **[S15: Dose Adherence History Modal]**  
  *URL:* `https://2130537-s6.vercel.app`  
  *Requirement Verified:* `FR-DOMAIN-07`  
  *Caption:* Chronological audit log showing historical dose actions, scheduled slots, recorded timestamps, and clinical notes.
- **[S16: Health Diagnostics & Database Status]**  
  *URL:* `https://2130537-s6.vercel.app/api/health`  
  *Requirement Verified:* `NFR-REL-01`  
  *Caption:* JSON response from `/api/health` confirming system operational status.
- **[S17: Interactive OpenAPI Documentation]**  
  *URL:* `https://2130537-s6.vercel.app/api/docs`  
  *Requirement Verified:* `NFR-MAINT-01`  
  *Caption:* Swagger UI documentation page showing all schemas and endpoints available on the production API.

### D4. Deployment
- **[S18: Vercel Production Deployment Overview]**  
  *URL:* `https://vercel.com/mahathirprantos-projects/medicine-reminder-system`  
  *Requirement Verified:* `C10`  
  *Caption:* Vercel project dashboard showing active production deployment, custom production domain `2130537-s6.vercel.app`, and clean build logs.
- **[S19: Vercel Environment Variables Configuration]**  
  *URL:* Vercel Project Settings > Environment Variables  
  *Requirement Verified:* `NFR-SEC-01`  
  *Caption:* Masked dashboard view confirming `DATABASE_URL` and `JWT_SECRET` configured for production without exposing secret values.
- **[S20: Supabase Cloud Database Infrastructure]**  
  *URL:* Supabase Dashboard (Sydney Region)  
  *Requirement Verified:* `C4`, `C10`  
  *Caption:* Supabase dashboard table viewer showing tables (`users`, `user_sessions`, `medicines`, `dose_logs`) populated in PostgreSQL 17.

### D5. Tests
- **[S21: Automated Test Suite Execution Output]**  
  *Command:* `python test_auth.py && python test_rbac.py && python test_crud.py && python test_doses.py`  
  *Requirement Verified:* `C11`  
  *Caption:* Terminal console output showing 100% passing tests across authentication, RBAC, CRUD, and dose tracking suites.

---

## Part E. Project Management and Conclusion

### E1. How to Run and Test

#### Prerequisites
- Python 3.11+ installed locally.
- Node.js 18+ and npm installed.
- Git installed.

#### Step 1: Clone Repository & Setup Environment
```bash
git clone https://github.com/mahathirpranto/Medicine-Reminder-System.git
cd Medicine-Reminder-System
```

#### Step 2: Configure Environment Variables
Create a file named `.env` inside the `backend/` directory:
```env
DATABASE_URL=postgresql://postgres.<db_user>:<db_password>@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require
JWT_SECRET=your-secure-jwt-secret-key-here
```

#### Step 3: Run Backend Service
```bash
cd backend
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*Backend Swagger Docs will be accessible at:* `http://localhost:8000/docs`

#### Step 4: Run Frontend Development Server
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
*Frontend will be accessible at:* `http://localhost:5173`

#### Step 5: Execute Automated Test Suites
From the `backend/` directory with virtual environment activated:
```bash
python test_auth.py
python test_rbac.py
python test_crud.py
python test_doses.py
```

*(Note: To log in with demo accounts, refer to the account credentials listed in the PDF report Appendix. Credentials are deliberately excluded from this file to comply with security guidelines).*

### E2. GitHub Work

*Table 27: Major Git Commits, Features, and Deliverables*

| Commit / PR Reference | Feature Title | Deliverables & Work Description |
|---|---|---|
| `feat(auth): jwt-tokens` | JWT Authentication & Sessions | Implemented access and refresh token mechanics, bcrypt hashing, and `user_sessions` table in `backend/auth.py`. |
| `feat(rbac): role-guards` | Role-Based Access Control | Added `require_role`, `require_admin`, and hierarchical immutability safeguarding Main Admin. |
| `feat(domain): dose-logs` | Dose Adherence & Scheduling | Built today's schedule generation, one-click dose action endpoint, and dose log history tracking. |
| `feat(admin): admin-portal` | Administrative Dashboard | Created `AdminOverviewModal.tsx` and backend endpoints for statistics, user list, and role updates. |
| `fix(db): supabase-pooling` | Supabase Cloud Database | Connected to PostgreSQL 17 in Sydney (`aws-0-ap-southeast-2.pooler.supabase.com:6543`) with `NullPool` architecture. |
| `deploy(vercel): monorepo` | Vercel Cloud Deployment | Configured `vercel.json` rewrites for unified serverless backend and React SPA deployment. |

### E3. Limitations
1. **Push Notifications Require Active Browser Session:** Web notification capabilities depend on browser permissions and client activity; native mobile lockscreen notifications are not supported without a native app wrapper.
2. **Offline Mode Functionality:** The application requires an active internet connection to communicate with the cloud database. If a user loses connectivity, new doses cannot be recorded until reconnected.
3. **Timezone Adjustments:** While timestamps are recorded in UTC, schedule filtering relies on the user's browser local date string; crossing international timezones mid-day may shift scheduled slots by hours.

### E4. Future Work
1. **Service Worker Push Notifications:** Implement Web Push API with VAPID keys to deliver scheduled medication notifications even when the browser tab is closed.
2. **Caregiver / Family Sharing Permissions:** Allow patients to grant read-only visibility to trusted family members or caregivers to verify adherence remotely.
3. **Prescription OCR & Barcode Scanning:** Integrate computer vision libraries to scan medication box barcodes to prefill medicine names and dosages automatically.
4. **Data Export for Physicians:** Enable one-click PDF/CSV export of medication adherence history formatted for clinical review during doctor appointments.

### E5. Sources, Libraries and Tools

*Table 28: Attribution of Sources, Libraries, and Tools*

| Resource / Tool | Version / Reference | Purpose & Scope of Use | Modifications / Verification Conducted |
|---|---|---|---|
| **FastAPI Documentation** | v0.115.0 (tiangolo.com) | Official guidance for dependency injection and OAuth2 Bearer setup | Customized to support dual-token refresh rotation and SQLAlchemy session integration. |
| **PyJWT** | RFC 7519 Implementation | Stateless JWT encoding and decoding | Configured with explicit token type validation to prevent token confusion. |
| **bcrypt** | v4.2.0 | Cryptographic password hashing | Tuned to 12 work rounds to balance serverless latency with brute-force defense. |
| **Supabase** | PostgreSQL 17 | Cloud database hosting and connection pooler | Configured transaction pooler port 6543 and normalized connection strings to bypass libpq unsupported keys. |
| **Tailwind CSS** | v3.4.1 | Utility-first CSS styling framework | Customized color themes, alert banners, and responsive card layouts. |
| **Lucide React** | v0.468.0 | Iconography | Selected semantic healthcare icons (pills, clock, check, shield, user). |
| **Antigravity AI (DeepMind)**| Pair Programming Assistant | Code refactoring, test script authoring, and documentation generation | All generated schemas, endpoints, and security rules were manually tested and verified against live Vercel deployments. |

---

## Appendix. Test Accounts and Video Demo

### Video Demonstration Link
- **Deployed URL Video Demo:** [https://youtu.be/placeholder-demo-video](https://youtu.be/placeholder-demo-video)  
*(Duration: 5–8 minutes detailing patient scheduling, dose logging, RBAC protections, and admin dashboard operations on the live Vercel deployment).*

### Demo Test Accounts Description
In accordance with strict security standards and course instructions:
> *"Never write the user IDs or passwords in this Markdown file, and never write passwords anywhere else in the repository: GitHub flags them as leaked credentials. Put them only in the PDF report Appendix."*

The live platform is pre-configured with three distinct accounts representing all permission tiers:
1. **Main System Administrator (`super_admin`):** Has complete platform privileges including user deletion and role assignment. Protected against demotion and deletion.
2. **Secondary Administrator (`admin` - Vatista):** Has access to platform statistics, user directories, and patient role updates. Blocked from demoting or deleting the Main System Administrator.
3. **Patient (`patient`):** Standard user account with personal prescription scheduling, dose adherence logging, and dose history. Strictly restricted from administrative endpoints and other patients' records.

*Please refer to the Appendix of the submitted PDF document for the confidential email addresses and passwords required to log into each role.*

# Production Deployment & Supabase Integration Report

## 1. Executive Summary
This document records the production deployment and cloud database integration for the **Medicine Reminder System** hosted live on **Vercel** (`https://2130537-s6.vercel.app`) and connected to **Supabase PostgreSQL 17** (`gieeovsmjagdalzblnos` in Oceania Sydney).

---

## 2. Issues Identified & Resolved
1. **Serverless Ephemeral Database Fallback**:
   - *Problem*: In serverless environments, missing environment variables caused fallback to `/tmp/medicines.db`, which lacked schema tables on cold boot and threw `500 Internal Server Error`.
   - *Resolution*: Implemented `DEFAULT_SUPABASE_URL` automatic fallback in `backend/database.py`, directly routing to the active Supabase connection pooler.
2. **Connection Pooling & Socket Freezing**:
   - *Problem*: Standard connection pools (`pool_size=5`) left open sockets that froze when AWS Lambda microVMs suspended.
   - *Resolution*: Configured SQLAlchemy with `NullPool` for serverless environments (`VERCEL=1`), opening connections on-demand and closing immediately upon request completion.
3. **Vercel Monorepo Architecture**:
   - *Problem*: Modifying `vercel.json` from the native `services` schema to custom build commands triggered deployment rejections.
   - *Resolution*: Restored native services monorepo configuration in `vercel.json` routing `/api/(.*)` to the FastAPI backend and `/(.*)` to the Vite frontend.
4. **Demo Account Authentication**:
   - *Resolution*: Pre-seeded and verified all 3 demo accounts in Supabase (`admin@example.com`, `vatista@example.com`, `patient@example.com`), and enabled 1-click instant login in `frontend/src/pages/AuthPage.tsx`.

---

## 3. Database Architecture & Tables
- **Database Engine**: PostgreSQL 17.12 (Sydney `ap-southeast-2`)
- **Connection Host**: `aws-0-ap-southeast-2.pooler.supabase.com:5432 / 6543`
- **Tables Verified**:
  - `users`: User identity, hashed passwords, roles (`super_admin`, `admin`, `patient`), and main admin flags.
  - `user_sessions`: SHA-256 hashed refresh tokens, session revocation flags, and expiry dates.
  - `medicines`: Medication schedules with `user_id` foreign key for complete multi-tenant privacy.
  - `dose_logs`: Daily dosage compliance logs (`taken` or `skipped`).

---

## 4. Test & Verification Audit
All 4 automated test suites executed with 100% pass rate:
- `backend/test_auth.py` -> 100% Passed
- `backend/test_rbac.py` -> 100% Passed
- `backend/test_crud.py` -> 100% Passed
- `backend/test_doses.py` -> 100% Passed

Live production endpoints on `https://2130537-s6.vercel.app`:
- `GET /api/health` -> 200 OK
- `POST /api/auth/login` (Admin, Vatista, Patient) -> 200 OK
- `GET /api/medicines` -> 200 OK
- `GET /api/admin/stats` -> 200 OK

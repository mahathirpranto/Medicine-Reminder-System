# Medicine Reminder System 💊

**CSE309 – Mid Project Assessment: MVP**  
A full-stack web application designed to help individuals track their daily medicine schedules, manage dosages, and set reminders. Built with **React + TypeScript (Vite)** on the frontend and **FastAPI + Python (SQLAlchemy/Supabase/SQLite)** on the backend.

---

## 1. Technology Stack

| Component | Technology | Description |
|---|---|---|
| **Frontend** | React 19 + TypeScript + Vite | Interactive UI, dynamic state management, Lucide icons |
| **Backend** | Python 3.12 + FastAPI | High-performance RESTful API with Pydantic validation |
| **Database** | SQLite (Local) / Supabase (PostgreSQL) | SQLAlchemy ORM with automatic table creation & seeding |
| **API Testing** | Postman & Swagger Docs | Complete CRUD testing suite & interactive `/docs` UI |
| **Deployment** | Vercel | Monorepo deployment with rewrites to FastAPI backend |
| **Version Control** | Git + GitHub | Clean feature branches and commits |

---

## 2. Database Design

**Table: `medicines`**

| Field Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for each medicine |
| `medicine_name` | String | Not Null, Indexed | Name of the medicine (e.g. Paracetamol) |
| `dosage` | String | Not Null | Dosage quantity (e.g. 500 mg, 1 tablet) |
| `frequency` | String | Not Null | Intake frequency (e.g. Twice daily) |
| `reminder_time` | String | Not Null | Scheduled time (e.g. 08:00 AM, 08:00 PM) |
| `start_date` | String | Not Null | Treatment start date (YYYY-MM-DD) |
| `end_date` | String | Not Null | Treatment end date (YYYY-MM-DD) |
| `status` | Boolean | Default: True, Not Null | Active schedule status (`true`/`false`) |

---

## 3. REST API Endpoints

The FastAPI backend exposes the following endpoints (available at both `/medicines` and `/api/medicines`):

| # | Operation | HTTP Method | Endpoint | Request Body | Success Status | Description |
|---|---|---|---|---|---|---|
| 1 | **Create** | `POST` | `/medicines` | JSON (all fields) | `201 Created` | Add a new medicine record |
| 2 | **Read List** | `GET` | `/medicines` | *None* (optional `search`, `status`) | `200 OK` | Get all medicine records |
| 3 | **Read Single**| `GET` | `/medicines/{id}` | *None* | `200 OK` | Get a specific medicine by ID |
| 4 | **Update** | `PUT` | `/medicines/{id}` | JSON (any fields) | `200 OK` | Edit an existing medicine by ID |
| 5 | **Delete** | `DELETE`| `/medicines/{id}` | *None* | `200 OK` | Permanently remove medicine by ID |

Interactive Swagger documentation is available at **http://localhost:8000/docs**.

---

## 4. Project Structure

```text
Medicine-Reminder-System/
│
├── frontend/                               # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── MedicineForm.tsx            # Add/Edit Medicine modal form
│   │   │   ├── MedicineList.tsx            # Search, filter, and card grid
│   │   │   └── MedicineCard.tsx            # Single card view with actions
│   │   ├── pages/
│   │   │   └── Dashboard.tsx               # Main dashboard with stats banner
│   │   ├── services/
│   │   │   └── medicineApi.ts              # API service for all 5 CRUD operations
│   │   ├── App.tsx                         # App entry component
│   │   ├── main.tsx                        # DOM mount point
│   │   └── index.css                       # Modern, clean medical UI styles
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts                      # Proxies /api to http://localhost:8000
│
├── backend/                                # FastAPI Backend
│   ├── .venv/                              # Python virtual environment
│   ├── database.py                         # SQLAlchemy engine & SQLite/Supabase setup
│   ├── models.py                           # SQLAlchemy Medicine table model
│   ├── schemas.py                          # Pydantic schemas for request/response
│   ├── main.py                             # FastAPI routes & CORS configuration
│   ├── test_crud.py                        # Automated Python tests for all CRUD routes
│   └── requirements.txt                    # Python dependencies
│
├── Medicine_Reminder_API.postman_collection.json  # Ready-to-import Postman collection
├── vercel.json                             # Vercel deployment configuration
└── README.md                               # Project documentation & viva guide
```

---

## 5. Quick Start (Running Locally)

### Prerequisites
- Python 3.10+
- Node.js 20+ and npm

### Terminal 1: Start Backend (FastAPI)
```powershell
cd backend
# If .venv is not yet activated:
.venv\Scripts\activate      # On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py         # Or: uvicorn main:app --reload --port 8000
```
Backend runs at: **http://localhost:8000**  
Swagger API Docs: **http://localhost:8000/docs**

### Terminal 2: Start Frontend (React + Vite)
```powershell
cd frontend
npm install
npm run dev
```
Frontend runs at: **http://localhost:5173**

---

## 6. How to Test with Postman

1. Open **Postman**.
2. Click **Import** and select `Medicine_Reminder_API.postman_collection.json` from the project root.
3. The collection includes all 5 pre-configured requests:
   - `GET {{base_url}}/health`
   - `POST {{base_url}}/medicines` (Create)
   - `GET {{base_url}}/medicines` (Read List)
   - `GET {{base_url}}/medicines/1` (Read Single)
   - `PUT {{base_url}}/medicines/1` (Update)
   - `DELETE {{base_url}}/medicines/1` (Delete)
4. Default variable `{{base_url}}` is set to `http://localhost:8000`.

---

## 7. Viva & Demonstration Guide

During your CSE309 assessment, be ready to demonstrate the following:

### 1. Demonstrate All 5 CRUD Operations in the Frontend
- **Create:** Click "+ Add Medicine", fill in medicine name, dosage, frequency, reminder time, dates, and click Save.
- **Read List:** Point out the medicine cards displayed on the dashboard, the real-time search box, and the status filter tabs (All, Active, Inactive).
- **Read Single:** Click the **Details** button on any card to open the single medicine inspection modal displaying all 8 database fields.
- **Update:** Click the **Edit** button to update fields (e.g. change dosage or frequency), or click the active/inactive status pill to quick-toggle.
- **Delete:** Click the **Delete** button, confirm the modal prompt, and show that the card is removed from both the UI and database.

### 2. Explain the Network Flow in Browser DevTools
- Press `F12` and switch to the **Network** tab.
- Perform a CRUD action (e.g. click "Details" to trigger `GET /api/medicines/{id}` or add a medicine to trigger `POST /api/medicines`).
- Show the HTTP method, request URL, payload JSON, response code (`200 OK` or `201 Created`), and the returned JSON.

### 3. Explain the Backend Architecture
- **`models.py`:** Defines the `Medicine` SQLAlchemy model mapped to the `medicines` table with data types and primary key.
- **`schemas.py`:** Pydantic validation schemas (`MedicineCreate`, `MedicineUpdate`, `MedicineResponse`).
- **`database.py`:** Database connection handling SQLite by default or Supabase/PostgreSQL via `DATABASE_URL`.
- **`main.py`:** FastAPI endpoint handlers using dependency injection (`db: Session = Depends(get_db)`).

---

## 8. Automated Testing

You can run the built-in test suite to verify all backend CRUD operations at any time:
```powershell
python backend/test_crud.py
```
Expected output:
```text
Initial medicines count: 3
Created medicine ID: 4, name: Ibuprofen
GET /medicines/{id} passed!
PUT /medicines/{id} passed!
DELETE /medicines/{id} passed!
404 on deleted item passed!
/api/medicines passed!
ALL 5 CRUD API TESTS PASSED PERFECTLY!
```

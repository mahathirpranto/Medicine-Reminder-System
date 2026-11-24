"""
Automated Test Suite for Role-Based Access Control (RBAC)
Tests:
1. Patient Forbidden from Admin Endpoints (403)
2. Vatista (Secondary Admin) can perform administrative tasks (Stats, User list, Patient management)
3. Vatista CANNOT modify, demote, or delete the Main System Administrator (403 Forbidden)
4. System Administrator has supreme access as Main Admin
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from database import init_db

# Initialize tables and seed admin user & Vatista
init_db()


def run_rbac_tests():
    with TestClient(app) as client:
        print("=== 1. VERIFY UNAUTHENTICATED ACCESS TO ADMIN ENDPOINT IS REJECTED (401) ===")
        unauth_res = client.get("/api/admin/stats")
        assert unauth_res.status_code == 401, f"Expected 401 Unauthorized, got {unauth_res.status_code}: {unauth_res.text}"
        print("PASS: Unauthenticated access rejected with 401 Unauthorized.")

        print("\n=== 2. REGISTER / LOGIN AS REGULAR PATIENT USER ===")
        patient_email = "test_patient_rbac@example.com"
        patient_pwd = "PatientPassword123!"

        reg_res = client.post(
            "/api/auth/signup",
            json={
                "email": patient_email,
                "password": patient_pwd,
                "full_name": "Test Patient",
            },
        )
        if reg_res.status_code == 400:
            login_res = client.post(
                "/api/auth/login",
                json={"email": patient_email, "password": patient_pwd},
            )
            assert login_res.status_code == 200, f"Login failed: {login_res.text}"
            patient_auth = login_res.json()
        else:
            assert reg_res.status_code == 201, f"Signup failed: {reg_res.text}"
            patient_auth = reg_res.json()

        patient_token = patient_auth["access_token"]
        patient_role = patient_auth["user"].get("role")
        patient_id = patient_auth["user"].get("id")
        assert patient_role == "patient", f"Expected default role 'patient', got '{patient_role}'"
        print(f"PASS: Patient registered/logged in with role '{patient_role}'.")

        patient_headers = {"Authorization": f"Bearer {patient_token}"}

        print("\n=== 3. VERIFY PATIENT IS FORBIDDEN (403) FROM ADMIN ENDPOINTS ===")
        p_stats_res = client.get("/api/admin/stats", headers=patient_headers)
        assert p_stats_res.status_code == 403, f"Expected 403 Forbidden for patient, got {p_stats_res.status_code}: {p_stats_res.text}"
        print(f"PASS: Patient accessing /api/admin/stats correctly returned 403 Forbidden.")

        p_users_res = client.get("/api/admin/users", headers=patient_headers)
        assert p_users_res.status_code == 403, f"Expected 403 Forbidden for patient, got {p_users_res.status_code}: {p_users_res.text}"
        print(f"PASS: Patient accessing /api/admin/users correctly returned 403 Forbidden.")

        print("\n=== 4. LOGIN AS VATISTA (SECONDARY ADMIN) ===")
        vatista_login_res = client.post(
            "/api/auth/login",
            json={"email": "vatista@example.com", "password": "VatistaPassword123!"},
        )
        assert vatista_login_res.status_code == 200, f"Vatista login failed: {vatista_login_res.text}"
        vatista_auth = vatista_login_res.json()
        vatista_token = vatista_auth["access_token"]
        vatista_role = vatista_auth["user"].get("role")
        vatista_is_main = vatista_auth["user"].get("is_main_admin")
        assert vatista_role == "admin", f"Expected Vatista role 'admin', got '{vatista_role}'"
        assert vatista_is_main is False, f"Expected Vatista is_main_admin=False, got {vatista_is_main}"
        vatista_headers = {"Authorization": f"Bearer {vatista_token}"}
        print(f"PASS: Vatista logged in as secondary Admin (role: '{vatista_role}', is_main_admin: False).")

        print("\n=== 5. VERIFY VATISTA CAN DO ADMIN ACTIONS (STATS & USERS LIST) ===")
        v_stats_res = client.get("/api/admin/stats", headers=vatista_headers)
        assert v_stats_res.status_code == 200, f"Expected 200 OK for Vatista stats, got {v_stats_res.status_code}: {v_stats_res.text}"
        stats_data = v_stats_res.json()
        print(f"PASS: Vatista successfully retrieved system stats: {stats_data}")

        v_users_res = client.get("/api/admin/users", headers=vatista_headers)
        assert v_users_res.status_code == 200, f"Expected 200 OK for Vatista users list, got {v_users_res.status_code}: {v_users_res.text}"
        users_list = v_users_res.json()
        print(f"PASS: Vatista successfully retrieved user directory ({len(users_list)} users).")

        # Locate Main System Administrator in user list
        sys_admin = next((u for u in users_list if u["email"] == "admin@example.com"), None)
        assert sys_admin is not None, "System Administrator must exist in user list"
        sys_admin_id = sys_admin["id"]
        assert sys_admin["is_main_admin"] is True, "System Administrator must have is_main_admin=True"

        print("\n=== 6. VERIFY VATISTA CANNOT DO ANYTHING TO SYSTEM ADMINISTRATOR (403) ===")
        # 6a. Vatista attempts to demote System Administrator
        v_demote_res = client.put(
            f"/api/admin/users/{sys_admin_id}/role",
            headers=vatista_headers,
            json={"role": "patient"},
        )
        assert v_demote_res.status_code == 403, f"Expected 403 Forbidden when Vatista attempts to demote Main Admin, got {v_demote_res.status_code}: {v_demote_res.text}"
        print(f"PASS: Vatista blocked from modifying System Administrator role (403): {v_demote_res.json().get('detail')}")

        # 6b. Vatista attempts to delete System Administrator
        v_del_res = client.delete(
            f"/api/admin/users/{sys_admin_id}",
            headers=vatista_headers,
        )
        assert v_del_res.status_code == 403, f"Expected 403 Forbidden when Vatista attempts to delete Main Admin, got {v_del_res.status_code}: {v_del_res.text}"
        print(f"PASS: Vatista blocked from deleting System Administrator (403): {v_del_res.json().get('detail')}")

        print("\n=== 7. LOGIN AS SYSTEM ADMINISTRATOR (MAIN ADMIN) ===")
        admin_login_res = client.post(
            "/api/auth/login",
            json={"email": "admin@example.com", "password": "AdminPassword123!"},
        )
        assert admin_login_res.status_code == 200, f"Admin login failed: {admin_login_res.text}"
        admin_auth = admin_login_res.json()
        assert admin_auth["user"].get("is_main_admin") is True, "System Administrator must be is_main_admin=True"
        admin_token = admin_auth["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print(f"PASS: Main System Administrator logged in with full super-admin authority.")

        print("\n=== 8. VERIFY SYSTEM ADMINISTRATOR CAN MANAGE PATIENT ROLES ===")
        # Main Admin updates patient role
        p_update_res = client.put(
            f"/api/admin/users/{patient_id}/role",
            headers=admin_headers,
            json={"role": "patient"},
        )
        assert p_update_res.status_code == 200, f"Expected 200 OK, got {p_update_res.status_code}: {p_update_res.text}"
        print(f"PASS: Main Admin updated patient role successfully: {p_update_res.json().get('message')}")

        print("\n=== 9. VERIFY ONLY MAIN ADMIN CAN DELETE USERS (VATISTA 403 vs MAIN ADMIN 200) ===")
        # Register a temporary user to test deletion
        temp_email = "temp_user_for_delete_test@example.com"
        temp_signup = client.post(
            "/api/auth/signup",
            json={"email": temp_email, "password": "Password123!", "full_name": "Temporary User"},
        )
        if temp_signup.status_code == 201:
            temp_user_id = temp_signup.json()["user"]["id"]
        else:
            # Login to get id
            temp_login = client.post("/api/auth/login", json={"email": temp_email, "password": "Password123!"})
            temp_user_id = temp_login.json()["user"]["id"]

        # 9a. Vatista attempts to delete the temporary user -> MUST FAIL WITH 403 FORBIDDEN
        v_del_patient = client.delete(f"/api/admin/users/{temp_user_id}", headers=vatista_headers)
        assert v_del_patient.status_code == 403, f"Expected 403 Forbidden when Vatista attempts to delete a user, got {v_del_patient.status_code}: {v_del_patient.text}"
        print(f"PASS: Vatista blocked from deleting user (403): {v_del_patient.json().get('detail')}")

        # 9b. Main System Administrator deletes the temporary user -> MUST SUCCEED (200 OK)
        admin_del_res = client.delete(f"/api/admin/users/{temp_user_id}", headers=admin_headers)
        assert admin_del_res.status_code == 200, f"Expected 200 OK when Main Admin deletes user, got {admin_del_res.status_code}: {admin_del_res.text}"
        print(f"PASS: Main System Administrator successfully deleted user account: {admin_del_res.json().get('message')}")

        # 9c. Main System Administrator attempts to delete self -> MUST BE PREVENTED (400 BAD REQUEST)
        admin_self_del = client.delete(f"/api/admin/users/{sys_admin_id}", headers=admin_headers)
        assert admin_self_del.status_code in (400, 403), f"Expected 400 or 403 preventing self-deletion, got {admin_self_del.status_code}"
        print(f"PASS: Main System Administrator self-deletion prevented: {admin_self_del.json().get('detail')}")

        print("\n===========================================================================")
        print("ALL HIERARCHICAL RBAC TESTS PASSED SUCCESSFULLY!")
        print("User deletion is exclusively granted to Main System Administrator!")
        print("===========================================================================")


if __name__ == "__main__":
    run_rbac_tests()

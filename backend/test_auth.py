import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from database import init_db

# Initialize tables
init_db()


def run_auth_and_isolation_tests():
    with TestClient(app) as client:
        print("=== 1. TEST USER REGISTRATION (/api/auth/signup) ===")
        user_a_email = "testuser_a@example.com"
        res = client.post(
            "/api/auth/signup",
            json={
                "email": user_a_email,
                "password": "Password123!",
                "full_name": "Test User A",
            },
        )
        # If already registered from previous run, that's fine, let's login
        if res.status_code == 400:
            print("User A already exists, proceeding to login...")
            login_res = client.post(
                "/api/auth/login",
                json={"email": user_a_email, "password": "Password123!"},
            )
            assert login_res.status_code == 200, f"Login failed: {login_res.text}"
            auth_data_a = login_res.json()
        else:
            assert res.status_code == 201, f"Signup failed: {res.text}"
            auth_data_a = res.json()

        access_token_a = auth_data_a["access_token"]
        refresh_token_a = auth_data_a["refresh_token"]
        user_a_id = auth_data_a["user"]["id"]
        headers_a = {"Authorization": f"Bearer {access_token_a}"}
        print(f"User A registered/logged in with ID {user_a_id}!")

        # 2. Test duplicate email rejection
        dup_res = client.post(
            "/api/auth/signup",
            json={
                "email": user_a_email,
                "password": "Password123!",
                "full_name": "Duplicate User",
            },
        )
        assert dup_res.status_code == 400
        print("Duplicate signup rejected with 400 OK!")

        # 3. Test wrong password rejection
        wrong_pwd = client.post(
            "/api/auth/login",
            json={"email": user_a_email, "password": "WrongPassword!"},
        )
        assert wrong_pwd.status_code == 401
        print("Wrong password rejected with 401 OK!")

        # 4. Test GET /api/users/me
        me_res = client.get("/api/users/me", headers=headers_a)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == user_a_email
        print(f"GET /api/users/me passed for {me_res.json()['full_name']}!")

        # 5. Test Refresh Token session (/api/auth/refresh)
        refresh_res = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token_a},
        )
        assert refresh_res.status_code == 200
        new_access_token = refresh_res.json()["access_token"]
        assert new_access_token != ""
        print("POST /api/auth/refresh issued new access token OK!")

        # 6. Test User-Isolated Medicines for User A
        print("\n=== 2. TEST USER DATA ISOLATION (PART 3) ===")
        med_res_a = client.post(
            "/api/medicines",
            headers=headers_a,
            json={
                "medicine_name": "User A Private Medicine",
                "dosage": "50 mg",
                "frequency": "Once daily",
                "reminder_time": "10:00 AM",
                "start_date": "2026-11-20",
                "end_date": "2026-11-30",
                "status": True,
            },
        )
        assert med_res_a.status_code == 201, f"Create med failed: {med_res_a.text}"
        med_a_id = med_res_a.json()["id"]
        print(f"User A created private medicine with ID {med_a_id}")

        # 7. Register User B
        import time
        unique_b = int(time.time())
        res_b = client.post(
            "/api/auth/signup",
            json={
                "email": f"user_b_{unique_b}@example.com",
                "password": "Password123!",
                "full_name": "Test User B",
            },
        )
        assert res_b.status_code == 201
        headers_b = {"Authorization": f"Bearer {res_b.json()['access_token']}"}

        # User B queries medicines - should NOT see User A's private medicine!
        list_b = client.get("/api/medicines", headers=headers_b)
        assert list_b.status_code == 200
        med_ids_b = [m["id"] for m in list_b.json()]
        assert med_a_id not in med_ids_b, "SECURITY BREACH: User B saw User A's medicine!"
        print("Data Isolation Verified: User B cannot see User A's medicine!")

        # User B attempts to GET User A's medicine by ID - should return 404
        sneak_res = client.get(f"/api/medicines/{med_a_id}", headers=headers_b)
        assert sneak_res.status_code == 404
        print("Security Verified: User B cannot fetch User A's medicine by ID (404 Not Found)!")

        # 8. Test Session Revocation & Logout
        print("\n=== 3. TEST LOGOUT & SESSION REVOCATION ===")
        logout_res = client.post(
            "/api/auth/logout",
            json={"refresh_token": refresh_token_a},
        )
        assert logout_res.status_code == 200
        print("POST /api/auth/logout succeeded!")

        # Attempt to reuse revoked refresh token
        reuse_res = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token_a},
        )
        assert reuse_res.status_code == 401
        assert "revoked" in reuse_res.json()["detail"].lower()
        print("Revoked token reuse successfully blocked with 401 Unauthorized!")

        print("\nALL AUTH & USER ISOLATION TESTS PASSED 100%!")


if __name__ == "__main__":
    run_auth_and_isolation_tests()

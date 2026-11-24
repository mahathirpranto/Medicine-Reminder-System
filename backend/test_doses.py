import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from database import init_db

init_db()


def run_dose_tracking_tests():
    with TestClient(app) as client:
        # Register/login user
        email = "dose_tester@example.com"
        pwd = "Password123!"
        res = client.post(
            "/api/auth/signup",
            json={"email": email, "password": pwd, "full_name": "Dose Tracker"},
        )
        if res.status_code == 400:
            res = client.post("/api/auth/login", json={"email": email, "password": pwd})
        assert res.status_code in (200, 201)
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create a medicine for today
        med_res = client.post(
            "/api/medicines",
            headers=headers,
            json={
                "medicine_name": "Metformin",
                "dosage": "500 mg",
                "frequency": "Twice daily",
                "reminder_time": "09:00 AM, 09:00 PM",
                "start_date": "2026-11-01",
                "end_date": "2026-12-31",
                "status": True,
            },
        )
        assert med_res.status_code == 201
        med_id = med_res.json()["id"]
        print(f"Created test medicine for dose tracking: ID {med_id}")

        # 2. Get today's schedule
        sched_res = client.get("/api/medicines/schedule/today", headers=headers)
        assert sched_res.status_code == 200
        sched_items = sched_res.json()
        print(f"Today's scheduled medicines count: {len(sched_items)}")
        target_item = next((i for i in sched_items if i["medicine_id"] == med_id), None)
        assert target_item is not None
        assert "09:00 AM" in target_item["scheduled_times"]
        assert target_item["is_fully_taken"] is False

        # 3. Log morning dose as taken
        take_res = client.post(
            f"/api/medicines/{med_id}/doses",
            headers=headers,
            json={"dose_time": "09:00 AM", "status": "taken", "notes": "Taken with breakfast"},
        )
        assert take_res.status_code == 201
        log_data = take_res.json()
        assert log_data["medicine_id"] == med_id
        assert log_data["status"] == "taken"
        print(f"Dose logged successfully! Dose ID {log_data['id']}, medicine: {log_data['medicine_name']}")

        # 4. Verify today's schedule now lists 09:00 AM in taken_times
        sched_res2 = client.get("/api/medicines/schedule/today", headers=headers)
        assert sched_res2.status_code == 200
        target_item2 = next(i for i in sched_res2.json() if i["medicine_id"] == med_id)
        assert "09:00 AM" in target_item2["taken_times"]
        print("Today's schedule successfully updated with taken dose!")

        # 5. Check medicine dose history
        history_res = client.get(f"/api/medicines/{med_id}/doses", headers=headers)
        assert history_res.status_code == 200
        assert len(history_res.json()) >= 1
        print("Medicine specific dose history verified!")

        # 6. Check global dose history
        global_history = client.get("/api/medicines/doses/history", headers=headers)
        assert global_history.status_code == 200
        assert len(global_history.json()) >= 1
        print("Global dose history verified!")

        print("\nALL DOSE TRACKING & SCHEDULE TESTS PASSED 100%!")


if __name__ == "__main__":
    run_dose_tracking_tests()

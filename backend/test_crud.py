import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient

try:
    from main import app
    from database import init_db
except ImportError:
    from backend.main import app
    from backend.database import init_db

# Ensure tables and initial seed data exist
init_db()

def test_crud_flow():
    with TestClient(app) as client:
        # 1. Test GET list
        res = client.get('/medicines')
        assert res.status_code == 200, f'GET /medicines failed: {res.text}'
        data = res.json()
        print(f'Initial medicines count: {len(data)}')

        # 2. Test POST create
        new_med = {
            'medicine_name': 'Ibuprofen',
            'dosage': '400 mg',
            'frequency': 'Every 8 hours',
            'reminder_time': '02:00 PM, 10:00 PM',
            'start_date': '2026-11-04',
            'end_date': '2026-11-10',
            'status': True
        }
        res = client.post('/medicines', json=new_med)
        assert res.status_code == 201, f'POST /medicines failed: {res.text}'
        created = res.json()
        med_id = created['id']
        print(f"Created medicine ID: {med_id}, name: {created['medicine_name']}")

        # 3. Test GET single
        res = client.get(f'/medicines/{med_id}')
        assert res.status_code == 200
        assert res.json()['medicine_name'] == 'Ibuprofen'
        print('GET /medicines/{id} passed!')

        # 4. Test PUT update
        res = client.put(f'/medicines/{med_id}', json={'dosage': '600 mg', 'status': False})
        assert res.status_code == 200
        assert res.json()['dosage'] == '600 mg'
        assert res.json()['status'] is False
        print('PUT /medicines/{id} passed!')

        # 5. Test DELETE
        res = client.delete(f'/medicines/{med_id}')
        assert res.status_code == 200
        print('DELETE /medicines/{id} passed!')

        # 6. Verify 404 after delete
        res = client.get(f'/medicines/{med_id}')
        assert res.status_code == 404
        print('404 on deleted item passed!')

        # Also test /api prefix
        res = client.get('/api/medicines')
        assert res.status_code == 200
        print('/api/medicines passed!')

        print('ALL 5 CRUD API TESTS PASSED PERFECTLY!')

if __name__ == '__main__':
    test_crud_flow()

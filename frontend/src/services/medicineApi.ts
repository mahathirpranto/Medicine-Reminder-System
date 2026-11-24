/**
 * Medicine Reminder System - API Service
 * Handles all 5 CRUD operations communicating with the FastAPI backend,
 * automatically authenticated via Bearer JWT with silent refresh retry,
 * plus Dose Tracking and Schedule Endpoints (Part 5).
 */

import type {
  Medicine,
  MedicineCreateInput,
  MedicineUpdateInput,
  DoseLog,
  DoseLogCreateInput,
  TodayScheduleItem,
} from '../types/medicine';
import { authenticatedFetch } from './authApi';

export type {
  Medicine,
  MedicineCreateInput,
  MedicineUpdateInput,
  DoseLog,
  DoseLogCreateInput,
  TodayScheduleItem,
};

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * 1. CREATE - Add a new medicine
 * POST /api/medicines
 */
export async function createMedicine(data: MedicineCreateInput): Promise<Medicine> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to create medicine (${response.status})`);
  }

  return response.json();
}

/**
 * 2. READ LIST - Get all medicines
 * GET /api/medicines
 */
export async function getMedicines(params?: { search?: string; status?: boolean }): Promise<Medicine[]> {
  const query = new URLSearchParams();
  if (params?.search) {
    query.set('search', params.search);
  }
  if (params?.status !== undefined) {
    query.set('status', String(params.status));
  }

  const url = query.toString() ? `${BASE_URL}/medicines?${query}` : `${BASE_URL}/medicines`;
  const response = await authenticatedFetch(url, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch medicines (${response.status})`);
  }

  return response.json();
}

/**
 * 3. READ SINGLE - Get one medicine by ID
 * GET /api/medicines/{id}
 */
export async function getMedicineById(id: number): Promise<Medicine> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/${id}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch medicine with ID ${id} (${response.status})`);
  }

  return response.json();
}

/**
 * 4. UPDATE - Edit medicine by ID
 * PUT /api/medicines/{id}
 */
export async function updateMedicine(id: number, data: MedicineUpdateInput): Promise<Medicine> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update medicine with ID ${id} (${response.status})`);
  }

  return response.json();
}

/**
 * 5. DELETE - Remove medicine by ID
 * DELETE /api/medicines/{id}
 */
export async function deleteMedicine(id: number): Promise<{ message: string; id: number }> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/${id}`, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to delete medicine with ID ${id} (${response.status})`);
  }

  return response.json();
}

// ==========================================
// Dose Tracking & Schedule API (Part 5)
// ==========================================

/**
 * 6. LOG DOSE - Mark medicine dose as taken or skipped
 * POST /api/medicines/{id}/doses
 */
export async function logMedicineDose(
  medicineId: number,
  data?: DoseLogCreateInput
): Promise<DoseLog> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/${medicineId}/doses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(data || { status: 'taken' }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to record dose (${response.status})`);
  }

  return response.json();
}

/**
 * 7. GET TODAY'S SCHEDULE
 * GET /api/medicines/schedule/today
 */
export async function getTodaySchedule(): Promise<TodayScheduleItem[]> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/schedule/today`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to load today's schedule (${response.status})`);
  }

  return response.json();
}

/**
 * 8. GET MEDICINE DOSE HISTORY
 * GET /api/medicines/{id}/doses
 */
export async function getMedicineDoseHistory(medicineId: number): Promise<DoseLog[]> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/${medicineId}/doses`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch dose history (${response.status})`);
  }

  return response.json();
}

/**
 * 9. GET USER GLOBAL DOSE HISTORY
 * GET /api/medicines/doses/history
 */
export async function getUserDoseHistory(limit: number = 30): Promise<DoseLog[]> {
  const response = await authenticatedFetch(`${BASE_URL}/medicines/doses/history?limit=${limit}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch global dose history (${response.status})`);
  }

  return response.json();
}

/**
 * Medicine Reminder System - API Service
 * Handles all 5 CRUD operations communicating with the FastAPI backend.
 */

export interface Medicine {
  id: number;
  medicine_name: string;
  dosage: string;
  frequency: string;
  reminder_time: string;
  start_date: string;
  end_date: string;
  status: boolean;
}

export type MedicineCreateInput = Omit<Medicine, 'id'>;
export type MedicineUpdateInput = Partial<MedicineCreateInput>;

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * 1. CREATE - Add a new medicine
 * POST /api/medicines
 */
export async function createMedicine(data: MedicineCreateInput): Promise<Medicine> {
  const response = await fetch(`${BASE_URL}/medicines`, {
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
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch medicines (${response.status})`);
  }

  return response.json();
}

/**
 * 3. READ SINGLE - Get one medicine by ID
 * GET /api/medicines/{id}
 */
export async function getMedicineById(id: number): Promise<Medicine> {
  const response = await fetch(`${BASE_URL}/medicines/${id}`, {
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
  const response = await fetch(`${BASE_URL}/medicines/${id}`, {
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
  const response = await fetch(`${BASE_URL}/medicines/${id}`, {
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

/**
 * Medicine Reminder System - Type Definitions
 * Dedicated types module for medicine entity and form inputs.
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

/**
 * Medicine Reminder System - Type Definitions
 * Dedicated types module for medicine entity, dose tracking, and schedule inputs.
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
  user_id?: number;
}

export type MedicineCreateInput = Omit<Medicine, 'id'>;
export type MedicineUpdateInput = Partial<MedicineCreateInput>;

export interface DoseLog {
  id: number;
  medicine_id: number;
  user_id: number;
  dose_time: string;
  taken_at: string;
  status: 'taken' | 'skipped' | 'missed';
  notes?: string | null;
  medicine_name?: string | null;
}

export interface DoseLogCreateInput {
  dose_time?: string;
  status?: 'taken' | 'skipped' | 'missed';
  notes?: string;
}

export interface TodayScheduleItem {
  medicine_id: number;
  medicine_name: string;
  dosage: string;
  frequency: string;
  scheduled_times: string[];
  taken_times: string[];
  is_fully_taken: boolean;
  status: boolean;
}

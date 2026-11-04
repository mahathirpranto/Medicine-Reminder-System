import React, { useState, useEffect } from 'react';
import { X, Plus, Save, AlertCircle } from 'lucide-react';
import type { Medicine, MedicineCreateInput } from '../services/medicineApi';

interface MedicineFormProps {
  initialData?: Medicine | null;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: MedicineCreateInput) => Promise<void>;
}

export const MedicineForm: React.FC<MedicineFormProps> = ({
  initialData,
  isOpen,
  onClose,
  onSubmit,
}) => {
  const getTodayDate = () => new Date().toISOString().split('T')[0];
  const getDefaultEndDate = () => {
    const d = new Date();
    d.setDate(d.getDate() + 7);
    return d.toISOString().split('T')[0];
  };

  const [formData, setFormData] = useState<MedicineCreateInput>({
    medicine_name: '',
    dosage: '',
    frequency: 'Once daily',
    reminder_time: '08:00 AM',
    start_date: getTodayDate(),
    end_date: getDefaultEndDate(),
    status: true,
  });

  const [error, setError] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        medicine_name: initialData.medicine_name,
        dosage: initialData.dosage,
        frequency: initialData.frequency,
        reminder_time: initialData.reminder_time,
        start_date: initialData.start_date,
        end_date: initialData.end_date,
        status: initialData.status,
      });
    } else {
      setFormData({
        medicine_name: '',
        dosage: '',
        frequency: 'Once daily',
        reminder_time: '08:00 AM',
        start_date: getTodayDate(),
        end_date: getDefaultEndDate(),
        status: true,
      });
    }
    setError('');
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!formData.medicine_name.trim()) {
      setError('Medicine name is required.');
      return;
    }
    if (!formData.dosage.trim()) {
      setError('Dosage is required (e.g. 500 mg).');
      return;
    }
    if (!formData.reminder_time.trim()) {
      setError('Reminder time is required.');
      return;
    }
    if (!formData.start_date || !formData.end_date) {
      setError('Both start and end dates are required.');
      return;
    }

    try {
      setSubmitting(true);
      await onSubmit(formData);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save medicine');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{initialData ? 'Edit Medicine' : 'Add New Medicine'}</h2>
          <button type="button" className="btn-close" onClick={onClose} aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        {error && (
          <div className="alert-box alert-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="medicine-form">
          <div className="form-grid">
            <div className="form-group full-width">
              <label htmlFor="medicine_name">
                Medicine Name <span className="req">*</span>
              </label>
              <input
                id="medicine_name"
                name="medicine_name"
                type="text"
                value={formData.medicine_name}
                onChange={handleChange}
                placeholder="e.g. Paracetamol, Amoxicillin"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="dosage">
                Dosage <span className="req">*</span>
              </label>
              <input
                id="dosage"
                name="dosage"
                type="text"
                value={formData.dosage}
                onChange={handleChange}
                placeholder="e.g. 500 mg, 1 tablet, 10 ml"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="frequency">
                Frequency <span className="req">*</span>
              </label>
              <select
                id="frequency"
                name="frequency"
                value={formData.frequency}
                onChange={handleChange}
                required
              >
                <option value="Once daily">Once daily</option>
                <option value="Twice daily">Twice daily</option>
                <option value="Three times daily">Three times daily</option>
                <option value="Every 4 hours">Every 4 hours</option>
                <option value="Every 6 hours">Every 6 hours</option>
                <option value="Every 8 hours">Every 8 hours</option>
                <option value="Every 12 hours">Every 12 hours</option>
                <option value="As needed">As needed</option>
              </select>
            </div>

            <div className="form-group full-width">
              <label htmlFor="reminder_time">
                Reminder Time <span className="req">*</span>
              </label>
              <input
                id="reminder_time"
                name="reminder_time"
                type="text"
                value={formData.reminder_time}
                onChange={handleChange}
                placeholder="e.g. 08:00 AM, 08:00 PM"
                required
              />
              <span className="form-hint">Tip: Enter specific daily times (e.g. "08:00 AM, 08:00 PM")</span>
            </div>

            <div className="form-group">
              <label htmlFor="start_date">
                Start Date <span className="req">*</span>
              </label>
              <input
                id="start_date"
                name="start_date"
                type="date"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_date">
                End Date <span className="req">*</span>
              </label>
              <input
                id="end_date"
                name="end_date"
                type="date"
                value={formData.end_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group full-width checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="status"
                  checked={formData.status}
                  onChange={handleChange}
                />
                <span className="checkbox-custom"></span>
                <span>Active Reminder (Enable scheduled alerts for this medicine)</span>
              </label>
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={submitting}>
              {submitting ? (
                <span>Saving...</span>
              ) : initialData ? (
                <>
                  <Save size={18} />
                  <span>Update Medicine</span>
                </>
              ) : (
                <>
                  <Plus size={18} />
                  <span>Add Medicine</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

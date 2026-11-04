import React, { useState, useEffect, useCallback } from 'react';
import {
  Pill,
  Plus,
  Activity,
  CheckCircle,
  Clock,
  Calendar,
  AlertTriangle,
  X,
  Trash2,
  Check,
} from 'lucide-react';
import {
  getMedicines,
  getMedicineById,
  createMedicine,
  updateMedicine,
  deleteMedicine,
  type Medicine,
  type MedicineCreateInput,
} from '../services/medicineApi';
import { MedicineList } from '../components/MedicineList';
import { MedicineForm } from '../components/MedicineForm';

interface ToastMessage {
  id: number;
  type: 'success' | 'error' | 'info';
  text: string;
}

export const Dashboard: React.FC = () => {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');

  // Modal States
  const [isFormOpen, setIsFormOpen] = useState<boolean>(false);
  const [editingMedicine, setEditingMedicine] = useState<Medicine | null>(null);

  // Single View Modal State (CRUD: Read Single)
  const [viewingMedicine, setViewingMedicine] = useState<Medicine | null>(null);
  const [viewLoading, setViewLoading] = useState<boolean>(false);

  // Delete Confirmation State (CRUD: Delete)
  const [deletingMedicine, setDeletingMedicine] = useState<Medicine | null>(null);
  const [deleteLoading, setDeleteLoading] = useState<boolean>(false);

  // Toast notification state
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (type: 'success' | 'error' | 'info', text: string) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, type, text }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // 1. Fetch all medicines (CRUD: Read List)
  const fetchMedicines = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getMedicines();
      setMedicines(data);
    } catch (err) {
      addToast('error', err instanceof Error ? err.message : 'Failed to fetch medicines');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMedicines();
  }, [fetchMedicines]);

  // 2. Fetch single medicine (CRUD: Read Single)
  const handleView = async (id: number) => {
    try {
      setViewLoading(true);
      const data = await getMedicineById(id);
      setViewingMedicine(data);
    } catch (err) {
      addToast('error', err instanceof Error ? err.message : 'Failed to fetch medicine details');
    } finally {
      setViewLoading(false);
    }
  };

  // 3. Handle Add / Edit Submission (CRUD: Create or Update)
  const handleFormSubmit = async (formData: MedicineCreateInput) => {
    if (editingMedicine) {
      // UPDATE operation
      const updated = await updateMedicine(editingMedicine.id, formData);
      setMedicines((prev) =>
        prev.map((med) => (med.id === updated.id ? updated : med))
      );
      addToast('success', `"${updated.medicine_name}" updated successfully!`);
    } else {
      // CREATE operation
      const created = await createMedicine(formData);
      setMedicines((prev) => [created, ...prev]);
      addToast('success', `"${created.medicine_name}" added to your schedule!`);
    }
  };

  // 4. Quick toggle status (CRUD: Update)
  const handleToggleStatus = async (medicine: Medicine) => {
    try {
      const updated = await updateMedicine(medicine.id, {
        status: !medicine.status,
      });
      setMedicines((prev) =>
        prev.map((med) => (med.id === updated.id ? updated : med))
      );
      addToast(
        'info',
        `"${updated.medicine_name}" marked as ${updated.status ? 'Active' : 'Inactive'}`
      );
    } catch (err) {
      addToast('error', 'Failed to toggle status');
    }
  };

  // 5. Delete operation (CRUD: Delete)
  const handleConfirmDelete = async () => {
    if (!deletingMedicine) return;
    try {
      setDeleteLoading(true);
      await deleteMedicine(deletingMedicine.id);
      setMedicines((prev) => prev.filter((med) => med.id !== deletingMedicine.id));
      addToast('success', `"${deletingMedicine.medicine_name}" was deleted successfully.`);
      setDeletingMedicine(null);
    } catch (err) {
      addToast('error', err instanceof Error ? err.message : 'Failed to delete medicine');
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleOpenAdd = () => {
    setEditingMedicine(null);
    setIsFormOpen(true);
  };

  const handleOpenEdit = (medicine: Medicine) => {
    setEditingMedicine(medicine);
    setIsFormOpen(true);
  };

  // Calculate statistics
  const totalCount = medicines.length;
  const activeCount = medicines.filter((m) => m.status).length;
  const inactiveCount = totalCount - activeCount;

  return (
    <div className="dashboard-wrapper">
      {/* Toast Notifications */}
      <div className="toast-container">
        {toasts.map((toast) => (
          <div key={toast.id} className={`toast toast-${toast.type}`}>
            {toast.type === 'success' && <Check size={18} />}
            {toast.type === 'error' && <AlertTriangle size={18} />}
            {toast.type === 'info' && <Pill size={18} />}
            <span>{toast.text}</span>
          </div>
        ))}
      </div>

      {/* Header */}
      <header className="app-header">
        <div className="header-container">
          <div className="header-brand">
            <div className="brand-logo">
              <Pill size={28} />
            </div>
            <div>
              <h1 className="brand-title">Medicine Reminder System</h1>
              <p className="brand-subtitle">
                Track and manage your daily medicine schedules
              </p>
            </div>
          </div>

          <div className="header-actions">
            <button
              type="button"
              className="btn-primary"
              onClick={handleOpenAdd}
            >
              <Plus size={18} />
              <span>Add Medicine</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-content">
        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card stat-total">
            <div className="stat-icon-wrapper">
              <Pill size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-value">{totalCount}</span>
              <span className="stat-label">Total Medicines</span>
            </div>
          </div>

          <div className="stat-card stat-active">
            <div className="stat-icon-wrapper">
              <Activity size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-value">{activeCount}</span>
              <span className="stat-label">Active Reminders</span>
            </div>
          </div>

          <div className="stat-card stat-today">
            <div className="stat-icon-wrapper">
              <Clock size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-value">
                {activeCount > 0 ? activeCount : 0}
              </span>
              <span className="stat-label">Today's Active Doses</span>
            </div>
          </div>

          <div className="stat-card stat-inactive">
            <div className="stat-icon-wrapper">
              <CheckCircle size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-value">{inactiveCount}</span>
              <span className="stat-label">Completed / Inactive</span>
            </div>
          </div>
        </div>

        {/* Medicine List Section */}
        <MedicineList
          medicines={medicines}
          loading={loading}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          statusFilter={statusFilter}
          onStatusFilterChange={setStatusFilter}
          onView={handleView}
          onEdit={handleOpenEdit}
          onDelete={setDeletingMedicine}
          onToggleStatus={handleToggleStatus}
          onAddNew={handleOpenAdd}
          onRefresh={fetchMedicines}
        />
      </main>

      {/* Form Modal: Add / Edit (CRUD: Create / Update) */}
      <MedicineForm
        isOpen={isFormOpen}
        initialData={editingMedicine}
        onClose={() => {
          setIsFormOpen(false);
          setEditingMedicine(null);
        }}
        onSubmit={handleFormSubmit}
      />

      {/* Single Medicine Details Modal (CRUD: Read Single) */}
      {viewingMedicine && (
        <div className="modal-overlay" onClick={() => setViewingMedicine(null)}>
          <div className="modal-container detail-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title-with-badge">
                <h2>Medicine Details</h2>
                <span className={`status-pill ${viewingMedicine.status ? 'pill-active' : 'pill-inactive'}`}>
                  {viewingMedicine.status ? 'Active Reminder' : 'Inactive'}
                </span>
              </div>
              <button
                type="button"
                className="btn-close"
                onClick={() => setViewingMedicine(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="detail-modal-body">
              <div className="detail-header-card">
                <div className="detail-icon-large">
                  <Pill size={32} />
                </div>
                <div>
                  <h3 className="detail-med-name">{viewingMedicine.medicine_name}</h3>
                  <p className="detail-med-sub">ID: #{viewingMedicine.id} &bull; {viewingMedicine.dosage}</p>
                </div>
              </div>

              <div className="detail-table">
                <div className="detail-row">
                  <span className="detail-label">Frequency:</span>
                  <span className="detail-val">{viewingMedicine.frequency}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Reminder Time:</span>
                  <span className="detail-val font-mono">{viewingMedicine.reminder_time}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Start Date:</span>
                  <span className="detail-val">{viewingMedicine.start_date}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">End Date:</span>
                  <span className="detail-val">{viewingMedicine.end_date}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Status:</span>
                  <span className="detail-val">
                    {viewingMedicine.status ? 'Active (Scheduled)' : 'Inactive (Paused)'}
                  </span>
                </div>
              </div>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setViewingMedicine(null)}
              >
                Close
              </button>
              <button
                type="button"
                className="btn-primary"
                onClick={() => {
                  const toEdit = viewingMedicine;
                  setViewingMedicine(null);
                  handleOpenEdit(toEdit);
                }}
              >
                Edit This Medicine
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal (CRUD: Delete) */}
      {deletingMedicine && (
        <div className="modal-overlay" onClick={() => setDeletingMedicine(null)}>
          <div className="modal-container delete-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Confirm Delete</h2>
              <button
                type="button"
                className="btn-close"
                onClick={() => setDeletingMedicine(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="delete-modal-body">
              <div className="delete-warn-icon">
                <AlertTriangle size={36} />
              </div>
              <p>
                Are you sure you want to delete{' '}
                <strong>"{deletingMedicine.medicine_name}"</strong> (ID: #{deletingMedicine.id})?
              </p>
              <p className="delete-subtext">
                This action cannot be undone. This medicine will be permanently removed from your schedule.
              </p>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setDeletingMedicine(null)}
                disabled={deleteLoading}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn-danger"
                onClick={handleConfirmDelete}
                disabled={deleteLoading}
              >
                {deleteLoading ? (
                  <span>Deleting...</span>
                ) : (
                  <>
                    <Trash2 size={16} />
                    <span>Delete Record</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

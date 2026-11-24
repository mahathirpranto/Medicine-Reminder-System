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
  User as UserIcon,
  LogOut,
  Bell,
  CheckCircle2,
  ListTodo,
  Shield,
  Crown,
} from 'lucide-react';
import {
  getMedicines,
  getMedicineById,
  createMedicine,
  updateMedicine,
  deleteMedicine,
  getTodaySchedule,
  logMedicineDose,
} from '../services/medicineApi';
import type { Medicine, MedicineCreateInput, TodayScheduleItem } from '../types/medicine';
import { MedicineList } from '../components/MedicineList';
import { MedicineForm } from '../components/MedicineForm';
import { DoseHistoryModal } from '../components/DoseHistoryModal';
import { AdminOverviewModal } from '../components/AdminOverviewModal';
import { useAuth } from '../context/AuthContext';

interface ToastMessage {
  id: number;
  type: 'success' | 'error' | 'info';
  text: string;
}

export const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');

  // Part 5: Today's Schedule & Dose Tracking States
  const [todaySchedule, setTodaySchedule] = useState<TodayScheduleItem[]>([]);
  const [historyMedicine, setHistoryMedicine] = useState<Medicine | null>(null);
  const [activeAlert, setActiveAlert] = useState<{ medicineName: string; dosage: string; time: string; medId: number } | null>(null);

  // Modal States
  const [isFormOpen, setIsFormOpen] = useState<boolean>(false);
  const [editingMedicine, setEditingMedicine] = useState<Medicine | null>(null);

  // Single View Modal State (CRUD: Read Single)
  const [viewingMedicine, setViewingMedicine] = useState<Medicine | null>(null);
  const [viewLoading, setViewLoading] = useState<boolean>(false);

  // Delete Confirmation State (CRUD: Delete)
  const [deletingMedicine, setDeletingMedicine] = useState<Medicine | null>(null);
  const [deleteLoading, setDeleteLoading] = useState<boolean>(false);

  // RBAC: Admin Overview Modal State
  const [isAdminModalOpen, setIsAdminModalOpen] = useState<boolean>(false);

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

  // 2. Fetch today's schedule (Part 5)
  const fetchSchedule = useCallback(async () => {
    try {
      const schedule = await getTodaySchedule();
      setTodaySchedule(schedule);
    } catch {
      // Ignore background errors
    }
  }, []);

  useEffect(() => {
    fetchMedicines();
    fetchSchedule();
  }, [fetchMedicines, fetchSchedule, user]);

  // Part 5: Real-time clock reminder engine (checks current time against reminder_time every 30s)
  useEffect(() => {
    const checkReminders = () => {
      const now = new Date();
      let hours = now.getHours();
      const minutes = now.getMinutes();
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12 || 12;
      const formattedHours = hours < 10 ? `0${hours}` : `${hours}`;
      const formattedMinutes = minutes < 10 ? `0${minutes}` : `${minutes}`;
      const currentTimeStr = `${formattedHours}:${formattedMinutes} ${ampm}`;

      for (const item of todaySchedule) {
        if (!item.status) continue;
        for (const scheduledTime of item.scheduled_times) {
          if (scheduledTime === currentTimeStr && !item.taken_times.includes(scheduledTime)) {
            setActiveAlert({
              medicineName: item.medicine_name,
              dosage: item.dosage,
              time: scheduledTime,
              medId: item.medicine_id,
            });
            break;
          }
        }
      }
    };

    checkReminders();
    const interval = setInterval(checkReminders, 30000);
    return () => clearInterval(interval);
  }, [todaySchedule]);

  // 3. Fetch single medicine (CRUD: Read Single)
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

  // 4. Handle Add / Edit Submission (CRUD: Create or Update)
  const handleFormSubmit = async (formData: MedicineCreateInput) => {
    if (editingMedicine) {
      const updated = await updateMedicine(editingMedicine.id, formData);
      setMedicines((prev) =>
        prev.map((med) => (med.id === updated.id ? updated : med))
      );
      addToast('success', `"${updated.medicine_name}" updated successfully!`);
    } else {
      const created = await createMedicine(formData);
      setMedicines((prev) => [created, ...prev]);
      addToast('success', `"${created.medicine_name}" created successfully!`);
    }
    fetchSchedule();
    setIsFormOpen(false);
    setEditingMedicine(null);
  };

  // 5. Toggle Status (CRUD: Update)
  const handleToggleStatus = async (medicine: Medicine) => {
    try {
      const updated = await updateMedicine(medicine.id, {
        status: !medicine.status,
      });
      setMedicines((prev) =>
        prev.map((med) => (med.id === updated.id ? updated : med))
      );
      fetchSchedule();
      addToast(
        'info',
        `"${updated.medicine_name}" marked as ${updated.status ? 'Active' : 'Inactive'}`
      );
    } catch (err) {
      addToast('error', 'Failed to toggle status');
    }
  };

  // 6. Delete operation (CRUD: Delete)
  const handleConfirmDelete = async () => {
    if (!deletingMedicine) return;
    try {
      setDeleteLoading(true);
      await deleteMedicine(deletingMedicine.id);
      setMedicines((prev) => prev.filter((med) => med.id !== deletingMedicine.id));
      fetchSchedule();
      addToast('success', `"${deletingMedicine.medicine_name}" was deleted successfully.`);
      setDeletingMedicine(null);
    } catch (err) {
      addToast('error', err instanceof Error ? err.message : 'Failed to delete medicine');
    } finally {
      setDeleteLoading(false);
    }
  };

  // 7. Part 5: Handle Mark as Taken Action
  const handleTakeDose = async (medicine: Medicine, specificTime?: string) => {
    try {
      await logMedicineDose(medicine.id, {
        dose_time: specificTime,
        status: 'taken',
      });
      addToast('success', `Dose for "${medicine.medicine_name}" recorded as taken!`);
      if (activeAlert?.medId === medicine.id) {
        setActiveAlert(null);
      }
      fetchSchedule();
    } catch (err) {
      addToast('error', 'Failed to record dose.');
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

  const handleLogout = async () => {
    await logout();
  };

  // Calculate statistics
  const totalCount = medicines.length;
  const activeCount = medicines.filter((m) => m.status).length;
  const inactiveCount = totalCount - activeCount;

  // Dose completion summary
  const totalDosesToday = todaySchedule.reduce((sum, item) => sum + item.scheduled_times.length, 0);
  const takenDosesToday = todaySchedule.reduce((sum, item) => sum + item.taken_times.length, 0);

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

      {/* Part 5: Live Reminder Alert Banner */}
      {activeAlert && (
        <div
          style={{
            background: 'linear-gradient(90deg, #059669 0%, #10b981 100%)',
            color: '#ffffff',
            padding: '0.85rem 1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            position: 'sticky',
            top: 0,
            zIndex: 100,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Bell size={22} className="bell-ring" />
            <div>
              <strong style={{ fontSize: '0.95rem' }}>Time for your scheduled medication!</strong>
              <span style={{ marginLeft: '0.5rem', fontSize: '0.875rem', opacity: 0.95 }}>
                {activeAlert.medicineName} ({activeAlert.dosage}) at {activeAlert.time}
              </span>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => {
                const med = medicines.find((m) => m.id === activeAlert.medId);
                if (med) handleTakeDose(med, activeAlert.time);
              }}
              style={{
                background: '#ffffff',
                color: '#059669',
                border: 'none',
                borderRadius: '6px',
                padding: '0.4rem 0.85rem',
                fontWeight: 700,
                fontSize: '0.825rem',
                cursor: 'pointer',
              }}
            >
              Take Now
            </button>
            <button
              type="button"
              onClick={() => setActiveAlert(null)}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#ffffff',
                cursor: 'pointer',
                opacity: 0.8,
              }}
            >
              <X size={18} />
            </button>
          </div>
        </div>
      )}

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

          <div className="header-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            {user && (() => {
              const isMainAdmin = Boolean(user.is_main_admin || user.role === 'super_admin' || user.email === 'admin@example.com');
              const isAdmin = isMainAdmin || user.role === 'admin';
              return (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    background: '#f8fafc',
                    padding: '0.4rem 0.85rem',
                    borderRadius: '20px',
                    fontSize: '0.85rem',
                    color: '#334155',
                    fontWeight: 600,
                    border: '1px solid #e2e8f0',
                  }}
                >
                  <UserIcon size={16} color="#059669" />
                  <span>{user.full_name || user.email}</span>
                  <span
                    style={{
                      fontSize: '0.72rem',
                      padding: '0.15rem 0.5rem',
                      borderRadius: '10px',
                      fontWeight: 700,
                      background: isMainAdmin
                        ? 'linear-gradient(135deg, #fef3c7 0%, #ede9fe 100%)'
                        : isAdmin
                        ? '#ede9fe'
                        : '#ecfdf5',
                      color: isMainAdmin ? '#7c2d12' : isAdmin ? '#6d28d9' : '#047857',
                      border: isMainAdmin ? '1px solid #fde68a' : 'none',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.25rem',
                    }}
                  >
                    {isMainAdmin ? (
                      <Crown size={11} color="#b45309" />
                    ) : isAdmin ? (
                      <Shield size={11} />
                    ) : null}
                    {isMainAdmin ? 'Main Admin' : isAdmin ? 'Admin' : 'Patient'}
                  </span>
                </div>
              );
            })()}

            {(user?.is_main_admin || user?.role === 'super_admin' || user?.role === 'admin' || user?.email === 'admin@example.com') && (
              <button
                type="button"
                onClick={() => setIsAdminModalOpen(true)}
                title="Open Administrative Controls & Metrics"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  padding: '0.55rem 0.95rem',
                  background: 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#ffffff',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  boxShadow: '0 2px 4px rgba(109, 40, 217, 0.25)',
                }}
              >
                <Shield size={16} />
                <span>Admin Portal</span>
              </button>
            )}

            <button
              type="button"
              className="btn-primary"
              onClick={handleOpenAdd}
            >
              <Plus size={18} />
              <span>Add Medicine</span>
            </button>

            <button
              type="button"
              onClick={handleLogout}
              title="Logout from Medicine Reminder System"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                padding: '0.55rem 0.9rem',
                background: '#ffffff',
                border: '1px solid #cbd5e1',
                borderRadius: '8px',
                color: '#475569',
                fontSize: '0.875rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.15s ease',
              }}
            >
              <LogOut size={16} />
              <span>Logout</span>
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

          <div className="stat-card stat-inactive">
            <div className="stat-icon-wrapper">
              <CheckCircle size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-value">
                {takenDosesToday} / {totalDosesToday}
              </span>
              <span className="stat-label">Today's Doses Taken</span>
            </div>
          </div>
        </div>

        {/* Part 5: Today's Schedule Overview Panel */}
        {todaySchedule.length > 0 && (
          <div
            style={{
              background: '#ffffff',
              borderRadius: '16px',
              padding: '1.25rem 1.5rem',
              marginBottom: '1.5rem',
              border: '1px solid #e2e8f0',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Clock size={20} color="#059669" />
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, margin: 0, color: '#0f172a' }}>
                  Today's Scheduled Reminders
                </h3>
              </div>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                {takenDosesToday} of {totalDosesToday} completed today
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '0.85rem' }}>
              {todaySchedule.map((item) => (
                <div
                  key={item.medicine_id}
                  style={{
                    padding: '0.85rem',
                    borderRadius: '10px',
                    background: item.is_fully_taken ? '#f0fdf4' : '#f8fafc',
                    border: `1px solid ${item.is_fully_taken ? '#bbf7d0' : '#e2e8f0'}`,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  <div style={{ marginBottom: '0.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.925rem', color: '#1e293b' }}>
                        {item.medicine_name}
                      </span>
                      {item.is_fully_taken && (
                        <span style={{ fontSize: '0.75rem', color: '#059669', display: 'flex', alignItems: 'center', gap: '0.2rem', fontWeight: 600 }}>
                          <CheckCircle2 size={14} /> Completed
                        </span>
                      )}
                    </div>
                    <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                      {item.dosage} &bull; {item.frequency}
                    </span>
                  </div>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                    {item.scheduled_times.map((time) => {
                      const isTaken = item.taken_times.includes(time);
                      return (
                        <button
                          key={time}
                          type="button"
                          disabled={isTaken}
                          onClick={() => {
                            const med = medicines.find((m) => m.id === item.medicine_id);
                            if (med) handleTakeDose(med, time);
                          }}
                          style={{
                            padding: '0.3rem 0.55rem',
                            borderRadius: '6px',
                            fontSize: '0.75rem',
                            fontWeight: 600,
                            border: '1px solid',
                            borderColor: isTaken ? '#86efac' : '#cbd5e1',
                            background: isTaken ? '#dcfce7' : '#ffffff',
                            color: isTaken ? '#15803d' : '#334155',
                            cursor: isTaken ? 'default' : 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.25rem',
                          }}
                        >
                          {isTaken ? <Check size={12} /> : <Clock size={12} />}
                          <span>{time}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Medicines List Section */}
        <MedicineList
          medicines={medicines}
          loading={loading}
          searchTerm={searchTerm}
          statusFilter={statusFilter}
          onSearchChange={setSearchTerm}
          onStatusFilterChange={setStatusFilter}
          onView={handleView}
          onEdit={handleOpenEdit}
          onDelete={(med) => setDeletingMedicine(med)}
          onToggleStatus={handleToggleStatus}
          onTakeDose={handleTakeDose}
          onViewHistory={(med) => setHistoryMedicine(med)}
          onRefresh={() => {
            fetchMedicines();
            fetchSchedule();
          }}
          onAddNew={handleOpenAdd}
        />
      </main>

      {/* Form Modal (CRUD: Create and Update) */}
      <MedicineForm
        isOpen={isFormOpen}
        initialData={editingMedicine}
        onClose={() => {
          setIsFormOpen(false);
          setEditingMedicine(null);
        }}
        onSubmit={handleFormSubmit}
      />

      {/* Dose History Modal (Part 5) */}
      <DoseHistoryModal
        medicine={historyMedicine}
        isOpen={!!historyMedicine}
        onClose={() => setHistoryMedicine(null)}
      />

      {/* Single Medicine Details Modal (CRUD: Read Single) */}
      {viewingMedicine && (
        <div className="modal-overlay" onClick={() => setViewingMedicine(null)}>
          <div className="modal-container detail-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="detail-modal-title">
                <Pill size={24} className="detail-pill-icon" />
                <h2>{viewingMedicine.medicine_name}</h2>
              </div>
              <button
                type="button"
                className="btn-close"
                onClick={() => setViewingMedicine(null)}
              >
                <X size={20} />
              </button>
            </div>

            <div className="detail-content">
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Dosage</span>
                  <span className="detail-value">{viewingMedicine.dosage}</span>
                </div>

                <div className="detail-item">
                  <span className="detail-label">Frequency</span>
                  <span className="detail-value">{viewingMedicine.frequency}</span>
                </div>

                <div className="detail-item">
                  <span className="detail-label">
                    <Clock size={16} /> Reminder Time
                  </span>
                  <span className="detail-value">{viewingMedicine.reminder_time}</span>
                </div>

                <div className="detail-item">
                  <span className="detail-label">Status</span>
                  <span
                    className={`status-badge ${
                      viewingMedicine.status ? 'status-active' : 'status-inactive'
                    }`}
                  >
                    {viewingMedicine.status ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <div className="detail-item full-width">
                  <span className="detail-label">
                    <Calendar size={16} /> Treatment Schedule
                  </span>
                  <span className="detail-value">
                    {viewingMedicine.start_date} to {viewingMedicine.end_date}
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
                Edit Medicine
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

      {/* RBAC: Admin Control Portal Modal */}
      <AdminOverviewModal
        isOpen={isAdminModalOpen}
        onClose={() => setIsAdminModalOpen(false)}
        onRoleChanged={fetchMedicines}
      />
    </div>
  );
};

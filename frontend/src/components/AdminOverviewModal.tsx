import React, { useEffect, useState, useCallback } from 'react';
import {
  X,
  ShieldAlert,
  Users,
  Pill,
  CheckCircle2,
  Activity,
  UserCheck,
  Shield,
  RefreshCw,
  Crown,
  Lock,
  Trash2,
} from 'lucide-react';
import type { AdminStats, AdminUserSummary } from '../types/auth';
import { getAdminStats, getAdminUsers, updateUserRole, deleteUserAccount } from '../services/authApi';
import { useAuth } from '../context/AuthContext';

interface AdminOverviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRoleChanged?: () => void;
}

export const AdminOverviewModal: React.FC<AdminOverviewModalProps> = ({
  isOpen,
  onClose,
  onRoleChanged,
}) => {
  const { user: currentUser } = useAuth();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUserSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const isCurrentMainAdmin = Boolean(
    currentUser?.is_main_admin ||
    currentUser?.role === 'super_admin' ||
    currentUser?.email === 'admin@example.com'
  );

  const loadAdminData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const [statsData, usersData] = await Promise.all([
        getAdminStats(),
        getAdminUsers(),
      ]);
      setStats(statsData);
      setUsers(usersData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load administrative data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      loadAdminData();
      setSuccessMsg(null);
    }
  }, [isOpen, loadAdminData]);

  const handleToggleRole = async (targetUser: AdminUserSummary) => {
    const isTargetMainAdmin = Boolean(
      targetUser.is_main_admin ||
      targetUser.role === 'super_admin' ||
      targetUser.email === 'admin@example.com'
    );

    if (isTargetMainAdmin) {
      setError('Permission denied: The Main System Administrator is protected and cannot be modified.');
      return;
    }

    if (targetUser.role === 'admin' && !isCurrentMainAdmin) {
      setError('Permission denied: Secondary administrators cannot modify or demote administrator accounts.');
      return;
    }

    const newRole = targetUser.role === 'admin' ? 'patient' : 'admin';
    const confirmPrompt = `Are you sure you want to change ${targetUser.full_name}'s role to '${newRole}'?`;
    if (!window.confirm(confirmPrompt)) return;

    try {
      setActionLoading(targetUser.id);
      setError(null);
      const res = await updateUserRole(targetUser.id, newRole);
      setSuccessMsg(res.message);
      await loadAdminData();
      if (onRoleChanged) onRoleChanged();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Role change failed');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteUser = async (targetUser: AdminUserSummary) => {
    if (!isCurrentMainAdmin) {
      setError('Permission denied: Only the Main System Administrator has authority to delete user accounts.');
      return;
    }

    const isTargetMainAdmin = Boolean(
      targetUser.is_main_admin ||
      targetUser.role === 'super_admin' ||
      targetUser.email === 'admin@example.com'
    );

    if (isTargetMainAdmin) {
      setError('The Main System Administrator cannot be deleted.');
      return;
    }

    const confirmPrompt = `Are you sure you want to permanently delete user "${targetUser.full_name}" (${targetUser.email})?\n\nThis will permanently remove their account, medications, and dose logs.`;
    if (!window.confirm(confirmPrompt)) return;

    try {
      setActionLoading(targetUser.id);
      setError(null);
      const res = await deleteUserAccount(targetUser.id);
      setSuccessMsg(res.message);
      await loadAdminData();
      if (onRoleChanged) onRoleChanged();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'User deletion failed');
    } finally {
      setActionLoading(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-container"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '820px', width: '95%', maxHeight: '90vh', overflowY: 'auto' }}
      >
        {/* Header */}
        <div
          className="modal-header"
          style={{
            borderBottom: '1px solid #f1f5f9',
            background: 'linear-gradient(135deg, #f8fafc 0%, #f3e8ff 100%)',
            padding: '1.25rem 1.75rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div
              style={{
                background: '#8b5cf6',
                color: '#ffffff',
                padding: '0.55rem',
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Shield size={22} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h2 style={{ margin: 0, fontSize: '1.25rem', color: '#1e293b' }}>
                  Admin Control Portal
                </h2>
                <span
                  style={{
                    background: '#ede9fe',
                    color: '#6d28d9',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    padding: '0.2rem 0.6rem',
                    borderRadius: '12px',
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em',
                  }}
                >
                  RBAC Active
                </span>
              </div>
              <p style={{ margin: '0.2rem 0 0', fontSize: '0.825rem', color: '#64748b' }}>
                System-wide overview, database metrics, and user permission management
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={loadAdminData}
              title="Refresh Data"
              disabled={loading}
              style={{
                background: '#ffffff',
                border: '1px solid #cbd5e1',
                borderRadius: '8px',
                padding: '0.45rem',
                cursor: loading ? 'not-allowed' : 'pointer',
                color: '#64748b',
                display: 'flex',
                alignItems: 'center',
              }}
            >
              <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            </button>
            <button type="button" className="btn-close" onClick={onClose}>
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div style={{ padding: '1.5rem 1.75rem' }}>
          {error && (
            <div
              style={{
                background: '#fef2f2',
                border: '1px solid #fecaca',
                color: '#dc2626',
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1.25rem',
                fontSize: '0.875rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              <ShieldAlert size={18} />
              <span>{error}</span>
            </div>
          )}

          {successMsg && (
            <div
              style={{
                background: '#f0fdf4',
                border: '1px solid #bbf7d0',
                color: '#15803d',
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                marginBottom: '1.25rem',
                fontSize: '0.875rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              <CheckCircle2 size={18} />
              <span>{successMsg}</span>
            </div>
          )}

          {/* Metric Cards Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
              gap: '1rem',
              marginBottom: '1.75rem',
            }}
          >
            {/* Total Users */}
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '10px',
                padding: '1rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#64748b' }}>
                <span style={{ fontSize: '0.775rem', fontWeight: 600, textTransform: 'uppercase' }}>Users</span>
                <Users size={16} color="#6366f1" />
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e293b', margin: '0.35rem 0' }}>
                {stats?.total_users ?? (loading ? '...' : 0)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span style={{ color: '#059669', fontWeight: 600 }}>{stats?.total_patients ?? 0}</span> Patients &bull;{' '}
                <span style={{ color: '#7c3aed', fontWeight: 600 }}>{stats?.total_admins ?? 0}</span> Admins
              </div>
            </div>

            {/* Total Medicines */}
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '10px',
                padding: '1rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#64748b' }}>
                <span style={{ fontSize: '0.775rem', fontWeight: 600, textTransform: 'uppercase' }}>Medicines</span>
                <Pill size={16} color="#059669" />
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e293b', margin: '0.35rem 0' }}>
                {stats?.total_medicines ?? (loading ? '...' : 0)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span style={{ color: '#059669', fontWeight: 600 }}>{stats?.active_medicines ?? 0}</span> Active Schedules
              </div>
            </div>

            {/* Doses Taken Today */}
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '10px',
                padding: '1rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#64748b' }}>
                <span style={{ fontSize: '0.775rem', fontWeight: 600, textTransform: 'uppercase' }}>Doses Today</span>
                <CheckCircle2 size={16} color="#10b981" />
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e293b', margin: '0.35rem 0' }}>
                {stats?.doses_taken_today ?? (loading ? '...' : 0)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span>Across all active patients</span>
              </div>
            </div>

            {/* Total Doses Logged */}
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '10px',
                padding: '1rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#64748b' }}>
                <span style={{ fontSize: '0.775rem', fontWeight: 600, textTransform: 'uppercase' }}>Total Logs</span>
                <Activity size={16} color="#f59e0b" />
              </div>
              <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#1e293b', margin: '0.35rem 0' }}>
                {stats?.total_doses_logged ?? (loading ? '...' : 0)}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span>Lifetime compliance events</span>
              </div>
            </div>
          </div>

          {/* User Management Directory */}
          <div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '0.85rem',
              }}
            >
              <h3 style={{ margin: 0, fontSize: '1rem', color: '#1e293b', fontWeight: 700 }}>
                Registered User Directory & Roles
              </h3>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>
                {users.length} registered accounts
              </span>
            </div>

            <div
              style={{
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                overflow: 'hidden',
              }}
            >
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
                    <th style={{ padding: '0.75rem 1rem', color: '#475569', fontWeight: 600 }}>User / Email</th>
                    <th style={{ padding: '0.75rem 1rem', color: '#475569', fontWeight: 600 }}>Role</th>
                    <th style={{ padding: '0.75rem 1rem', color: '#475569', fontWeight: 600 }}>Medicines</th>
                    <th style={{ padding: '0.75rem 1rem', color: '#475569', fontWeight: 600 }}>Joined</th>
                    <th style={{ padding: '0.75rem 1rem', color: '#475569', fontWeight: 600, textAlign: 'right' }}>
                      RBAC Action
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {loading && users.length === 0 ? (
                    <tr>
                      <td colSpan={5} style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
                        Loading registered accounts...
                      </td>
                    </tr>
                  ) : users.length === 0 ? (
                    <tr>
                      <td colSpan={5} style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                        No users registered in the system.
                      </td>
                    </tr>
                  ) : (
                    users.map((u) => {
                      const isTargetMain = Boolean(
                        u.is_main_admin ||
                        u.role === 'super_admin' ||
                        u.email === 'admin@example.com'
                      );
                      const isTargetAdmin = u.role === 'admin' || isTargetMain;
                      const isPendingAction = actionLoading === u.id;
                      return (
                        <tr
                          key={u.id}
                          style={{
                            borderBottom: '1px solid #f1f5f9',
                            transition: 'background 0.15s ease',
                          }}
                        >
                          <td style={{ padding: '0.75rem 1rem' }}>
                            <div style={{ fontWeight: 600, color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                              <span>{u.full_name}</span>
                              {isTargetMain && <Crown size={14} color="#f59e0b" />}
                            </div>
                            <div style={{ fontSize: '0.775rem', color: '#64748b' }}>{u.email}</div>
                          </td>
                          <td style={{ padding: '0.75rem 1rem' }}>
                            <span
                              style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '0.3rem',
                                padding: '0.2rem 0.6rem',
                                borderRadius: '12px',
                                fontSize: '0.75rem',
                                fontWeight: 700,
                                background: isTargetMain
                                  ? 'linear-gradient(135deg, #fef3c7 0%, #ede9fe 100%)'
                                  : isTargetAdmin
                                  ? '#ede9fe'
                                  : '#ecfdf5',
                                color: isTargetMain ? '#7c2d12' : isTargetAdmin ? '#6d28d9' : '#047857',
                                border: isTargetMain ? '1px solid #fde68a' : 'none',
                              }}
                            >
                              {isTargetMain ? (
                                <Crown size={12} color="#b45309" />
                              ) : isTargetAdmin ? (
                                <Shield size={12} />
                              ) : (
                                <UserCheck size={12} />
                              )}
                              {isTargetMain
                                ? 'Main Admin'
                                : isTargetAdmin
                                ? 'Admin'
                                : 'Patient'}
                            </span>
                          </td>
                          <td style={{ padding: '0.75rem 1rem', color: '#475569' }}>
                            <span style={{ fontWeight: 600 }}>{u.medicines_count}</span> total{' '}
                            <span style={{ color: '#059669', fontSize: '0.775rem' }}>
                              ({u.active_medicines_count} active)
                            </span>
                          </td>
                          <td style={{ padding: '0.75rem 1rem', color: '#64748b', fontSize: '0.8rem' }}>
                            {new Date(u.created_at).toLocaleDateString()}
                          </td>
                          <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', justifyContent: 'flex-end' }}>
                              {isTargetMain ? (
                                <button
                                  type="button"
                                  disabled
                                  title="System Administrator cannot be demoted or modified"
                                  style={{
                                    border: '1px solid #e2e8f0',
                                    background: '#f8fafc',
                                    color: '#94a3b8',
                                    borderRadius: '6px',
                                    padding: '0.35rem 0.65rem',
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    cursor: 'not-allowed',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '0.25rem',
                                  }}
                                >
                                  <Lock size={12} />
                                  <span>Protected Main Admin</span>
                                </button>
                              ) : isTargetAdmin && !isCurrentMainAdmin ? (
                                <button
                                  type="button"
                                  disabled
                                  title="Only the Main System Administrator can demote fellow admins"
                                  style={{
                                    border: '1px solid #e2e8f0',
                                    background: '#f8fafc',
                                    color: '#94a3b8',
                                    borderRadius: '6px',
                                    padding: '0.35rem 0.65rem',
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    cursor: 'not-allowed',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '0.25rem',
                                  }}
                                >
                                  <Lock size={12} />
                                  <span>Protected Admin</span>
                                </button>
                              ) : (
                                <button
                                  type="button"
                                  onClick={() => handleToggleRole(u)}
                                  disabled={isPendingAction}
                                  style={{
                                    border: isTargetAdmin ? '1px solid #cbd5e1' : '1px solid #c084fc',
                                    background: isTargetAdmin ? '#f8fafc' : '#faf5ff',
                                    color: isTargetAdmin ? '#475569' : '#7e22ce',
                                    borderRadius: '6px',
                                    padding: '0.35rem 0.65rem',
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    cursor: isPendingAction ? 'not-allowed' : 'pointer',
                                  }}
                                >
                                  {isPendingAction
                                    ? 'Updating...'
                                    : isTargetAdmin
                                    ? 'Demote to Patient'
                                    : 'Promote to Admin'}
                                </button>
                              )}

                              {/* Delete User: Exclusively visible to the Main System Administrator for non-main users */}
                              {isCurrentMainAdmin && !isTargetMain && (
                                <button
                                  type="button"
                                  onClick={() => handleDeleteUser(u)}
                                  disabled={isPendingAction}
                                  title={`Permanently delete user ${u.full_name}`}
                                  style={{
                                    border: '1px solid #fecaca',
                                    background: '#fef2f2',
                                    color: '#dc2626',
                                    borderRadius: '6px',
                                    padding: '0.35rem 0.6rem',
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    cursor: isPendingAction ? 'not-allowed' : 'pointer',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '0.25rem',
                                    transition: 'all 0.15s ease',
                                  }}
                                >
                                  <Trash2 size={12} />
                                  <span>Delete</span>
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            borderTop: '1px solid #f1f5f9',
            padding: '1rem 1.75rem',
            display: 'flex',
            justifyContent: 'flex-end',
            background: '#fafafa',
          }}
        >
          <button
            type="button"
            className="btn-secondary"
            onClick={onClose}
            style={{ padding: '0.5rem 1.25rem', fontSize: '0.875rem' }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

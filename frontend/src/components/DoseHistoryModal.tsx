import React, { useEffect, useState } from 'react';
import { X, CheckCircle2, Clock, Calendar, AlertCircle } from 'lucide-react';
import type { Medicine, DoseLog } from '../types/medicine';
import { getMedicineDoseHistory } from '../services/medicineApi';

interface DoseHistoryModalProps {
  medicine: Medicine | null;
  isOpen: boolean;
  onClose: () => void;
}

export const DoseHistoryModal: React.FC<DoseHistoryModalProps> = ({
  medicine,
  isOpen,
  onClose,
}) => {
  const [logs, setLogs] = useState<DoseLog[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (medicine && isOpen) {
      setLoading(true);
      getMedicineDoseHistory(medicine.id)
        .then((data) => setLogs(data))
        .catch(() => setLogs([]))
        .finally(() => setLoading(false));
    }
  }, [medicine, isOpen]);

  if (!isOpen || !medicine) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '480px' }}>
        <div className="modal-header">
          <div>
            <h2>Dose History</h2>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.85rem', color: '#64748b' }}>
              {medicine.medicine_name} ({medicine.dosage})
            </p>
          </div>
          <button type="button" className="btn-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: '1rem 1.5rem', maxHeight: '380px', overflowY: 'auto' }}>
          {loading ? (
            <p style={{ textAlign: 'center', color: '#64748b', padding: '1.5rem 0' }}>Loading history...</p>
          ) : logs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 1rem', color: '#94a3b8' }}>
              <Clock size={36} style={{ margin: '0 auto 0.5rem', display: 'block', opacity: 0.6 }} />
              <p style={{ fontWeight: 500, margin: '0 0 0.25rem' }}>No doses logged yet</p>
              <span style={{ fontSize: '0.8rem' }}>Click "Mark as Taken" on this medicine card to record your intake.</span>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {logs.map((log) => (
                <div
                  key={log.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.75rem 1rem',
                    background: '#f8fafc',
                    borderRadius: '10px',
                    border: '1px solid #e2e8f0',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <div
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '50%',
                        background: log.status === 'taken' ? '#ecfdf5' : '#fee2e2',
                        color: log.status === 'taken' ? '#059669' : '#dc2626',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <CheckCircle2 size={18} />
                    </div>
                    <div>
                      <span style={{ fontWeight: 600, fontSize: '0.9rem', color: '#1e293b', display: 'block' }}>
                        Dose Time: {log.dose_time}
                      </span>
                      <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                        Recorded: {new Date(log.taken_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                  <span
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: 600,
                      padding: '0.2rem 0.6rem',
                      borderRadius: '20px',
                      background: log.status === 'taken' ? '#d1fae5' : '#fee2e2',
                      color: log.status === 'taken' ? '#047857' : '#b91c1c',
                      textTransform: 'capitalize',
                    }}
                  >
                    {log.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="modal-actions" style={{ padding: '1rem 1.5rem', borderTop: '1px solid #f1f5f9' }}>
          <button type="button" className="btn-secondary" onClick={onClose} style={{ width: '100%' }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { Pill, Clock, Calendar, CheckCircle2, XCircle, Edit3, Trash2, Eye } from 'lucide-react';
import type { Medicine } from '../services/medicineApi';

interface MedicineCardProps {
  medicine: Medicine;
  onView: (id: number) => void;
  onEdit: (medicine: Medicine) => void;
  onDelete: (medicine: Medicine) => void;
  onToggleStatus: (medicine: Medicine) => void;
}

export const MedicineCard: React.FC<MedicineCardProps> = ({
  medicine,
  onView,
  onEdit,
  onDelete,
  onToggleStatus,
}) => {
  return (
    <div className={`med-card ${medicine.status ? 'med-card-active' : 'med-card-inactive'}`}>
      <div className="med-card-header">
        <div className="med-title-group">
          <div className={`med-icon-wrap ${medicine.status ? 'icon-wrap-active' : 'icon-wrap-inactive'}`}>
            <Pill size={20} />
          </div>
          <div>
            <h3 className="med-name">{medicine.medicine_name}</h3>
            <span className="med-dosage-freq">
              {medicine.dosage} &bull; {medicine.frequency}
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={() => onToggleStatus(medicine)}
          className={`status-badge-btn ${medicine.status ? 'status-badge-active' : 'status-badge-inactive'}`}
          title="Click to toggle status"
        >
          {medicine.status ? (
            <>
              <CheckCircle2 size={14} />
              <span>Active</span>
            </>
          ) : (
            <>
              <XCircle size={14} />
              <span>Inactive</span>
            </>
          )}
        </button>
      </div>

      <div className="med-card-details">
        <div className="med-detail-item">
          <Clock size={16} className="detail-icon" />
          <span className="detail-text">
            <strong>Time:</strong> {medicine.reminder_time}
          </span>
        </div>

        <div className="med-detail-item">
          <Calendar size={16} className="detail-icon" />
          <span className="detail-text">
            <strong>Duration:</strong> {medicine.start_date} &rarr; {medicine.end_date}
          </span>
        </div>
      </div>

      <div className="med-card-actions">
        <button
          type="button"
          onClick={() => onView(medicine.id)}
          className="btn-action btn-view"
          title="View Single Medicine Details"
        >
          <Eye size={15} />
          <span>Details</span>
        </button>
        <button
          type="button"
          onClick={() => onEdit(medicine)}
          className="btn-action btn-edit"
          title="Edit Medicine"
        >
          <Edit3 size={15} />
          <span>Edit</span>
        </button>
        <button
          type="button"
          onClick={() => onDelete(medicine)}
          className="btn-action btn-delete"
          title="Delete Medicine"
        >
          <Trash2 size={15} />
          <span>Delete</span>
        </button>
      </div>
    </div>
  );
};

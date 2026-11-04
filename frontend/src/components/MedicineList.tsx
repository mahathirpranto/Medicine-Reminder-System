import React from 'react';
import { Search, Plus, Filter, Pill, RefreshCw } from 'lucide-react';
import { MedicineCard } from './MedicineCard';
import type { Medicine } from '../services/medicineApi';

interface MedicineListProps {
  medicines: Medicine[];
  loading: boolean;
  searchTerm: string;
  onSearchChange: (value: string) => void;
  statusFilter: 'all' | 'active' | 'inactive';
  onStatusFilterChange: (filter: 'all' | 'active' | 'inactive') => void;
  onView: (id: number) => void;
  onEdit: (medicine: Medicine) => void;
  onDelete: (medicine: Medicine) => void;
  onToggleStatus: (medicine: Medicine) => void;
  onAddNew: () => void;
  onRefresh: () => void;
}

export const MedicineList: React.FC<MedicineListProps> = ({
  medicines,
  loading,
  searchTerm,
  onSearchChange,
  statusFilter,
  onStatusFilterChange,
  onView,
  onEdit,
  onDelete,
  onToggleStatus,
  onAddNew,
  onRefresh,
}) => {
  // Filter medicines based on search and status tabs
  const filteredMedicines = medicines.filter((med) => {
    const matchesSearch =
      med.medicine_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      med.dosage.toLowerCase().includes(searchTerm.toLowerCase()) ||
      med.frequency.toLowerCase().includes(searchTerm.toLowerCase());

    if (statusFilter === 'active') return matchesSearch && med.status === true;
    if (statusFilter === 'inactive') return matchesSearch && med.status === false;
    return matchesSearch;
  });

  return (
    <div className="medicine-list-section">
      <div className="list-toolbar">
        <div className="search-box">
          <Search size={18} className="search-icon" />
          <input
            type="text"
            placeholder="Search medicines by name or dosage..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
          />
          {searchTerm && (
            <button
              type="button"
              className="clear-search-btn"
              onClick={() => onSearchChange('')}
            >
              &times;
            </button>
          )}
        </div>

        <div className="filter-actions">
          <div className="filter-tabs">
            <button
              type="button"
              className={`filter-tab ${statusFilter === 'all' ? 'active' : ''}`}
              onClick={() => onStatusFilterChange('all')}
            >
              All ({medicines.length})
            </button>
            <button
              type="button"
              className={`filter-tab ${statusFilter === 'active' ? 'active' : ''}`}
              onClick={() => onStatusFilterChange('active')}
            >
              Active ({medicines.filter((m) => m.status).length})
            </button>
            <button
              type="button"
              className={`filter-tab ${statusFilter === 'inactive' ? 'active' : ''}`}
              onClick={() => onStatusFilterChange('inactive')}
            >
              Inactive ({medicines.filter((m) => !m.status).length})
            </button>
          </div>

          <button
            type="button"
            className="btn-refresh"
            onClick={onRefresh}
            title="Refresh list"
            disabled={loading}
          >
            <RefreshCw size={16} className={loading ? 'spin' : ''} />
          </button>
        </div>
      </div>

      {loading && medicines.length === 0 ? (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading medicines from database...</p>
        </div>
      ) : filteredMedicines.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon-box">
            <Pill size={44} />
          </div>
          <h3>No medicines found</h3>
          <p>
            {searchTerm || statusFilter !== 'all'
              ? 'Try adjusting your search query or filter options.'
              : 'You have not added any medicines yet. Get started by adding your first medicine schedule!'}
          </p>
          <button type="button" className="btn-primary" onClick={onAddNew}>
            <Plus size={18} />
            <span>Add New Medicine</span>
          </button>
        </div>
      ) : (
        <div className="medicine-cards-grid">
          {filteredMedicines.map((medicine) => (
            <MedicineCard
              key={medicine.id}
              medicine={medicine}
              onView={onView}
              onEdit={onEdit}
              onDelete={onDelete}
              onToggleStatus={onToggleStatus}
            />
          ))}
        </div>
      )}
    </div>
  );
};

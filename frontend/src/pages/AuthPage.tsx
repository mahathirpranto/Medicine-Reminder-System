import React, { useState } from 'react';
import { Pill, Lock, Mail, User as UserIcon, AlertCircle, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AuthPage: React.FC = () => {
  const { login, signup } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');

  // Form fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');

  // UI state
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (mode === 'login') {
      if (!email.trim() || !password) {
        setError('Please enter both email and password.');
        return;
      }

      setIsSubmitting(true);
      try {
        await login({ email: email.trim(), password });
      } catch (err: any) {
        setError(err.message || 'Invalid email or password. Please try again.');
      } finally {
        setIsSubmitting(false);
      }
    } else {
      // Register validation
      if (!fullName.trim() || !email.trim() || !password) {
        setError('Please complete all required fields.');
        return;
      }
      if (password.length < 6) {
        setError('Password must be at least 6 characters long.');
        return;
      }
      if (password !== confirmPassword) {
        setError('Passwords do not match.');
        return;
      }

      setIsSubmitting(true);
      try {
        await signup({
          full_name: fullName.trim(),
          email: email.trim(),
          password,
        });
      } catch (err: any) {
        setError(err.message || 'Registration failed. Email might already be taken.');
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f0fdf4 0%, #f8fafc 50%, #eff6ff 100%)',
        padding: '2rem 1rem',
        fontFamily: "var(--font-sans, 'Inter', system-ui, sans-serif)",
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '460px',
          background: '#ffffff',
          borderRadius: '20px',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
          border: '1px solid #e2e8f0',
          overflow: 'hidden',
        }}
      >
        {/* Header Branding */}
        <div
          style={{
            padding: '2rem 2rem 1.5rem',
            textAlign: 'center',
            background: 'linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%)',
            borderBottom: '1px solid #f1f5f9',
          }}
        >
          <div
            style={{
              width: '56px',
              height: '56px',
              borderRadius: '16px',
              background: '#059669',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              margin: '0 auto 1rem',
              boxShadow: '0 4px 6px -1px rgba(5, 150, 105, 0.25)',
            }}
          >
            <Pill size={32} />
          </div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#0f172a', margin: '0 0 0.4rem' }}>
            Medicine Reminder System
          </h1>
          <p style={{ fontSize: '0.875rem', color: '#64748b', margin: 0 }}>
            {mode === 'login'
              ? 'Please sign in to access your personal medicine schedule'
              : 'Create an account to securely track your medications'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div style={{ padding: '1.25rem 2rem 0' }}>
          <div
            style={{
              display: 'flex',
              background: '#f1f5f9',
              borderRadius: '10px',
              padding: '4px',
              gap: '4px',
            }}
          >
            <button
              type="button"
              onClick={() => {
                setMode('login');
                setError(null);
              }}
              style={{
                flex: 1,
                padding: '0.6rem 0',
                fontSize: '0.875rem',
                fontWeight: 600,
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                background: mode === 'login' ? '#ffffff' : 'transparent',
                color: mode === 'login' ? '#059669' : '#64748b',
                boxShadow: mode === 'login' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
              }}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => {
                setMode('register');
                setError(null);
              }}
              style={{
                flex: 1,
                padding: '0.6rem 0',
                fontSize: '0.875rem',
                fontWeight: 600,
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                background: mode === 'register' ? '#ffffff' : 'transparent',
                color: mode === 'register' ? '#059669' : '#64748b',
                boxShadow: mode === 'register' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
              }}
            >
              Create Account
            </button>
          </div>
        </div>

        {/* Form Body */}
        <div style={{ padding: '1.5rem 2rem 2.25rem' }}>
          {error && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.6rem',
                padding: '0.75rem 1rem',
                backgroundColor: '#fee2e2',
                color: '#b91c1c',
                borderRadius: '10px',
                fontSize: '0.875rem',
                marginBottom: '1.25rem',
                border: '1px solid #fecaca',
              }}
            >
              <AlertCircle size={18} style={{ flexShrink: 0 }} />
              <span>{error}</span>
            </div>
          )}

          {mode === 'login' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.4rem', marginBottom: '1.25rem' }}>
              <button
                type="button"
                onClick={() => {
                  setEmail('admin@example.com');
                  setPassword('AdminPassword123!');
                }}
                title="Fill credentials for Main System Administrator"
                style={{
                  padding: '0.45rem 0.25rem',
                  fontSize: '0.725rem',
                  fontWeight: 600,
                  background: '#fef3c7',
                  color: '#92400e',
                  border: '1px solid #fde68a',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                👑 Main Admin
              </button>
              <button
                type="button"
                onClick={() => {
                  setEmail('vatista@example.com');
                  setPassword('VatistaPassword123!');
                }}
                title="Fill credentials for Vatista (Secondary Administrator)"
                style={{
                  padding: '0.45rem 0.25rem',
                  fontSize: '0.725rem',
                  fontWeight: 600,
                  background: '#ede9fe',
                  color: '#6d28d9',
                  border: '1px solid #ddd6fe',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                🛡️ Vatista
              </button>
              <button
                type="button"
                onClick={() => {
                  setEmail('test_patient_rbac@example.com');
                  setPassword('PatientPassword123!');
                }}
                title="Fill credentials for test Patient account"
                style={{
                  padding: '0.45rem 0.25rem',
                  fontSize: '0.725rem',
                  fontWeight: 600,
                  background: '#ecfdf5',
                  color: '#047857',
                  border: '1px solid #a7f3d0',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                🧑‍⚕️ Patient
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {mode === 'register' && (
              <div style={{ marginBottom: '1.1rem' }}>
                <label
                  style={{
                    display: 'block',
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: '#334155',
                    marginBottom: '0.4rem',
                  }}
                >
                  Full Name
                </label>
                <div style={{ position: 'relative' }}>
                  <UserIcon
                    size={18}
                    style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }}
                  />
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Mahathir Pranto"
                    required
                    style={{
                      width: '100%',
                      padding: '0.7rem 0.85rem 0.7rem 2.4rem',
                      borderRadius: '8px',
                      border: '1px solid #cbd5e1',
                      fontSize: '0.925rem',
                      outline: 'none',
                    }}
                  />
                </div>
              </div>
            )}

            <div style={{ marginBottom: '1.1rem' }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  color: '#334155',
                  marginBottom: '0.4rem',
                }}
              >
                Email Address
              </label>
              <div style={{ position: 'relative' }}>
                <Mail
                  size={18}
                  style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }}
                />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  required
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.85rem 0.7rem 2.4rem',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.925rem',
                    outline: 'none',
                  }}
                />
              </div>
            </div>

            <div style={{ marginBottom: mode === 'register' ? '1.1rem' : '1.5rem' }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  color: '#334155',
                  marginBottom: '0.4rem',
                }}
              >
                Password {mode === 'register' && '(min. 6 chars)'}
              </label>
              <div style={{ position: 'relative' }}>
                <Lock
                  size={18}
                  style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }}
                />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  minLength={mode === 'register' ? 6 : undefined}
                  style={{
                    width: '100%',
                    padding: '0.7rem 0.85rem 0.7rem 2.4rem',
                    borderRadius: '8px',
                    border: '1px solid #cbd5e1',
                    fontSize: '0.925rem',
                    outline: 'none',
                  }}
                />
              </div>
            </div>

            {mode === 'register' && (
              <div style={{ marginBottom: '1.5rem' }}>
                <label
                  style={{
                    display: 'block',
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: '#334155',
                    marginBottom: '0.4rem',
                  }}
                >
                  Confirm Password
                </label>
                <div style={{ position: 'relative' }}>
                  <Lock
                    size={18}
                    style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }}
                  />
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    minLength={6}
                    style={{
                      width: '100%',
                      padding: '0.7rem 0.85rem 0.7rem 2.4rem',
                      borderRadius: '8px',
                      border: '1px solid #cbd5e1',
                      fontSize: '0.925rem',
                      outline: 'none',
                    }}
                  />
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              style={{
                width: '100%',
                padding: '0.85rem',
                background: '#059669',
                color: '#ffffff',
                border: 'none',
                borderRadius: '10px',
                fontSize: '0.95rem',
                fontWeight: 600,
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                boxShadow: '0 4px 6px -1px rgba(5, 150, 105, 0.3)',
                transition: 'background 0.15s ease',
              }}
            >
              <span>{isSubmitting ? 'Processing...' : mode === 'login' ? 'Sign In to Dashboard' : 'Create Account'}</span>
              {!isSubmitting && <ArrowRight size={18} />}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

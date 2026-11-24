/**
 * Authentication & Session Types
 */

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'patient' | 'admin' | 'super_admin';
  is_main_admin?: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  signup: (credentials: SignupCredentials) => Promise<void>;
  logout: () => Promise<void>;
}

export interface AdminStats {
  total_users: number;
  total_patients: number;
  total_admins: number;
  total_medicines: number;
  active_medicines: number;
  total_doses_logged: number;
  doses_taken_today: number;
}

export interface AdminUserSummary {
  id: number;
  email: string;
  full_name: string;
  role: 'patient' | 'admin' | 'super_admin';
  is_main_admin?: boolean;
  created_at: string;
  medicines_count: number;
  active_medicines_count: number;
}

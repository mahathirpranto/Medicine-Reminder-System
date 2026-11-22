/**
 * Authentication API Service
 * Handles user signup, login, refresh token rotation, session revocation, and current user retrieval.
 */

import type {
  User,
  TokenResponse,
  RefreshTokenResponse,
  LoginCredentials,
  SignupCredentials,
} from '../types/auth';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const ACCESS_TOKEN_KEY = 'medrem_access_token';
const REFRESH_TOKEN_KEY = 'medrem_refresh_token';
const USER_KEY = 'medrem_user';

export function getStoredAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getStoredRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getStoredUser(): User | null {
  const data = localStorage.getItem(USER_KEY);
  if (!data) return null;
  try {
    return JSON.parse(data);
  } catch {
    return null;
  }
}

export function saveSession(tokens: TokenResponse): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
  localStorage.setItem(USER_KEY, JSON.stringify(tokens.user));
}

export function clearSession(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

/**
 * 1. SIGNUP
 * POST /api/auth/signup
 */
export async function signupUser(credentials: SignupCredentials): Promise<TokenResponse> {
  const response = await fetch(`${BASE_URL}/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Registration failed (${response.status})`);
  }

  const data: TokenResponse = await response.json();
  saveSession(data);
  return data;
}

/**
 * 2. LOGIN
 * POST /api/auth/login
 */
export async function loginUser(credentials: LoginCredentials): Promise<TokenResponse> {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Login failed (${response.status})`);
  }

  const data: TokenResponse = await response.json();
  saveSession(data);
  return data;
}

/**
 * 3. REFRESH SESSION
 * POST /api/auth/refresh
 */
export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = getStoredRefreshToken();
  if (!refreshToken) {
    clearSession();
    return null;
  }

  try {
    const response = await fetch(`${BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      clearSession();
      return null;
    }

    const data: RefreshTokenResponse = await response.json();
    localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
    return data.access_token;
  } catch {
    clearSession();
    return null;
  }
}

/**
 * 4. LOGOUT
 * POST /api/auth/logout
 */
export async function logoutUser(): Promise<void> {
  const refreshToken = getStoredRefreshToken();
  if (refreshToken) {
    try {
      await fetch(`${BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    } catch {
      // Ignore network errors on logout
    }
  }
  clearSession();
}

/**
 * 5. GET CURRENT USER
 * GET /api/users/me
 */
export async function fetchCurrentUser(): Promise<User | null> {
  const response = await authenticatedFetch(`${BASE_URL}/users/me`);
  if (!response.ok) return null;
  return response.json();
}

/**
 * Silent Refresh Interceptor
 * Intercepts requests, attaches the Bearer token, and automatically retries
 * when encountering a 401 by renewing the token with the refresh token.
 */
export async function authenticatedFetch(url: string, options: RequestInit = {}): Promise<Response> {
  let token = getStoredAccessToken();

  const headers = new Headers(options.headers || {});
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  let response = await fetch(url, { ...options, headers });

  // If 401 Unauthorized, attempt silent refresh
  if (response.status === 401) {
    const newToken = await refreshAccessToken();
    if (newToken) {
      headers.set('Authorization', `Bearer ${newToken}`);
      response = await fetch(url, { ...options, headers });
    }
  }

  return response;
}

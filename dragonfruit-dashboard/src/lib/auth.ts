// lib/auth.ts
import { fetchFromAPI } from './api';

export interface User {
  uid: string;
  username: string;
  email: string;
}

let currentUser: User | null = null; // optional: in-memory cache (use carefully)

export async function getCurrentUser(): Promise<User | null> {
  try {
    const user = await fetchFromAPI<User>('/api/auth/me', {
      credentials: 'include',
    });
    currentUser = user;
    return user;
  } catch (err) {
    currentUser = null;
    return null;
  }
}

// ✅ NEW: explicit logout function
export async function logout(): Promise<void> {
  try {
    await fetchFromAPI('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });
  } catch (err) {
    console.warn('Logout API error (safe to ignore):', err);
  } finally {
    // Clear any local user state
    currentUser = null;
    // Note: cookie is cleared by backend; no need to do anything else here
  }
}
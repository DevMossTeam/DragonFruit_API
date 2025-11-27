// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchFromAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!res.ok) {
      const errorText = await res.text(); // Get raw response 
      throw new Error(`HTTP ${res.status} - ${res.statusText}: ${errorText}`);
    }

    return res.json();
  } catch (err) {
    console.error('API Error:', err); // show console error for debugging from API hit
    throw err;
  }
}
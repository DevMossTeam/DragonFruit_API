// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchFromAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    console.log(`📡 Fetching: ${API_BASE_URL}${endpoint}`, { method: options?.method, headers: options?.headers });
    
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!res.ok) {
      const errorText = await res.text(); // Get raw response 
      console.error(`❌ HTTP Error: ${res.status}`, errorText);
      throw new Error(`HTTP ${res.status} - ${res.statusText}: ${errorText}`);
    }

    return res.json();
  } catch (err) {
    console.error('🔴 API Error:', err);
    // More helpful CORS error messages
    if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
      console.error('⚠️  CORS or network error. Check:');
      console.error('  - Backend running at:', API_BASE_URL);
      console.error('  - Backend CORS allows:', window.location.origin);
      console.error('  - Check browser console Network tab for details');
    }
    throw err;
  }
}
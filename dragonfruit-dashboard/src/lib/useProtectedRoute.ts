import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

/**
 * Hook to protect routes - redirects to login if user is not authenticated
 * Should be used in 'use client' components that require authentication
 */
export function useProtectedRoute() {
  const router = useRouter();

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    
    if (!userStr) {
      // No user in localStorage, redirect to login
      router.push('/login');
    }
  }, [router]);
}

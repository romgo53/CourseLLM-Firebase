"use client";

import React, { useEffect } from 'react';
import { useAuth } from './AuthProviderClient';
import { usePathname, useRouter } from 'next/navigation';

export default function AuthRedirector() {
  const { firebaseUser, profile, loading, onboardingRequired } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (loading) return;

    // If not logged in, do nothing here
    if (!firebaseUser) return;

    // If onboarding required, navigate to onboarding when on neutral pages (root/login)
    if (onboardingRequired) {
      if (pathname !== '/onboarding') {
        router.replace('/onboarding');
      }
      return;
    }

    // If profile exists, enforce role-based dashboard access
    if (profile && profile.role) {
      const allowed = profile.role === 'teacher' ? '/teacher' : '/student';

      // Redirect neutral entry points to the allowed dashboard
      if (pathname === '/' || pathname === '/login' || pathname === '') {
        router.replace(allowed);
        return;
      }

      // Block access to the other dashboard's routes
      if (pathname.startsWith('/teacher') && allowed !== '/teacher') {
        router.replace(allowed);
        return;
      }
      if (pathname.startsWith('/student') && allowed !== '/student') {
        router.replace(allowed);
        return;
      }
    }
  }, [loading, firebaseUser, profile, onboardingRequired, pathname, router]);

  return null;
}

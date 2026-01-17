# Change Proposal: Role-Based Authentication, Onboarding, and Routing

## Summary

Introduce a role-based authentication and onboarding system that serves as the entry gate for the application. Users authenticate via Google Sign-In, complete onboarding on first login, and are deterministically routed to either the Student or Teacher dashboard on subsequent sessions.

## Motivation

The application supports two distinct personas—Students and Teachers—each with different navigation paths and access boundaries. Without persistent user profiles and role-aware routing, users may experience incorrect navigation, unauthorized access, or repeated setup friction.

This change establishes:

- A single OAuth-based authentication mechanism
- Persistent user profiles stored in Firestore
- First-time onboarding with explicit role selection
- Role-enforced routing and access guards
- Deterministic post-login navigation

## Scope

Included:

- Google OAuth authentication via Firebase
- Firestore-backed user profiles keyed by Auth UID
- First-time onboarding flow for profile completion
- Role-based dashboard routing
- Client-side role guards
- Backend validation for profile creation
- Test-only authentication helpers for E2E testing

Excluded:

- Role changes after onboarding
- External identity verification (e.g., institutional directories)
- Multi-role or admin users
- Server-side authorization beyond profile validation

## User-Facing Behavior

- All users sign in using Google Sign-In.
- If no user profile exists (or is incomplete), the user is redirected to onboarding.
- Onboarding collects role, department, and courses.
- After onboarding, users are routed to a role-specific dashboard.
- Returning users bypass onboarding and are routed directly after login.
- Users attempting to access routes outside their role are redirected to their permitted dashboard.

## Routing Guarantees

- Unauthenticated users are redirected to `/login`.
- Authenticated users without completed profiles are redirected to `/onboarding`.
- Authenticated users with completed profiles are routed based on `profile.role`.
- Role mismatches trigger automatic correction redirects.

## Impact

- Introduces a persistent `users/{uid}` profile contract.
- Establishes role-based navigation as a foundational system invariant.
- All future features assume authenticated users have completed profiles.

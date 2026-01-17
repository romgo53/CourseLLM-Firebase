# Implementation Tasks

## Authentication

- [x] Configure Firebase Auth with Google provider
- [x] Implement popup sign-in with redirect fallback
- [x] Implement global auth state listener
- [x] Support sign-out and session reset

## Profile Management

- [x] Define Firestore `users/{uid}` profile schema
- [x] Load profile on auth state resolution
- [x] Detect incomplete or missing profiles
- [x] Enforce profile completeness rules (role, department, courses)

## Onboarding

- [x] Implement onboarding UI for first-time users
- [x] Validate onboarding inputs client-side
- [x] Persist onboarding data to Firestore
- [x] Ensure idempotent profile creation
- [x] Recover users who exit onboarding mid-flow

## Routing & Guards

- [x] Implement global auth redirector for neutral routes
- [x] Implement role-based client route guards
- [x] Enforce role-correct dashboard access
- [x] Prevent unauthorized role access via redirects

## UX & Resilience

- [x] Display loading state during auth/profile resolution
- [x] Avoid UI flashing during redirects
- [x] Handle popup blocking and network failures gracefully

## Testing

- [x] Add test-only custom token auth route (dev/test only)
- [x] Add test sign-in client for E2E flows
- [x] Implement Playwright tests for auth scenarios

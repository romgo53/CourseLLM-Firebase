# Architecture Spec: auth-login-llm

This document describes the APIs and components for the login authentication.
Scope: Google sign-in, profile onboarding, and role-based routing for student/teacher dashboards.

## High-level flow
1) User lands on `/` which redirects to `/login`.
2) User signs in with Google.
3) Auth state loads and Firestore profile is fetched.
4) If profile is missing/incomplete, user is sent to `/onboarding`.
5) After onboarding, user is routed to `/student` or `/teacher`.

## Component diagram (logical)
```
┌──────────────────────────────┐
│            Client            │
│  Next.js App Router + UI     │
└──────────────┬───────────────┘
               │
               │ uses
               ▼
┌──────────────────────────────┐
│  AuthProviderClient          │
│  - Auth state                │
│  - Profile fetch             │
└──────────────┬───────────────┘
               │
     ┌─────────┴─────────┐
     │                   │
     ▼                   ▼
┌──────────────┐   ┌────────────────┐
│ Firebase Auth│   │ Firestore users│
└──────────────┘   └────────────────┘
               ▲
               │
┌──────────────┴───────────────┐
│ AuthRedirector / RoleGuard   │
│ - route to onboarding        │
│ - enforce student/teacher    │
└──────────────────────────────┘
```

## Auth flow (sequence)
```
User -> /login
Login -> Firebase Auth (Google sign-in)
AuthProviderClient -> Firebase Auth (onAuthStateChanged)
AuthProviderClient -> Firestore users/{uid} (getDoc)
AuthRedirector:
  - if profile missing -> /onboarding
  - else -> /student or /teacher
Onboarding -> Firestore users/{uid} (setDoc)
RoleGuardClient -> allow or redirect based on role
```

## Components
- **Next.js App Router shell**: `src/app/layout.tsx` wraps the app with auth context and redirect logic.
- **Auth context**: `src/components/AuthProviderClient.tsx` subscribes to Firebase Auth and loads the user profile from Firestore.
- **Auth service**: `src/lib/authService.ts` performs Google sign-in (popup with redirect fallback) and sign-out.
- **Firebase client**: `src/lib/firebase.ts` initializes Firebase Auth + Firestore and enables offline persistence.
- **Redirector**: `src/components/AuthRedirector.tsx` moves users from neutral pages to onboarding or dashboards.
- **Role guard**: `src/components/RoleGuardClient.tsx` enforces `/student` and `/teacher` access.
- **Login UI**: `src/app/login/page.tsx` signs in and routes new users to onboarding.
- **Onboarding UI**: `src/app/onboarding/page.tsx` collects role/department/courses and writes `users/{uid}`.
- **Dashboards**: `src/app/student/*` and `src/app/teacher/*` (with shared app shell in `src/components/InnerAppShellClient.tsx`).

## APIs
### Firebase Auth (client)
- **Provider**: Google (popup; redirect fallback if popup blocked).
- **Used by**: `src/lib/authService.ts`, `src/components/AuthProviderClient.tsx`, `src/app/login/page.tsx`.

### Firestore (client)
- **Collection**: `users/{uid}`
- **Reads**: `src/components/AuthProviderClient.tsx`
- **Writes**: `src/app/onboarding/page.tsx`

### Test-only API (server)
- **Route**: `GET /api/test-token`
- **File**: `src/app/api/test-token/route.ts`
- **Guard**: `ENABLE_TEST_AUTH=true`
- **Purpose**: Generates a Firebase custom token (and optionally a profile) for automated tests.

### Test sign-in page (client)
- **Route**: `/test/signin?token=...`
- **File**: `src/app/test/signin/page.tsx`
- **Purpose**: Consumes a custom token, then redirects into the normal auth flow.

## Data model (Firestore)
### users/{uid}
- `uid` (string)
- `email` (string)
- `displayName` (string, optional)
- `photoURL` (string, optional)
- `role` ("student" | "teacher")
- `department` (string)
- `courses` (string[])
- `authProviders` (string[])
- `profileComplete` (boolean)
- `createdAt`, `updatedAt` (server timestamps)

## Security rules
Defined in `firestore.rules`:
- `users/{uid}` can only be read/written by the authenticated user with the same UID.
- `courses` and `departments` collections are read-only (if present).

## Configuration
Environment variables required (see `.env.local.example`):
- `NEXT_PUBLIC_FIREBASE_API_KEY`
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID`
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`
- `NEXT_PUBLIC_FIREBASE_APP_ID`

Test-only variables:
- `ENABLE_TEST_AUTH=true`
- `FIREBASE_SERVICE_ACCOUNT_JSON` or `FIREBASE_SERVICE_ACCOUNT_PATH`

## Runtime entry points
- Dev server: `npm run dev` (Next.js on port 9002)
- Main pages: `/login`, `/onboarding`, `/student`, `/teacher`

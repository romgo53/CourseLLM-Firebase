# Design Notes: Authentication & Routing

## Auth Model

Authentication is delegated to Firebase Auth using Google OAuth. The application treats Firebase Auth as the identity source and Firestore as the profile authority.

## Profile Contract

Each authenticated user is associated with exactly one Firestore profile document keyed by Auth UID. A profile is considered complete only when required fields are present.

## Role Assignment

Roles are selected once during onboarding and treated as immutable to prevent privilege escalation. The system assumes honest self-identification for the current scope.

## Routing Strategy

Routing decisions are resolved client-side after both auth state and profile state are known. A global redirector prevents intermediate UI states and incorrect flashes.

## Testing Strategy

OAuth flows are not automated directly. Instead, custom Firebase tokens are used in test environments to ensure deterministic and fast end-to-end testing without reliance on external providers.

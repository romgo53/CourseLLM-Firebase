# Change Proposal: DSPy Topic Intelligence Service

## Summary

Introduce a secured backend service that performs topic extraction, topic-tree generation, topic-tree updates, and material-to-topic matching using DSPy-powered language models. The service is protected by Firebase authentication and enforces role-based access control.

## Motivation

The application requires structured semantic understanding of course materials to support downstream features such as topic graphs, adaptive tutoring, and analytics. This change provides a dedicated microservice capable of extracting, organizing, and matching educational topics from uploaded content in a consistent and reusable manner.

## Scope

Included:

- A FastAPI-based microservice for topic intelligence
- DSPy modules for topic extraction and hierarchical modeling
- Firebase-based authentication and token verification
- Role-based access enforcement (`student`, `teacher`)
- File-based markdown ingestion
- Topic tree HTML rendering utility
- Test-only authentication bypass for local and E2E testing

Excluded:

- Persistent storage of topics or trees
- Course-to-topic database integration
- Authorization beyond role validation
- Frontend UI integration

## User-Facing Behavior

- Authenticated users can upload markdown files to extract topics.
- Users can request hierarchical topic trees derived from extracted topics.
- Existing topic trees can be incrementally updated with new topics.
- Uploaded materials can be matched against a predefined topic set.
- Requests without valid authentication tokens are rejected.
- Requests with invalid or missing roles are rejected.

## Security Model

- All protected endpoints require a valid Firebase ID token.
- Tokens are verified server-side using Firebase Admin SDK.
- User roles are derived from Firebase custom claims.
- Only users with roles `student` or `teacher` are authorized.
- A test authentication token may be enabled explicitly for local/testing use.

## Impact

- Introduces a new backend intelligence service.
- Establishes a reusable contract for topic-based reasoning.
- Provides a foundation for topic graphs, RAG pipelines, and analytics.

# Implementation Tasks

## Service Setup

- [x] Initialize FastAPI application
- [x] Configure service settings via environment variables
- [x] Add health check endpoint

## Authentication & Authorization

- [x] Initialize Firebase Admin SDK
- [x] Verify Firebase ID tokens on each request
- [x] Support test authentication token for local testing
- [x] Extract user role from Firebase custom claims
- [x] Enforce role-based access to endpoints

## DSPy Integration

- [x] Configure DSPy language model provider
- [x] Implement topic extraction signature
- [x] Implement topic tree generation signature
- [x] Implement topic tree update signature
- [x] Implement material-to-topic matching signature

## API Endpoints

- [x] `/extract` — extract topics from uploaded markdown
- [x] `/topic_tree` — generate hierarchical topic tree
- [x] `/update_topic_tree` — merge new topics into an existing tree
- [x] `/match` — match material against known topics
- [x] `/test_auth` — validate authentication and role handling

## File Handling

- [x] Accept uploaded markdown files
- [x] Load and parse markdown content
- [x] Manage temporary file storage

## Models & Data Contracts

- [x] Define Topic and TopicTree data models
- [x] Include topic metadata (confidence, sources)

## Tooling

- [x] Implement standalone HTML renderer for topic trees

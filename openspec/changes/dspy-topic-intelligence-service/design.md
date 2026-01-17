# Design Notes: DSPy Topic Intelligence Service

## Architecture

The service is implemented as a standalone FastAPI microservice to isolate AI-driven processing from frontend and core application logic.

## Authentication Strategy

Firebase Authentication is used as the identity provider. Authorization is enforced by extracting custom role claims from verified ID tokens.

## Role Enforcement

The service treats `student` and `teacher` as valid roles. Requests lacking a valid role are rejected early to prevent misuse.

## DSPy Usage

DSPy signatures are used to define deterministic input/output contracts for topic-related reasoning. This allows the LLM to be treated as a structured component rather than free-form text generation.

## File-Based Processing

Uploaded markdown files are processed synchronously and are not persisted beyond request scope. Temporary storage is used for compatibility with existing file loaders.

## Testing Support

A test-only authentication token path is provided to allow deterministic local and E2E testing without Firebase client flows. This mechanism is explicitly disabled by default.

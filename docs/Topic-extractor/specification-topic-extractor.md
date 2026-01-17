# Specification: topic-extractor

This spec defines where the topic extractor fits in the product workflow, how it is integrated in this repo, how to verify it, and the API contract.
It complements `docs/architecture-topic-extractor.md`.

## Workflow placement
- Teacher manages a course and uploads materials (MD/PDF/PPT/DOC).
- The system extracts topics from the uploaded content.
- Topics feed into learning objectives, assessments, and student-facing views.

Current status in this repo:
- The topic extractor service exists, but no frontend or backend integration is wired to it.
- The teacher UI uses mock data and does not call any upload or extraction API yet.

## Integration in this project
- Microservice code: `services/topics_extractor/*` (FastAPI + DSPy).
- Auth is based on Firebase ID tokens with custom claims for `role`.
- There is no Next.js API route or client call to this service yet.
- Data storage for extracted topics is not implemented in this repo.

## React components (current touchpoints)
These are the likely integration points; none are wired to the extractor yet.
- `src/app/teacher/courses/page.tsx` (course list entry to manage materials)
- `src/app/teacher/courses/[courseId]/page.tsx` (course management shell)
- `src/app/teacher/courses/[courseId]/_components/course-management-client.tsx` (file input for materials)
- `src/app/student/courses/[courseId]/page.tsx` (materials view for students)
- `src/app/student/courses/[courseId]/_components/chat-panel.tsx` (potential consumer of topic context)

## Verification
Manual checks (current):
1) Start the service locally (see `services/topics_extractor/README.md`).
2) `GET /health` returns `{ "status": "ok" }`.
3) `GET /test_auth` with `Authorization: Bearer <TEST_AUTH_TOKEN>` returns a role.
4) `POST /extract` with a Markdown file returns `topics`.
5) `POST /topic_tree` with a Markdown file returns `topic_tree`.
6) `POST /update_topic_tree` with a sample tree and topics returns `updated_topic_tree`.


## Api Specifications
```json
{
    "openapi": "3.1.0",
    "info": {
        "title": "DSPy Topic Extractor",
        "version": "0.1.0"
    },
    "paths": {
        "/extract": {
            "post": {
                "summary": "Topics",
                "description": "Extract topics from uploaded markdown file",
                "operationId": "topics_extract_post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_topics_extract_post"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "HTTPBearer": []
                    }
                ]
            }
        },
        "/topic_tree": {
            "post": {
                "summary": "Topic Tree",
                "description": "Generate a topic tree from uploaded markdown file",
                "operationId": "topic_tree_topic_tree_post",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_topic_tree_topic_tree_post"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "HTTPBearer": []
                    }
                ]
            }
        },
        "/update_topic_tree": {
            "post": {
                "summary": "Update Tree",
                "description": "Update an existing topic tree with new topics",
                "operationId": "update_tree_update_topic_tree_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_update_tree_update_topic_tree_post"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "HTTPBearer": []
                    }
                ]
            }
        },
        "/test_auth": {
            "get": {
                "summary": "Test Auth",
                "description": "Test authentication and return the user's role",
                "operationId": "test_auth_test_auth_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "security": [
                    {
                        "HTTPBearer": []
                    }
                ]
            }
        },
        "/health": {
            "get": {
                "summary": "Health",
                "description": "Check the health status of the service",
                "operationId": "health_health_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/sentry-debug": {
            "get": {
                "summary": "Trigger Error",
                "operationId": "trigger_error_sentry_debug_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Body_topic_tree_topic_tree_post": {
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "title": "File"
                    }
                },
                "type": "object",
                "required": [
                    "file"
                ],
                "title": "Body_topic_tree_topic_tree_post"
            },
            "Body_topics_extract_post": {
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "title": "File"
                    }
                },
                "type": "object",
                "required": [
                    "file"
                ],
                "title": "Body_topics_extract_post"
            },
            "Body_update_tree_update_topic_tree_post": {
                "properties": {
                    "topics": {
                        "items": {
                            "$ref": "#/components/schemas/Topic"
                        },
                        "type": "array",
                        "title": "Topics"
                    },
                    "existing_tree": {
                        "$ref": "#/components/schemas/TopicTree"
                    }
                },
                "type": "object",
                "required": [
                    "topics",
                    "existing_tree"
                ],
                "title": "Body_update_tree_update_topic_tree_post"
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        },
                        "type": "array",
                        "title": "Detail"
                    }
                },
                "type": "object",
                "title": "HTTPValidationError"
            },
            "Topic": {
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Name"
                    },
                    "description": {
                        "anyOf": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Description"
                    },
                    "metadata": {
                        "anyOf": [
                            {
                                "$ref": "#/components/schemas/TopicMetadata"
                            },
                            {
                                "type": "null"
                            }
                        ]
                    }
                },
                "type": "object",
                "required": [
                    "name"
                ],
                "title": "Topic",
                "description": "Model representing a topic."
            },
            "TopicMetadata": {
                "properties": {
                    "source_files": {
                        "anyOf": [
                            {
                                "items": {
                                    "type": "string"
                                },
                                "type": "array"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Source Files"
                    },
                    "confidence_score": {
                        "anyOf": [
                            {
                                "type": "number"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Confidence Score"
                    },
                    "source_sections": {
                        "anyOf": [
                            {
                                "items": {
                                    "type": "string"
                                },
                                "type": "array"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Source Sections"
                    }
                },
                "type": "object",
                "title": "TopicMetadata",
                "description": "Model representing metadata for a topic."
            },
            "TopicTree": {
                "properties": {
                    "topic": {
                        "$ref": "#/components/schemas/Topic"
                    },
                    "subtopics": {
                        "anyOf": [
                            {
                                "items": {
                                    "$ref": "#/components/schemas/TopicTree"
                                },
                                "type": "array"
                            },
                            {
                                "type": "null"
                            }
                        ],
                        "title": "Subtopics"
                    }
                },
                "type": "object",
                "required": [
                    "topic"
                ],
                "title": "TopicTree",
                "description": "Model representing a hierarchical topic tree."
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {
                            "anyOf": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "integer"
                                }
                            ]
                        },
                        "type": "array",
                        "title": "Location"
                    },
                    "msg": {
                        "type": "string",
                        "title": "Message"
                    },
                    "type": {
                        "type": "string",
                        "title": "Error Type"
                    }
                },
                "type": "object",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "title": "ValidationError"
            }
        },
        "securitySchemes": {
            "HTTPBearer": {
                "type": "http",
                "scheme": "bearer"
            }
        }
    }
}
```
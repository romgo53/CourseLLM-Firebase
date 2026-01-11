from pydantic import BaseModel

class TopicMetadata(BaseModel):
    """Model representing metadata for a topic."""

    source_files: list[str] | None = None
    confidence_score: float | None = None
    source_sections: list[str] | None = None
    summary: str | None = None

class Topic(BaseModel):
    """Model representing a topic."""
    name: str
    description: str | None = None
    metadata: TopicMetadata | None = None



class TopicTree(BaseModel):
    """Model representing a hierarchical topic tree."""

    topic: Topic
    subtopics: list["TopicTree"] | None = None
"""Utilities for loading markdown files."""

def load_markdown_file(file_path: str) -> str:
    """Load a markdown file and return its text content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to load markdown file {file_path}: {e}")

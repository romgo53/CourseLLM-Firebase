

## Load Markdown Files from given path and return text content
def load_markdown_file(file_path: str) -> str:
    """Load a markdown file and return its text content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise RuntimeError(f"Failed to load markdown file {file_path}: {e}")

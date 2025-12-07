# fetch files from file store 
from typing import List, Dict
from file_store_client import FileStoreClient

def fetch_markdown_files(file_ids: List[str]) -> Dict[str, str]:
    """
    Fetch markdown files from the file store given their IDs.
    
    Args:
        file_ids (List[str]): List of file IDs to fetch.
    Returns:
        Dict[str, str]: A dictionary mapping file IDs to their text content.
    """ 
    client = FileStoreClient()
    files_content = {}
    for file_id in file_ids:
        try:
            content = client.get_file_content(file_id)
            files_content[file_id] = content
        except Exception as e:
            print(f"Error fetching file {file_id}: {e}")
    return files_content
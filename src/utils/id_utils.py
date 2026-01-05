"""
ID generation utilities.
"""
import uuid


def generate_id() -> str:
    """
    Generate a UUIDv4 string for use as a primary key.
    
    Returns:
        String representation of UUIDv4
    """
    return str(uuid.uuid4())

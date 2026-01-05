"""
Time and timestamp generation utilities.
"""
from datetime import datetime, timedelta
import random


def random_past_timestamp(days_ago_min: int = 365, days_ago_max: int = 1) -> str:
    """
    Generate a random timestamp in the past.
    
    Args:
        days_ago_min: Minimum days in the past
        days_ago_max: Maximum days in the past (most recent)
    
    Returns:
        ISO 8601 formatted timestamp string
    """
    days_ago = random.randint(days_ago_max, days_ago_min)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    
    timestamp = datetime.now() - timedelta(days=days_ago, hours=hours, minutes=minutes, seconds=seconds)
    return timestamp.isoformat()


def random_timestamp_after(after: str, max_days_later: int = 30) -> str:
    """
    Generate a random timestamp after a given timestamp.
    
    Args:
        after: ISO 8601 timestamp string
        max_days_later: Maximum days after the given timestamp
    
    Returns:
        ISO 8601 formatted timestamp string
    """
    start = datetime.fromisoformat(after)
    days_later = random.randint(0, max_days_later)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    
    timestamp = start + timedelta(days=days_later, hours=hours, minutes=minutes, seconds=seconds)
    return timestamp.isoformat()


def random_due_date(created_at: str, overdue_chance: float = 0.2) -> str:
    """
    Generate a random due date relative to creation date.
    May be in the past (overdue) based on overdue_chance.
    
    Args:
        created_at: ISO 8601 timestamp string of task creation
        overdue_chance: Probability (0-1) that the task is overdue
    
    Returns:
        ISO 8601 formatted date string (date only, no time)
    """
    start = datetime.fromisoformat(created_at)
    
    if random.random() < overdue_chance:
        # Make it overdue: due date is before today
        days_until_due = random.randint(-30, -1)
    else:
        # Not overdue: due date is in the future or today
        days_until_due = random.randint(1, 60)
    
    due_date = start + timedelta(days=days_until_due)
    return due_date.date().isoformat()


def maybe_completed_at(created_at: str, due_date: str = None, completion_rate: float = 0.7) -> str:
    """
    Generate a completion timestamp or None based on completion rate.
    If completed, ensures completed_at > created_at.
    
    Args:
        created_at: ISO 8601 timestamp string
        due_date: Optional due date (ISO format)
        completion_rate: Probability (0-1) that task is completed
    
    Returns:
        ISO 8601 timestamp string or None
    """
    if random.random() > completion_rate:
        return None
    
    # Task is completed
    start = datetime.fromisoformat(created_at)
    
    if due_date:
        # Complete within reasonable time after creation, possibly after due date
        max_days = 90
    else:
        max_days = 60
    
    days_later = random.randint(1, max_days)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)
    
    completed = start + timedelta(days=days_later, hours=hours, minutes=minutes, seconds=seconds)
    return completed.isoformat()

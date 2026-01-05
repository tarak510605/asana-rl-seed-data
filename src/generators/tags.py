"""
Generate tags for organization.
"""
import sqlite3
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_tags(conn: sqlite3.Connection, count: int = 15) -> List[Dict[str, str]]:
    """
    Generate tags and insert into database.
    
    Args:
        conn: SQLite connection
        count: Number of tags to create
    
    Returns:
        List of dictionaries with tag info (id, name)
    """
    cursor = conn.cursor()
    tags = []
    
    # Common tags in project management
    tag_names = [
        "bug",
        "feature",
        "enhancement",
        "urgent",
        "high-priority",
        "low-priority",
        "documentation",
        "design",
        "backend",
        "frontend",
        "mobile",
        "api",
        "security",
        "performance",
        "tech-debt",
        "refactoring",
        "testing",
        "blocked",
        "needs-review",
        "customer-request",
        "internal",
        "ui/ux",
        "accessibility",
        "infrastructure",
        "deployment",
    ]
    
    # Use only the specified count
    selected_tags = tag_names[:min(count, len(tag_names))]
    
    for tag_name in selected_tags:
        tag_id = generate_id()
        created_at = random_past_timestamp(days_ago_min=365, days_ago_max=180)
        
        cursor.execute("""
            INSERT INTO tags (tag_id, name, created_at)
            VALUES (?, ?, ?)
        """, (tag_id, tag_name, created_at))
        
        tags.append({
            'id': tag_id,
            'name': tag_name
        })
    
    conn.commit()
    print(f"✓ Created {len(tags)} tag(s)")
    return tags


def generate_task_tag_associations(conn: sqlite3.Connection, tasks: List[Dict], 
                                   tags: List[Dict]) -> int:
    """
    Generate associations between tasks and tags.
    
    Args:
        conn: SQLite connection
        tasks: List of task dictionaries
        tags: List of tag dictionaries
    
    Returns:
        Number of associations created
    """
    import random
    
    cursor = conn.cursor()
    associations = 0
    
    tag_ids = [t['id'] for t in tags]
    
    for task in tasks:
        task_id = task['id']
        
        # 60% of tasks have tags
        if random.random() > 0.6:
            continue
        
        # Tasks typically have 1-3 tags
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tag_ids, min(num_tags, len(tag_ids)))
        
        for tag_id in selected_tags:
            assigned_at = random_past_timestamp(days_ago_min=150, days_ago_max=1)
            
            cursor.execute("""
                INSERT INTO task_tag_associations (task_id, tag_id, assigned_at)
                VALUES (?, ?, ?)
            """, (task_id, tag_id, assigned_at))
            
            associations += 1
    
    conn.commit()
    print(f"✓ Created {associations} task-tag association(s)")
    return associations

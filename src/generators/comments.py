"""
Generate comments on tasks.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_timestamp_after


def generate_comments(conn: sqlite3.Connection, tasks: List[Dict], users: List[Dict],
                     avg_comments_per_task: float = 1.5) -> List[Dict[str, str]]:
    """
    Generate comments for tasks and insert into database.
    
    Args:
        conn: SQLite connection
        tasks: List of task dictionaries
        users: List of user dictionaries
        avg_comments_per_task: Average number of comments per task
    
    Returns:
        List of dictionaries with comment info (id, task_id, user_id, content)
    """
    cursor = conn.cursor()
    comments = []
    
    # Realistic comment templates
    comment_templates = [
        "This looks good to me, approved!",
        "Can we discuss this in tomorrow's standup?",
        "I've made some changes, please review.",
        "Blocked on the API integration.",
        "Need clarification on requirements.",
        "Great work! Shipped to production.",
        "Found an edge case we need to handle.",
        "Testing completed successfully.",
        "Added to sprint backlog.",
        "Reassigning to {name} for review.",
        "Updated based on feedback.",
        "This is urgent, prioritizing now.",
        "Waiting on design mockups.",
        "Dependencies have been updated.",
        "Documentation is complete.",
        "Let's break this into smaller tasks.",
        "Related to ticket #{number}.",
        "Performance looks good after optimization.",
        "Security review passed.",
        "Merged PR, closing task.",
    ]
    
    user_ids = [u['id'] for u in users]
    user_names = {u['id']: f"{u['first_name']} {u['last_name']}" for u in users}
    
    for task in tasks:
        task_id = task['id']
        task_created_at = task['created_at']
        
        # Some tasks have no comments, some have many
        # Use Poisson-like distribution
        if random.random() < 0.3:
            # No comments
            num_comments = 0
        elif random.random() < 0.7:
            # 1-2 comments
            num_comments = random.randint(1, 2)
        else:
            # 3-8 comments
            num_comments = random.randint(3, 8)
        
        # Track when last comment was made
        last_comment_time = task_created_at
        
        for i in range(num_comments):
            comment_id = generate_id()
            user_id = random.choice(user_ids)
            
            # Pick comment template
            template = random.choice(comment_templates)
            
            # Fill in template placeholders
            if "{name}" in template:
                random_name = random.choice(list(user_names.values()))
                content = template.format(name=random_name)
            elif "{number}" in template:
                content = template.format(number=random.randint(100, 999))
            else:
                content = template
            
            # Comments are created after the previous comment
            created_at = random_timestamp_after(last_comment_time, max_days_later=15)
            last_comment_time = created_at
            
            cursor.execute("""
                INSERT INTO comments (comment_id, task_id, author_id, body, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (comment_id, task_id, user_id, content, created_at))
            
            comments.append({
                'id': comment_id,
                'task_id': task_id,
                'author_id': user_id,
                'body': content
            })
    
    conn.commit()
    print(f"✓ Created {len(comments)} comment(s)")
    return comments

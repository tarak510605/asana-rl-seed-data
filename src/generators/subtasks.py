"""
Generate subtasks for tasks.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_timestamp_after, maybe_completed_at


def generate_subtasks(conn: sqlite3.Connection, tasks: List[Dict], 
                      subtask_probability: float = 0.3) -> List[Dict[str, str]]:
    """
    Generate subtasks for tasks and insert into database.
    Not all tasks have subtasks.
    
    Args:
        conn: SQLite connection
        tasks: List of task dictionaries
        subtask_probability: Probability that a task has subtasks
    
    Returns:
        List of dictionaries with subtask info (id, title, parent_task_id)
    """
    cursor = conn.cursor()
    subtasks = []
    
    # Subtask title templates
    subtask_templates = [
        "Research approach",
        "Create design mockup",
        "Write unit tests",
        "Update documentation",
        "Code review",
        "QA testing",
        "Deploy to staging",
        "Get stakeholder approval",
        "Update dependencies",
        "Refactor code",
        "Add error handling",
        "Performance testing",
        "Security review",
        "Write changelog",
        "Update API docs",
    ]
    
    for task in tasks:
        # Skip if task doesn't have subtasks
        if random.random() > subtask_probability:
            continue
        
        task_id = task['id']
        task_created_at = task['created_at']
        task_completed = task['completed_at'] is not None
        
        # Tasks with subtasks typically have 2-5 subtasks
        num_subtasks = random.randint(2, 5)
        
        for i in range(num_subtasks):
            subtask_id = generate_id()
            name = random.choice(subtask_templates)
            
            # Subtask created after parent task
            created_at = random_timestamp_after(task_created_at, max_days_later=10)
            
            # Some subtasks have assignees (50% chance)
            assignee_id = task.get('assignee_id') if random.random() < 0.5 else None
            
            # If parent task is completed, most subtasks should be completed too
            if task_completed:
                completion_rate = 0.9
            else:
                completion_rate = 0.5
            
            completed_at = maybe_completed_at(created_at, completion_rate=completion_rate)
            completed = 1 if completed_at else 0
            
            cursor.execute("""
                INSERT INTO subtasks (subtask_id, parent_task_id, assignee_id, name, completed, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (subtask_id, task_id, assignee_id, name, completed, created_at, completed_at))
            
            subtasks.append({
                'id': subtask_id,
                'name': name,
                'parent_task_id': task_id
            })
    
    conn.commit()
    print(f"✓ Created {len(subtasks)} subtask(s)")
    return subtasks

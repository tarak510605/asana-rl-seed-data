"""
Generate tasks within sections/projects.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp, random_due_date, maybe_completed_at


def generate_tasks(conn: sqlite3.Connection, projects: List[Dict], sections: List[Dict], 
                   users: List[Dict], tasks_per_project: int = 15) -> List[Dict[str, str]]:
    """
    Generate tasks for projects and insert into database.
    
    Args:
        conn: SQLite connection
        projects: List of project dictionaries
        sections: List of section dictionaries
        users: List of user dictionaries
        tasks_per_project: Average number of tasks per project
    
    Returns:
        List of dictionaries with task info (id, title, project_id, assignee_id, etc.)
    """
    cursor = conn.cursor()
    tasks = []
    
    # Task title templates
    task_templates = [
        "Implement {} feature",
        "Fix bug in {}",
        "Review {} documentation",
        "Test {} functionality",
        "Design {} interface",
        "Refactor {} module",
        "Update {} configuration",
        "Deploy {} to production",
        "Optimize {} performance",
        "Research {} solution",
        "Write tests for {}",
        "Create {} mockups",
        "Analyze {} metrics",
        "Set up {} integration",
        "Document {} API",
        "Migrate {} database",
        "Improve {} UX",
        "Add {} validation",
        "Configure {} monitoring",
        "Prepare {} presentation",
    ]
    
    components = [
        "authentication", "dashboard", "API", "database", "frontend", "backend",
        "payment system", "user profile", "search", "notifications", "reports",
        "admin panel", "mobile app", "analytics", "settings", "workflow",
        "integration", "permissions", "logging", "caching", "email system"
    ]
    
    priorities = ["low", "medium", "high", "urgent"]
    priority_weights = [2, 4, 3, 1]  # More medium/high tasks
    
    for project in projects:
        project_id = project['id']
        
        # Get sections for this project
        project_sections = [s for s in sections if s['project_id'] == project_id]
        if not project_sections:
            continue
        
        # Get team users for assignment
        cursor.execute("""
            SELECT DISTINCT u.user_id
            FROM users u
            JOIN team_memberships tm ON u.user_id = tm.user_id
            JOIN teams t ON tm.team_id = t.team_id
            JOIN projects p ON t.team_id = p.team_id
            WHERE p.project_id = ?
        """, (project_id,))
        project_user_ids = [row[0] for row in cursor.fetchall()]
        
        if not project_user_ids:
            continue
        
        num_tasks = random.randint(max(5, tasks_per_project - 5), tasks_per_project + 5)
        
        for i in range(num_tasks):
            task_id = generate_id()
            
            # Generate task name
            template = random.choice(task_templates)
            component = random.choice(components)
            name = template.format(component)
            
            # Optional description for some tasks
            description = f"Details for {name}" if random.random() < 0.3 else None
            
            # Random section
            section_id = random.choice(project_sections)['id']
            
            # 20% chance task is unassigned
            if random.random() < 0.2:
                assignee_id = None
            else:
                assignee_id = random.choice(project_user_ids)
            
            created_at = random_past_timestamp(days_ago_min=200, days_ago_max=1)
            
            # 70% of tasks have due dates
            if random.random() < 0.7:
                due_date = random_due_date(created_at, overdue_chance=0.2)
            else:
                due_date = None
            
            # 70% completion rate
            completed_at = maybe_completed_at(created_at, due_date, completion_rate=0.7)
            completed = 1 if completed_at else 0
            
            cursor.execute("""
                INSERT INTO tasks (task_id, project_id, section_id, assignee_id, name, 
                                 description, due_date, completed, created_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, project_id, section_id, assignee_id, name, 
                  description, due_date, completed, created_at, completed_at))
            
            tasks.append({
                'id': task_id,
                'name': name,
                'project_id': project_id,
                'section_id': section_id,
                'assignee_id': assignee_id,
                'created_at': created_at,
                'completed_at': completed_at
            })
    
    conn.commit()
    print(f"✓ Created {len(tasks)} task(s)")
    return tasks

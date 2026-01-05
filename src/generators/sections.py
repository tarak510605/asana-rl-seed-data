"""
Generate sections within projects.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_sections(conn: sqlite3.Connection, projects: List[Dict]) -> List[Dict[str, str]]:
    """
    Generate sections for projects and insert into database.
    
    Args:
        conn: SQLite connection
        projects: List of project dictionaries
    
    Returns:
        List of dictionaries with section info (id, name, project_id)
    """
    cursor = conn.cursor()
    sections = []
    
    # Common section names in project management
    section_names = [
        "To Do",
        "In Progress",
        "In Review",
        "Done",
        "Backlog",
        "Blocked",
        "Ready for Testing",
        "Planning",
        "Research",
        "Design",
        "Development",
        "Testing",
        "Deployment",
    ]
    
    for project in projects:
        project_id = project['id']
        
        # Each project gets 3-6 sections
        num_sections = random.randint(3, 6)
        project_sections = random.sample(section_names, min(num_sections, len(section_names)))
        
        for position, section_name in enumerate(project_sections):
            section_id = generate_id()
            
            cursor.execute("""
                INSERT INTO sections (section_id, project_id, name, position)
                VALUES (?, ?, ?, ?)
            """, (section_id, project_id, section_name, position))
            
            sections.append({
                'id': section_id,
                'name': section_name,
                'project_id': project_id
            })
    
    conn.commit()
    print(f"✓ Created {len(sections)} section(s)")
    return sections

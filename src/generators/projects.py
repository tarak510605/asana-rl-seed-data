"""
Generate projects for teams.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_projects(conn: sqlite3.Connection, teams: List[Dict], users: List[Dict], 
                     projects_per_team: int = 3) -> List[Dict[str, str]]:
    """
    Generate projects for teams and insert into database.
    
    Args:
        conn: SQLite connection
        teams: List of team dictionaries
        users: List of user dictionaries
        projects_per_team: Average number of projects per team
    
    Returns:
        List of dictionaries with project info (id, name, team_id, owner_id)
    """
    cursor = conn.cursor()
    projects = []
    
    # Project name templates
    project_templates = [
        "Q{} Planning",
        "{} Product Launch",
        "{} Marketing Campaign",
        "Website Redesign {}",
        "{} Integration Project",
        "Customer Onboarding {}",
        "{} Feature Development",
        "Bug Fixes - {}",
        "Infrastructure Upgrade {}",
        "Sales Enablement {}",
        "{} Documentation",
        "Mobile App - {}",
        "API Development {}",
        "Security Audit {}",
        "Performance Optimization {}",
    ]
    
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    years = ["2024", "2025", "2026"]
    descriptors = ["Sprint", "Phase 1", "Phase 2", "v1.0", "v2.0", "Alpha", "Beta", "Pilot"]
    
    # Project types with realistic distribution
    project_types = ["product", "marketing", "operations", "initiative", "campaign", "infrastructure"]
    
    for team in teams:
        team_id = team['id']
        
        num_projects = random.randint(max(1, projects_per_team - 1), projects_per_team + 2)
        
        for i in range(num_projects):
            project_id = generate_id()
            
            # Generate project name
            template = random.choice(project_templates)
            if "{}" in template:
                filler = random.choice(quarters + years + descriptors)
                name = template.format(filler)
            else:
                name = template
            
            project_type = random.choice(project_types)
            created_at = random_past_timestamp(days_ago_min=300, days_ago_max=30)
            
            cursor.execute("""
                INSERT INTO projects (project_id, team_id, name, project_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, team_id, name, project_type, created_at))
            
            projects.append({
                'id': project_id,
                'name': name,
                'team_id': team_id,
                'project_type': project_type
            })
    
    conn.commit()
    print(f"✓ Created {len(projects)} project(s)")
    return projects

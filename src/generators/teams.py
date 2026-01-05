"""
Generate teams within organizations.
"""
import sqlite3
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_teams(conn: sqlite3.Connection, org_id: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Generate teams for an organization and insert into database.
    
    Args:
        conn: SQLite connection
        org_id: Organization ID
        count: Number of teams to create
    
    Returns:
        List of dictionaries with team info (id, name, org_id)
    """
    cursor = conn.cursor()
    teams = []
    
    # Typical team names in a B2B SaaS company
    team_names = [
        "Engineering",
        "Product",
        "Marketing",
        "Sales",
        "Customer Success",
        "Design",
        "Operations",
        "Finance",
        "HR",
        "Legal",
    ]
    
    team_types = [
        "engineering",
        "product",
        "marketing",
        "sales",
        "support",
        "design",
        "operations",
        "finance",
        "hr",
        "legal",
    ]
    
    for i in range(count):
        team_id = generate_id()
        name = team_names[i % len(team_names)]
        team_type = team_types[i % len(team_types)]
        created_at = random_past_timestamp(days_ago_min=365, days_ago_max=180)  # 6-12 months ago
        
        cursor.execute("""
            INSERT INTO teams (team_id, organization_id, name, team_type, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (team_id, org_id, name, team_type, created_at))
        
        teams.append({
            'id': team_id,
            'name': name,
            'org_id': org_id
        })
    
    conn.commit()
    print(f"✓ Created {count} team(s)")
    return teams

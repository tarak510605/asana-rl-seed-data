"""
Generate users within an organization.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_users(conn: sqlite3.Connection, org_id: str, count: int = 50) -> List[Dict[str, str]]:
    """
    Generate users for an organization and insert into database.
    Also creates team_memberships to assign users to teams.
    
    Args:
        conn: SQLite connection
        org_id: Organization ID
        count: Number of users to create
    
    Returns:
        List of dictionaries with user info (id, name, email, org_id)
    """
    cursor = conn.cursor()
    users = []
    
    # Fetch existing teams for this organization
    cursor.execute("SELECT team_id FROM teams WHERE organization_id = ?", (org_id,))
    team_ids = [row[0] for row in cursor.fetchall()]
    
    # Common first and last names for realistic user generation
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah",
        "Ian", "Julia", "Kevin", "Laura", "Michael", "Nina", "Oliver", "Patricia",
        "Quinn", "Rachel", "Steve", "Tara", "Uma", "Victor", "Wendy", "Xavier",
        "Yara", "Zachary", "Amy", "Ben", "Claire", "David", "Emma", "Frank",
        "Grace", "Henry", "Iris", "Jack", "Kate", "Liam", "Mia", "Nathan",
        "Olivia", "Paul", "Rosa", "Sam", "Tina", "Ursula", "Vera", "Will", "Zoe"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Walker", "Hall",
        "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams",
        "Nelson", "Carter", "Mitchell", "Roberts", "Turner", "Phillips", "Campbell",
        "Parker", "Evans", "Edwards", "Collins", "Stewart", "Morris", "Rogers", "Reed"
    ]
    
    roles = ["Engineer", "Manager", "Designer", "Analyst", "Coordinator", "Specialist", "Lead", "Director"]
    
    for i in range(count):
        user_id = generate_id()
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@company.com"
        role = random.choice(roles)
        created_at = random_past_timestamp(days_ago_min=365, days_ago_max=30)
        
        cursor.execute("""
            INSERT INTO users (user_id, organization_id, first_name, last_name, email, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, org_id, first_name, last_name, email, role, created_at))
        
        users.append({
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'org_id': org_id
        })
        
        # Assign user to 1-3 teams
        if team_ids:
            num_teams = random.randint(1, min(3, len(team_ids)))
            assigned_teams = random.sample(team_ids, num_teams)
            
            for team_id in assigned_teams:
                membership_id = generate_id()
                cursor.execute("""
                    INSERT INTO team_memberships (membership_id, user_id, team_id, joined_at)
                    VALUES (?, ?, ?, ?)
                """, (membership_id, user_id, team_id, created_at))
    
    conn.commit()
    print(f"✓ Created {count} user(s) with team memberships")
    return users

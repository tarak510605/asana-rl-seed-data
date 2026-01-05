"""
Generate organizations.
"""
import sqlite3
from typing import List
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_organizations(conn: sqlite3.Connection, count: int = 1) -> List[str]:
    """
    Generate organizations and insert into database.
    
    Args:
        conn: SQLite connection
        count: Number of organizations to create (typically 1 for a single company)
    
    Returns:
        List of created organization IDs
    """
    cursor = conn.cursor()
    org_ids = []
    
    # Company names for B2B SaaS companies
    company_names = [
        "Acme Corporation",
        "TechVision Inc",
        "DataFlow Systems",
        "CloudScale Solutions",
        "InnovateLabs",
    ]
    
    # Company domains
    company_domains = [
        "acmecorp.com",
        "techvision.io",
        "dataflow.com",
        "cloudscale.net",
        "innovatelabs.io",
    ]
    
    for i in range(count):
        org_id = generate_id()
        name = company_names[i % len(company_names)] if i < len(company_names) else f"Company {i+1}"
        domain = company_domains[i % len(company_domains)] if i < len(company_domains) else f"company{i+1}.com"
        created_at = random_past_timestamp(days_ago_min=730, days_ago_max=365)  # 1-2 years ago
        
        cursor.execute("""
            INSERT INTO organizations (organization_id, name, domain, created_at)
            VALUES (?, ?, ?, ?)
        """, (org_id, name, domain, created_at))
        
        org_ids.append(org_id)
    
    conn.commit()
    print(f"✓ Created {count} organization(s)")
    return org_ids

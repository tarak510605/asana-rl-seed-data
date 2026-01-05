"""
Generate custom fields for projects.
"""
import sqlite3
import random
from typing import List, Dict
from src.utils.id_utils import generate_id
from src.utils.time_utils import random_past_timestamp


def generate_custom_fields(conn: sqlite3.Connection, projects: List[Dict]) -> List[Dict[str, str]]:
    """
    Generate custom field definitions for projects and their values for tasks.
    
    Args:
        conn: SQLite connection
        projects: List of project dictionaries
    
    Returns:
        List of dictionaries with custom field info (id, name, field_type, project_id)
    """
    cursor = conn.cursor()
    custom_fields = []
    
    # Custom field templates
    field_definitions = [
        {"name": "Story Points", "field_type": "number"},
        {"name": "Sprint", "field_type": "text"},
        {"name": "Epic", "field_type": "text"},
        {"name": "Effort Estimate", "field_type": "number"},
        {"name": "Department", "field_type": "text"},
        {"name": "Severity", "field_type": "text"},
        {"name": "Release Version", "field_type": "text"},
        {"name": "Customer Impact", "field_type": "text"},
        {"name": "Progress", "field_type": "number"},
        {"name": "Cost Center", "field_type": "text"},
    ]
    
    for project in projects:
        project_id = project['id']
        
        # Each project has 2-4 custom fields
        num_fields = random.randint(2, 4)
        selected_fields = random.sample(field_definitions, min(num_fields, len(field_definitions)))
        
        for field_def in selected_fields:
            field_id = generate_id()
            name = field_def['name']
            field_type = field_def['field_type']
            created_at = random_past_timestamp(days_ago_min=250, days_ago_max=50)
            
            cursor.execute("""
                INSERT INTO custom_field_definitions (field_id, project_id, name, field_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (field_id, project_id, name, field_type, created_at))
            
            custom_fields.append({
                'id': field_id,
                'name': name,
                'field_type': field_type,
                'project_id': project_id
            })
    
    conn.commit()
    print(f"✓ Created {len(custom_fields)} custom field definition(s)")
    return custom_fields


def generate_custom_field_values(conn: sqlite3.Connection, custom_fields: List[Dict], 
                                 tasks: List[Dict]) -> int:
    """
    Generate custom field values for tasks.
    
    Args:
        conn: SQLite connection
        custom_fields: List of custom field definition dictionaries
        tasks: List of task dictionaries
    
    Returns:
        Number of custom field values created
    """
    cursor = conn.cursor()
    values_created = 0
    
    # Value templates for different field types
    text_values = {
        "Sprint": ["Sprint 1", "Sprint 2", "Sprint 3", "Sprint 4", "Sprint 5"],
        "Epic": ["User Management", "Payment System", "Analytics Dashboard", "Mobile App", "API v2"],
        "Department": ["Engineering", "Product", "Marketing", "Sales", "Support"],
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Release Version": ["v1.0", "v1.1", "v2.0", "v2.1", "v3.0"],
        "Customer Impact": ["High", "Medium", "Low", "None"],
        "Cost Center": ["R&D", "Operations", "Sales", "Marketing"],
    }
    
    # Group custom fields by project
    fields_by_project = {}
    for field in custom_fields:
        project_id = field['project_id']
        if project_id not in fields_by_project:
            fields_by_project[project_id] = []
        fields_by_project[project_id].append(field)
    
    for task in tasks:
        task_id = task['id']
        project_id = task['project_id']
        
        # Get custom fields for this task's project
        project_fields = fields_by_project.get(project_id, [])
        
        for field in project_fields:
            # 70% of tasks have values for custom fields
            if random.random() > 0.7:
                continue
            
            value_id = generate_id()
            field_id = field['id']
            field_type = field['field_type']
            field_name = field['name']
            
            # Generate appropriate value based on field type
            if field_type == "number":
                if "Points" in field_name or "Estimate" in field_name:
                    value = str(random.choice([1, 2, 3, 5, 8, 13]))
                elif "Progress" in field_name:
                    value = str(random.randint(0, 100))
                else:
                    value = str(random.randint(1, 100))
            else:  # text
                if field_name in text_values:
                    value = random.choice(text_values[field_name])
                else:
                    value = f"Value {random.randint(1, 5)}"
            
            updated_at = random_past_timestamp(days_ago_min=150, days_ago_max=1)
            
            cursor.execute("""
                INSERT INTO custom_field_values (value_id, field_id, task_id, value, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (value_id, field_id, task_id, value, updated_at))
            
            values_created += 1
    
    conn.commit()
    print(f"✓ Created {values_created} custom field value(s)")
    return values_created

#!/usr/bin/env python3
"""
Verification script to validate the generated database.
Checks for data integrity, referential integrity, and temporal consistency.
"""
import sqlite3
import sys
from pathlib import Path


def verify_database(db_path: str):
    """Verify database integrity and consistency."""
    
    print("=" * 60)
    print("Database Verification")
    print("=" * 60)
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys to check referential integrity
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA foreign_key_check")
    fk_violations = cursor.fetchall()
    
    if fk_violations:
        print("❌ Foreign key violations found:")
        for violation in fk_violations:
            print(f"   {violation}")
        return False
    else:
        print("✓ Foreign key integrity: PASSED")
    
    # Check temporal consistency
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE completed_at IS NOT NULL 
        AND completed_at < created_at
    """)
    temporal_violations = cursor.fetchone()[0]
    
    if temporal_violations > 0:
        print(f"❌ Temporal consistency: FAILED ({temporal_violations} tasks with completed_at < created_at)")
        return False
    else:
        print("✓ Temporal consistency: PASSED")
    
    # Check for unassigned tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id IS NULL")
    unassigned = cursor.fetchone()[0]
    print(f"✓ Unassigned tasks: {unassigned}")
    
    # Check for completed vs incomplete tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
    incomplete = cursor.fetchone()[0]
    total = completed + incomplete
    completion_rate = (completed / total * 100) if total > 0 else 0
    print(f"✓ Task completion: {completed}/{total} ({completion_rate:.1f}%)")
    
    # Check for overdue tasks
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE due_date IS NOT NULL 
        AND completed = 0
        AND date(due_date) < date('now')
    """)
    overdue = cursor.fetchone()[0]
    print(f"✓ Overdue tasks: {overdue}")
    
    # Check subtask distribution
    cursor.execute("""
        SELECT COUNT(DISTINCT parent_task_id) FROM subtasks
    """)
    tasks_with_subtasks = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    subtask_rate = (tasks_with_subtasks / total_tasks * 100) if total_tasks > 0 else 0
    print(f"✓ Tasks with subtasks: {tasks_with_subtasks}/{total_tasks} ({subtask_rate:.1f}%)")
    
    # Check tag associations
    cursor.execute("""
        SELECT COUNT(DISTINCT task_id) FROM task_tag_associations
    """)
    tasks_with_tags = cursor.fetchone()[0]
    tag_rate = (tasks_with_tags / total_tasks * 100) if total_tasks > 0 else 0
    print(f"✓ Tasks with tags: {tasks_with_tags}/{total_tasks} ({tag_rate:.1f}%)")
    
    # Summary of record counts
    print()
    print("Record Counts:")
    tables = [
        "organizations", "teams", "users", "team_memberships",
        "projects", "sections", "tasks", "subtasks", "comments",
        "tags", "task_tag_associations", 
        "custom_field_definitions", "custom_field_values"
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  • {table:30s} {count:6d}")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("✅ Verification Complete: All checks passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    project_root = Path(__file__).parent
    db_path = project_root / "output" / "asana_simulation.sqlite"
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print("Run 'python3 -m src.main' first to generate the database.")
        sys.exit(1)
    
    success = verify_database(str(db_path))
    sys.exit(0 if success else 1)

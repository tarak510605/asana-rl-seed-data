"""
Main orchestration script for generating Asana-like seed data.

Generates a realistic SQLite database for a B2B SaaS company using Asana,
following the schema defined in schema.sql.

Usage:
    python -m src.main
    
Configuration:
    Edit config.ini to adjust generation parameters, database size, and date ranges.
"""
import logging
import sys
from pathlib import Path

from src.utils.config import get_config
from src.utils.logger import setup_logging
from src.utils.db import get_connection, initialize_schema
from src.generators.organizations import generate_organizations
from src.generators.teams import generate_teams
from src.generators.users import generate_users
from src.generators.projects import generate_projects
from src.generators.sections import generate_sections
from src.generators.tasks import generate_tasks
from src.generators.subtasks import generate_subtasks
from src.generators.comments import generate_comments
from src.generators.tags import generate_tags, generate_task_tag_associations
from src.generators.custom_fields import generate_custom_fields, generate_custom_field_values


def main():
    """
    Main execution function that orchestrates the entire data generation pipeline.
    All configuration parameters are loaded from config.ini.
    """
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = get_config()
    
    print("=" * 60)
    print("Asana Seed Data Generator")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Initialize database connection and schema
        logger.info("Initializing database...")
        print("📦 Initializing database...")
        conn = get_connection(config.db_output_path)
        initialize_schema(conn)
        logger.info("Database initialized successfully")
        print("✓ Database initialized with schema\n")
        
        # Step 2: Generate organizations
        logger.info(f"Generating {config.organizations_count} organization(s)...")
        print("🏢 Generating organizations...")
        org_ids = generate_organizations(conn, count=config.organizations_count)
        org_id = org_ids[0]
        print()
        
        # Step 3: Generate teams
        logger.info(f"Generating {config.teams_per_org} teams...")
        print("👥 Generating teams...")
        teams = generate_teams(conn, org_id, count=config.teams_per_org)
        print()
        
        # Step 4: Generate users (includes team_memberships)
        logger.info(f"Generating {config.users_per_org} users...")
        print("👤 Generating users...")
        users = generate_users(conn, org_id, count=config.users_per_org)
        print()
        
        # Step 5: Generate projects
        logger.info(f"Generating projects ({config.projects_per_team} per team)...")
        print("📋 Generating projects...")
        projects = generate_projects(conn, teams, users, projects_per_team=config.projects_per_team)
        print()
        
        # Step 6: Generate sections
        logger.info("Generating sections...")
        print("📂 Generating sections...")
        sections = generate_sections(conn, projects)
        print()
        
        # Step 7: Generate tasks
        logger.info(f"Generating tasks ({config.tasks_per_project} per project)...")
        print("✅ Generating tasks...")
        tasks = generate_tasks(conn, projects, sections, users, tasks_per_project=config.tasks_per_project)
        print()
        
        # Step 8: Generate subtasks
        logger.info("Generating subtasks...")
        print("🔸 Generating subtasks...")
        subtasks = generate_subtasks(conn, tasks, subtask_probability=config.getfloat('generation_probabilities', 'subtask_probability', 0.3))
        print()
        
        # Step 9: Generate comments
        logger.info("Generating comments...")
        print("💬 Generating comments...")
        comments = generate_comments(conn, tasks, users, avg_comments_per_task=1.5)
        print()
        
        # Step 10: Generate tags
        logger.info(f"Generating {config.tags_count} tags...")
        print("🏷️  Generating tags...")
        tags = generate_tags(conn, count=config.tags_count)
        print()
        
        # Step 11: Generate task-tag associations
        logger.info("Generating task-tag associations...")
        print("🔗 Generating task-tag associations...")
        generate_task_tag_associations(conn, tasks, tags)
        print()
        
        # Step 12: Generate custom field definitions
        logger.info("Generating custom field definitions...")
        print("⚙️  Generating custom field definitions...")
        custom_fields = generate_custom_fields(conn, projects)
        print()
        
        # Step 13: Generate custom field values
        logger.info("Generating custom field values...")
        print("📊 Generating custom field values...")
        generate_custom_field_values(conn, custom_fields, tasks)
        print()
        
        # Summary
        print("=" * 60)
        print("✨ Data generation complete!")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  • Organizations:       {len(org_ids)}")
        print(f"  • Teams:               {len(teams)}")
        print(f"  • Users:               {len(users)}")
        print(f"  • Projects:            {len(projects)}")
        print(f"  • Sections:            {len(sections)}")
        print(f"  • Tasks:               {len(tasks)}")
        print(f"  • Subtasks:            {len(subtasks)}")
        print(f"  • Comments:            {len(comments)}")
        print(f"  • Tags:                {len(tags)}")
        print(f"  • Custom Fields:       {len(custom_fields)}")
        print()
        
        # Database location
        project_root = Path(__file__).parent.parent
        db_path = project_root / config.db_output_path
        print(f"📁 Database saved to: {db_path}")
        print()
        
        logger.info("Data generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data generation: {e}", exc_info=True)
        print(f"\n❌ Error during data generation: {e}")
        import traceback
        traceback.print_exc()
        conn.close()
        sys.exit(1)
    
    finally:
        # Close connection
        conn.close()
    
    print("✅ Done!")


if __name__ == "__main__":
    main()

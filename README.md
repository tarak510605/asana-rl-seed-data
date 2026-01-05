# Asana RL Seed Data Generator

A Python project that generates realistic seed data for an Asana-like project management system. Created for a Research Scientist Internship take-home assignment.

## Overview

This project generates a realistic SQLite database representing a large B2B SaaS company using Asana for project management. The data includes:

- Organizations and teams
- Users with team memberships
- Projects with sections
- Tasks with priorities, due dates, and assignments
- Subtasks, comments, and tags
- Custom fields with values

## Features

- ✅ Strict foreign key integrity
- ✅ Temporal consistency (created_at < completed_at)
- ✅ Realistic distributions
- ✅ Unassigned, overdue, and incomplete tasks
- ✅ UUIDv4 primary keys
- ✅ Modular, readable code
- ✅ No external dependencies (pure Python stdlib)

## Project Structure

```
asana_rl_seed_data/
├── schema.sql                # Database schema (DO NOT MODIFY)
├── requirements.txt          # Python dependencies (none required)
├── .env.example             # Example configuration
├── src/
│   ├── main.py              # Main orchestration script
│   ├── generators/          # Data generators
│   │   ├── organizations.py
│   │   ├── teams.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   ├── sections.py
│   │   ├── tasks.py
│   │   ├── subtasks.py
│   │   ├── comments.py
│   │   ├── tags.py
│   │   └── custom_fields.py
│   └── utils/              # Utility modules
│       ├── db.py           # Database connection
│       ├── id_utils.py     # UUID generation
│       └── time_utils.py   # Timestamp utilities
└── output/
    └── asana_simulation.sqlite  # Generated database
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)
- SQLite3 (included with Python)

## Installation & Setup

### Option 1: Quick Setup (Recommended)

```bash
# Clone or download the project
cd asana_rl_seed_data

# Run the setup script
./setup.sh

# Generate the database
python3 -m src.main
```

### Option 2: Manual Setup

```bash
# Verify Python 3.7+ is installed
python3 --version

# Create output directory
mkdir -p output

# Install dependencies (none required, but you can run this anyway)
pip install -r requirements.txt

# Generate the database
python3 -m src.main
```

## Usage

### Quick Start

```bash
# Run the generator with default settings
python3 -m src.main
```

The generated database will be saved to `output/asana_simulation.sqlite`.

### Configuration

All generation parameters can be customized via `config.ini`:

```ini
[generation_counts]
organizations = 1
teams_per_org = 8
users_per_org = 50
projects_per_team = 4
tasks_per_project = 20
tags_count = 15

[generation_probabilities]
task_unassigned_rate = 0.20
task_completion_rate = 0.70
task_overdue_chance = 0.20
subtask_probability = 0.30

[date_ranges]
org_created_days_ago_min = 730
org_created_days_ago_max = 365
# ... more date range settings
```

**To customize generation:**

1. Edit `config.ini` to adjust counts, probabilities, and date ranges
2. Run `python3 -m src.main` to generate a new database

### Verification

Verify the generated database integrity:

```bash
python3 verify.py
```

This checks:
- Foreign key integrity
- Temporal consistency (created_at < completed_at)
- Realistic data distributions
- Record counts

### Database Queries

```bash
# Open the database
sqlite3 output/asana_simulation.sqlite

# Example queries
SELECT COUNT(*) FROM tasks;
SELECT COUNT(*) FROM users;
SELECT name, project_type FROM projects LIMIT 10;
SELECT first_name, last_name, role FROM users LIMIT 10;
```

### Customization

You can modify the data generation parameters in `config.ini`:

**Generation Counts** - Control the size of the database:
- `organizations`: Number of companies (typically 1)
- `teams_per_org`: Teams per organization
- `users_per_org`: Users per organization
- `projects_per_team`: Projects per team
- `tasks_per_project`: Tasks per project
- `tags_count`: Total number of tags

**Generation Probabilities** - Control data characteristics:
- `task_unassigned_rate`: % of tasks without assignees (0.0-1.0)
- `task_has_due_date_rate`: % of tasks with due dates
- `task_completion_rate`: % of tasks completed
- `task_overdue_chance`: % of tasks that are overdue
- `subtask_probability`: % of tasks with subtasks
- `task_has_description_rate`: % of tasks with descriptions
- `task_has_tags_rate`: % of tasks with tags
- `custom_field_value_rate`: % of tasks with custom field values

**Date Ranges** - Control when entities were created:
- `*_created_days_ago_min/max`: Date ranges for entity creation

Example: To generate a larger database with 100 users and 30 tasks per project:

```ini
[generation_counts]
users_per_org = 100
tasks_per_project = 30
```

## Data Generation Order

The pipeline follows this strict order to maintain referential integrity:

1. Organizations
2. Teams
3. Users (+ team_memberships)
4. Projects
5. Sections
6. Tasks
7. Subtasks
8. Comments
9. Tags (+ task_tag_associations)
10. Custom field definitions (+ custom_field_values)

## Schema

The database schema is defined in `schema.sql` and includes the following tables:

- `organizations` - Company/organization records
- `teams` - Departmental teams within organizations
- `users` - User accounts
- `team_memberships` - User-team associations
- `projects` - Project records with status tracking
- `sections` - Project sections (columns/stages)
- `tasks` - Individual work items
- `subtasks` - Sub-items under tasks
- `comments` - Discussion threads on tasks
- `tags` - Categorization labels
- `task_tag_associations` - Task-tag relationships
- `custom_field_definitions` - Custom field schemas
- `custom_field_values` - Custom field data per task

## Data Characteristics

### Realistic Distributions

- **Users**: 50 users across 8 teams
- **Projects**: ~4 projects per team
- **Tasks**: ~20 tasks per project
- **Subtasks**: 30% of tasks have 2-5 subtasks
- **Comments**: Average 1.5 comments per task
- **Tags**: 15 organization-wide tags, 60% of tasks tagged
- **Custom Fields**: 2-4 custom fields per project

### Temporal Consistency

- All timestamps use ISO 8601 format
- `created_at` always precedes `completed_at`
- Comments are chronologically ordered
- Due dates can be overdue (20% chance)

### Task States

- 70% completion rate
- 20% unassigned tasks
- 20% overdue tasks
- Mix of priorities (low, medium, high, urgent)
- Various project statuses (active, on_hold, completed)

## Database Operations

### Querying the Database

```bash
# Open the database
sqlite3 output/asana_simulation.sqlite

# Example queries
SELECT COUNT(*) FROM tasks;
SELECT COUNT(*) FROM users;
SELECT name, status FROM projects LIMIT 10;
```

### Resetting the Database

Simply run `python src/main.py` again. The script automatically removes the existing database before generating new data.

## Development

### Adding New Generators

1. Create a new file in `src/generators/`
2. Implement a generator function that:
   - Accepts a `sqlite3.Connection`
   - Inserts data into the appropriate table
   - Returns created IDs when needed by downstream generators
3. Import and call it in `src/main.py` in the correct order

### Modifying Time Distributions

Edit functions in `src/utils/time_utils.py`:

- `random_past_timestamp()` - Generate timestamps in the past
- `random_timestamp_after()` - Generate timestamps after a given time
- `random_due_date()` - Generate due dates with overdue probability
- `maybe_completed_at()` - Generate completion timestamps

## License

This project is created for educational purposes as part of a take-home assignment.

## Notes

- The schema in `schema.sql` is final and should not be modified
- All IDs use UUIDv4 format
- Foreign key constraints are enforced
- The database is regenerated from scratch on each run
- No ORM is used - direct SQL with sqlite3

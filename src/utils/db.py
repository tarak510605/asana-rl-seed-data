"""
Database connection and initialization utilities.
"""
import sqlite3
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Create and return a SQLite connection with foreign key constraints enabled.
    
    Args:
        db_path: Path to the database file. Defaults to output/asana_simulation.sqlite
    
    Returns:
        sqlite3.Connection with foreign keys enabled
        
    Raises:
        Exception: If database connection or initialization fails
    """
    if db_path is None:
        # Default path relative to project root
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "output" / "asana_simulation.sqlite"
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        logger.info(f"Output directory ensured: {os.path.dirname(db_path)}")
        
        # Remove existing database to start fresh
        if os.path.exists(db_path):
            logger.info(f"Removing existing database: {db_path}")
            os.remove(db_path)
        
        # Create connection
        logger.info(f"Creating database connection: {db_path}")
        conn = sqlite3.Connection(db_path)
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        logger.info("Foreign key constraints enabled")
        
        return conn
        
    except Exception as e:
        logger.error(f"Failed to create database connection: {e}")
        raise Exception(f"Database connection error: {e}")


def initialize_schema(conn: sqlite3.Connection, schema_path: str = None) -> None:
    """
    Initialize the database schema from schema.sql file.
    
    Args:
        conn: SQLite connection
        schema_path: Path to schema.sql file. Defaults to project root.
        
    Raises:
        FileNotFoundError: If schema.sql file is not found
        Exception: If schema initialization fails
    """
    if schema_path is None:
        project_root = Path(__file__).parent.parent.parent
        schema_path = project_root / "schema.sql"
    
    try:
        # Check if schema file exists
        if not os.path.exists(schema_path):
            logger.error(f"Schema file not found: {schema_path}")
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        logger.info(f"Loading schema from: {schema_path}")
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema (may contain multiple statements)
        conn.executescript(schema_sql)
        conn.commit()
        
        logger.info("Schema initialized successfully")
        
    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Failed to initialize schema: {e}")
        raise Exception(f"Schema initialization error: {e}")

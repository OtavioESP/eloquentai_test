"""
Migration utility for automatic migration execution on startup
"""

import os
import sys
import psycopg2
from pathlib import Path
from typing import List
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rag_chat'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

def get_connection():
    """Get database connection"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise e

def create_migrations_table(conn):
    """Create migrations tracking table if it doesn't exist"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def get_executed_migrations(conn) -> List[str]:
    """Get list of executed migrations"""
    with conn.cursor() as cur:
        cur.execute("SELECT filename FROM migrations ORDER BY id")
        return [row[0] for row in cur.fetchall()]

def mark_migration_executed(conn, filename: str):
    """Mark migration as executed"""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO migrations (filename) VALUES (%s)", (filename,))
        conn.commit()

def get_migration_files() -> List[Path]:
    """Get all migration files sorted by name"""
    migrations_dir = Path(__file__).parent / "migrations"
    return sorted([f for f in migrations_dir.glob("*.sql") if f.name != "run_migrations.py"])

def run_migration(conn, migration_file: Path):
    """Run a single migration file"""
    logger.info(f"Running migration: {migration_file.name}")
    
    with open(migration_file, 'r') as f:
        sql_content = f.read()
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql_content)
            conn.commit()
            mark_migration_executed(conn, migration_file.name)
            logger.info(f"✓ Migration {migration_file.name} executed successfully")
        except psycopg2.Error as e:
            conn.rollback()
            logger.error(f"✗ Error running migration {migration_file.name}: {e}")
            raise e

def run_pending_migrations():
    """Run all pending migrations"""
    try:
        conn = get_connection()
        try:
            # Create migrations table if it doesn't exist
            create_migrations_table(conn)
            
            # Get executed and pending migrations
            executed = get_executed_migrations(conn)
            migration_files = get_migration_files()
            pending = [f for f in migration_files if f.name not in executed]
            
            if not pending:
                logger.info("No pending migrations to run")
                return True
            
            logger.info(f"Found {len(pending)} pending migrations")
            
            # Run each pending migration
            for migration_file in pending:
                run_migration(conn, migration_file)
            
            logger.info("All migrations completed successfully")
            return True
            
        finally:
            conn.close()
            
    except psycopg2.Error as e:
        logger.error(f"Migration failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False

def check_database_connection():
    """Check if database connection is available"""
    try:
        conn = get_connection()
        conn.close()
        return True
    except psycopg2.Error:
        return False

def auto_migrate():
    """
    Main function to run migrations automatically
    Returns True if successful, False otherwise
    """
    logger.info("Starting automatic migration check...")
    
    # Check database connection first
    if not check_database_connection():
        logger.error("Cannot connect to database. Please check your database configuration.")
        return False
    
    # Run pending migrations
    return run_pending_migrations()

if __name__ == "__main__":
    # Test migration functionality
    success = auto_migrate()
    if success:
        print("✓ Auto-migration completed successfully")
        sys.exit(0)
    else:
        print("✗ Auto-migration failed")
        sys.exit(1)

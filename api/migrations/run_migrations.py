#!/usr/bin/env python3
"""
Migration runner for PostgreSQL database
Usage: python run_migrations.py [up|down] [migration_file]
"""

import os
import sys
import psycopg2
from pathlib import Path
import argparse
from typing import List, Optional

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
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def create_migrations_table(conn):
    """Create migrations tracking table"""
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
    migrations_dir = Path(__file__).parent
    return sorted([f for f in migrations_dir.glob("*.sql") if f.name != "run_migrations.py"])

def run_migration(conn, migration_file: Path):
    """Run a single migration file"""
    print(f"Running migration: {migration_file.name}")
    
    with open(migration_file, 'r') as f:
        sql_content = f.read()
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql_content)
            conn.commit()
            mark_migration_executed(conn, migration_file.name)
            print(f"✓ Migration {migration_file.name} executed successfully")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"✗ Error running migration {migration_file.name}: {e}")
            sys.exit(1)

def run_migrations_up(conn, target_file: Optional[str] = None):
    """Run migrations up to target file or all pending"""
    create_migrations_table(conn)
    executed = get_executed_migrations(conn)
    migration_files = get_migration_files()
    
    if target_file:
        target_path = Path(target_file)
        if not target_path.exists():
            print(f"Target migration file not found: {target_file}")
            sys.exit(1)
        migration_files = [f for f in migration_files if f.name <= target_path.name]
    
    pending = [f for f in migration_files if f.name not in executed]
    
    if not pending:
        print("No pending migrations to run")
        return
    
    print(f"Found {len(pending)} pending migrations")
    for migration_file in pending:
        run_migration(conn, migration_file)

def run_migrations_down(conn, target_file: str):
    """Rollback migrations down to target file"""
    create_migrations_table(conn)
    executed = get_executed_migrations(conn)
    
    if target_file not in executed:
        print(f"Migration {target_file} not found in executed migrations")
        sys.exit(1)
    
    # For simplicity, this just removes the migration record
    # In production, you'd want to implement proper rollback SQL
    with conn.cursor() as cur:
        cur.execute("DELETE FROM migrations WHERE filename = %s", (target_file,))
        conn.commit()
        print(f"✓ Rolled back migration: {target_file}")

def main():
    parser = argparse.ArgumentParser(description='Run database migrations')
    parser.add_argument('command', choices=['up', 'down'], help='Migration command')
    parser.add_argument('target', nargs='?', help='Target migration file (optional for up)')
    
    args = parser.parse_args()
    
    conn = get_connection()
    try:
        if args.command == 'up':
            run_migrations_up(conn, args.target)
        elif args.command == 'down':
            if not args.target:
                print("Target migration file required for rollback")
                sys.exit(1)
            run_migrations_down(conn, args.target)
    finally:
        conn.close()

if __name__ == '__main__':
    main()

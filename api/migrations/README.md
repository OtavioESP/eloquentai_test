# For initialize the whole application run the:

```shell
    docker-compose up -d
```

# Database Migrations

This directory contains PostgreSQL database migrations for the RAG chat application.

## Database Schema

The initial schema includes three main tables:

### Users Table
- `id` (UUID, Primary Key) - Auto-generated UUID
- `name` (VARCHAR) - User's display name
- `password` (VARCHAR) - Hashed password
- `created_at` (TIMESTAMP) - Record creation time
- `updated_at` (TIMESTAMP) - Last update time

### Chats Table
- `id` (UUID, Primary Key) - Auto-generated UUID
- `user_id` (UUID, Foreign Key) - References users.id
- `created_at` (TIMESTAMP) - Record creation time
- `updated_at` (TIMESTAMP) - Last update time

### Messages Table
- `id` (SERIAL, Primary Key) - Auto-incrementing integer
- `chat_id` (UUID, Foreign Key) - References chats.id
- `content` (TEXT) - Message content
- `is_response` (BOOLEAN) - Whether this is a bot response (default: false)
- `created_at` (TIMESTAMP) - Record creation time

## Running Migrations

### Prerequisites

1. Install required dependencies:
```bash
pip install psycopg2-binary
```

2. Set up environment variables:
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=rag_chat
export DB_USER=postgres
export DB_PASSWORD=your_password
export PINECONE_API_KEY=API_KEY
export PINECONE_INDEX=API_INDEX
```

### Commands

#### Run all pending migrations:
```bash
python migrations/run_migrations.py up
```

#### Run migrations up to a specific file:
```bash
python migrations/run_migrations.py up 001_initial_schema.sql
```

#### Rollback a migration:
```bash
python migrations/run_migrations.py down 001_initial_schema.sql
```

## Migration Files

- `001_initial_schema.sql` - Initial database schema with all tables, indexes, and triggers
- `run_migrations.py` - Migration runner script

## Features

- **UUID Support**: Uses PostgreSQL's uuid-ossp extension for UUID generation
- **Foreign Key Constraints**: Proper relationships between tables with CASCADE deletes
- **Indexes**: Performance indexes on frequently queried columns
- **Triggers**: Automatic updated_at timestamp updates
- **Migration Tracking**: Tracks executed migrations to prevent re-running

## Database Setup
# if done correctly the aplication itself will generate the migrations and database, if not:

1. Create a PostgreSQL database:
```sql
CREATE DATABASE rag_chat;
```

2. Run the initial migration:
```bash
python migrations/run_migrations.py up
```

This will create all tables, indexes, and triggers needed for the application.

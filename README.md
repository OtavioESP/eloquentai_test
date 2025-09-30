<<<<<<< Updated upstream
# eloquentai_test

Node v23.11.x
=======
# RAG Chat Application

A full-stack RAG (Retrieval-Augmented Generation) chat application with FastAPI backend and React frontend.

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React with TypeScript and Vite
- **Database**: PostgreSQL with automatic migrations
- **Containerization**: Docker Compose for easy deployment

## 🚀 Quick Start with Docker Compose

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd eloquentai_test
```

### 2. Start All Services

```bash
docker-compose up --build
```

This will start:
- **PostgreSQL Database** on port 5432
- **FastAPI Backend** on port 8000
- **React Frontend** on port 3000

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🛠️ Development Setup (Without Docker)

### Backend Setup

1. **Navigate to API directory**:
```bash
cd api
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp config.env.example .env
# Edit .env with your database settings
```

5. **Start PostgreSQL database** (using Docker):
```bash
docker run --name rag_chat_db -e POSTGRES_DB=rag_chat -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15-alpine
```

6. **Run the API**:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. **Navigate to UI directory**:
```bash
cd ui
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

## 📊 Database Schema

The application uses PostgreSQL with the following tables:

### Users
- `id` (UUID) - Primary key
- `name` (VARCHAR) - User's display name
- `password` (VARCHAR) - Hashed password
- `created_at` (TIMESTAMP) - Creation timestamp
- `updated_at` (TIMESTAMP) - Last update timestamp

### Chats
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key to users table
- `created_at` (TIMESTAMP) - Creation timestamp
- `updated_at` (TIMESTAMP) - Last update timestamp

### Messages
- `id` (SERIAL) - Auto-incrementing primary key
- `chat_id` (UUID) - Foreign key to chats table
- `content` (TEXT) - Message content
- `is_response` (BOOLEAN) - Whether this is a bot response
- `created_at` (TIMESTAMP) - Creation timestamp

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `api` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag_chat
DB_USER=postgres
DB_PASSWORD=password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Compose Services

- **postgres**: PostgreSQL 15 database
- **api**: FastAPI application with auto-migrations
- **frontend**: React development server

## 📝 API Endpoints

- `GET /api/health` - Health check
- `POST /api/v1/users/login` - User login
- `POST /api/v1/users/unlogged` - Continue without login
- `GET /api/v1/chats` - Get user chats
- `POST /api/v1/chats` - Create new chat
- `GET /api/v1/chats/{chat_id}/messages` - Get chat messages
- `POST /api/v1/chats/{chat_id}/messages` - Send message

## 🗄️ Database Migrations

Migrations run automatically on API startup. Manual migration commands:

```bash
# Run all pending migrations
python api/migrations/run_migrations.py up

# Run migrations up to specific file
python api/migrations/run_migrations.py up 001_initial_schema.sql

# Rollback migration
python api/migrations/run_migrations.py down 001_initial_schema.sql
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api
```

## 🧪 Testing

### Test Database Connection
```bash
python api/database.py
```

### Test Migration System
```bash
python api/migration_util.py
```

## 📁 Project Structure

```
eloquentai_test/
├── api/                    # FastAPI backend
│   ├── app/               # Application modules
│   ├── migrations/        # Database migrations
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── migration_util.py # Auto-migration utility
│   └── requirements.txt  # Python dependencies
├── ui/                    # React frontend
│   ├── src/              # Source code
│   ├── public/           # Static assets
│   └── package.json      # Node dependencies
├── docker-compose.yml    # Docker Compose configuration
└── README.md            # This file
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS middleware configuration
- SQL injection prevention with parameterized queries
- Environment variable configuration

## 🚀 Production Deployment

For production deployment:

1. Update environment variables for production
2. Use production PostgreSQL instance
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use production Docker images
6. Configure proper logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
>>>>>>> Stashed changes

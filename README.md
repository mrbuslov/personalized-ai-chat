# AI-Powered Customer Messaging Management System

A lightweight MVP/POC for testing AI-assisted customer communication management. This system allows managers to simulate conversations with clients, where AI generates manager responses that can be reviewed, edited, and approved before sending.

## Overview

This is a proof-of-concept to test AI response quality before integrating with real platforms like Instagram, OnlyFans, and CRM systems. The system provides:

- **Multi-tenant architecture** with company-level data isolation
- **Chat simulation** where managers write messages as clients
- **AI-generated responses** as the manager with review/edit capabilities  
- **Flexible AI configuration** with global and per-chat customization
- **Message management** with edit, delete, and AI revision features

## Architecture

### Backend (FastAPI)
- **FastAPI** with Tortoise ORM and PostgreSQL
- **Pydantic Settings** for configuration management
- **Database Facade** for abstracted data operations
- **JWT Authentication** with refresh token support
- **OpenAI/Claude integration** for AI message generation
- **RESTful API** with comprehensive endpoint coverage

### Frontend (React)
- **React 18** with React Router for navigation
- **Tailwind CSS** for clean, minimalist UI
- **Axios** for API communication with automatic token refresh
- **Modular components** for chat interface and message management

### Infrastructure
- **Docker Compose** for easy development and deployment
- **PostgreSQL** database with proper indexing
- **Environment-based configuration** for different deployment stages

## Features

### Core Functionality

1. **User Management**
   - Multi-tenant system with company isolation
   - JWT authentication with automatic token refresh
   - User registration with company creation

2. **Chat Interface**
   - Create and manage multiple client conversations
   - Client descriptions for AI context
   - Special instructions for per-chat AI behavior
   - Import/export message functionality

3. **Message Management**
   - Write messages as the client (simulation)
   - AI generates manager responses
   - Edit messages manually or with AI assistance
   - Delete messages with confirmation
   - Real-time message flow

4. **AI Configuration**
   - Global manager personality/behavior settings
   - Per-chat special instructions override
   - AI revision with custom instructions
   - Support for multiple AI providers (OpenAI, Claude)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd personalized-ai-chat
```

### 2. Set Up Environment
```bash
cd docker
cp .env.example .env
# Edit .env with your configuration
```

### 3. Configure API Keys
Add your AI provider API keys to the `.env` file:
```env
OPENAI_API_KEY=your-openai-key-here
```

### 4. Start the Services
```bash
docker-compose up -d
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Database Setup
```bash
# The database will be automatically initialized when the backend starts
# Tables are created using Tortoise ORM's auto-generation
```

## Configuration


## Usage Guide

### 1. Create Account
- Register with your email, name, and company name
- Each company has isolated data

### 2. Set Up AI Configuration
- Go to Dashboard → AI Settings
- Define the global manager personality and behavior
- This prompt will be used for all chats unless overridden

### 3. Create a Chat
- Click "New Chat" on the dashboard
- Provide a name and client description
- Add special instructions if needed for this specific client

### 4. Simulate Conversation
- Write messages as the CLIENT (simulating customer input)
- Click "Generate AI" to get manager responses
- Review, edit, or revise AI responses before "sending"
- Use "Edit with AI" for automated message revisions

### 5. Message Management
- **Edit**: Manually rewrite any message
- **Edit with AI**: Provide revision instructions for automated editing
- **Delete**: Remove messages from conversation
- **Import**: Bulk import conversation history

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info

### Chats
- `GET /chats/` - List user's chats
- `POST /chats/` - Create new chat
- `GET /chats/{id}` - Get specific chat
- `PUT /chats/{id}` - Update chat
- `DELETE /chats/{id}` - Delete chat

### Messages
- `POST /messages/` - Create message
- `GET /messages/{id}` - Get message
- `PUT /messages/{id}` - Update message
- `DELETE /messages/{id}` - Delete message
- `POST /messages/generate-ai-response` - Generate AI response
- `POST /messages/revise-with-ai` - Revise message with AI
- `POST /messages/import` - Import multiple messages

### AI Configuration
- `GET /ai-config/global` - Get global AI config
- `PUT /ai-config/global` - Update global AI config
- `GET /ai-config/chat/{id}` - Get chat-specific AI config
- `PUT /ai-config/chat/{id}` - Update chat-specific AI config

## Security Features

- **JWT Authentication** with secure token refresh
- **Multi-tenant data isolation** at company level
- **Input validation** using Pydantic schemas
- **SQL injection prevention** via ORM
- **CORS configuration** for frontend integration
- **Environment-based secrets** management

## Deployment

### Production Deployment
1. Copy `docker/.env.example` to `docker/.env`
2. Update all configuration values for production
3. Use strong, unique `SECRET_KEY`
4. Configure proper CORS origins
5. Set `DEBUG=false`
6. Run `docker-compose up -d`

### Environment Considerations
- Use managed PostgreSQL service for production
- Configure proper backup strategies
- Set up monitoring and logging
- Use HTTPS with proper SSL certificates
- Consider load balancing for scalability

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in .env
   - Verify network connectivity

2. **AI Responses Not Working**
   - Check API key configuration
   - Verify API key has proper permissions
   - Check rate limits and billing status

3. **Frontend Can't Connect to Backend**
   - Verify CORS configuration
   - Check backend URL in frontend env
   - Ensure backend is running and accessible

4. **Token Refresh Issues**
   - Check SECRET_KEY consistency
   - Verify token expiration settings
   - Clear browser storage and re-login

## Project Structure

```
personalized-ai-chat/
├── backend/
│   ├── api/           # FastAPI routers
│   ├── common/        # Settings and database facade
│   ├── models/        # Tortoise ORM models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic layer
│   └── main.py        # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API and auth services
│   └── public/
├── docker/
│   ├── docker-compose.yml
│   └── .env.example
└── README.md
```

## Contributing

1. Follow existing code structure and naming conventions
2. Use TypeScript for new frontend components
3. Add proper error handling and validation
4. Write tests for new features
5. Update documentation for API changes

## License

This is a proof-of-concept project for testing AI-assisted customer communication management.


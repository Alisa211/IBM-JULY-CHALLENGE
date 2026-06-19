# Stage 3A - Watsonx.ai Prompt Engine Implementation

## Overview

Stage 3A implements the **Watsonx.ai Prompt Engine** for AI-powered sculpture concept generation. This is the foundation for the RAG system that will be built in later stages.

## Architecture

```
React Frontend
      ↓
FastAPI Gateway
      ↓
Idea Service
      ↓
Watsonx Service
      ↓
IBM Watsonx.ai API
      ↓
Idea Cards (Database)
```

## What Was Implemented

### 1. Watsonx Integration Layer (`integrations/watsonx.ai/`)

#### [`clients.py`](integrations/watsonx.ai/clients.py)
- **WatsonxClient**: Handles all communication with IBM Watsonx.ai
- Authentication with IBM Cloud
- Model initialization and management
- Three specialized generation methods:
  - `generate_ideas()`: Creative idea generation (temperature=0.8)
  - `generate_critique()`: Balanced analysis (temperature=0.5)
  - `analyze_style()`: Style analysis (temperature=0.6)
- Health check functionality

#### [`prompts.py`](integrations/watsonx.ai/prompts.py)
- **IDEA_GENERATION_PROMPT**: Template for generating sculpture concepts
- **CRITIQUE_PROMPT**: Template for critiquing concepts
- **STYLE_DNA_PROMPT**: Template for style analysis
- `format_prompt()`: Helper function for template formatting

#### [`parser.py`](integrations/watsonx.ai/parser.py)
- `parse_idea_cards()`: Converts raw LLM output to structured idea cards
- `parse_critique()`: Parses critique responses
- `parse_style_dna()`: Parses style analysis
- JSON extraction and validation
- Error handling and recovery

### 2. Backend Services

#### [`watsonx_service.py`](backend/app/services/watsonx_service.py)
- **WatsonxService**: Business logic layer for Watsonx operations
- Orchestrates prompt formatting, API calls, and parsing
- Error handling and logging
- Singleton pattern for efficient resource usage

#### [`idea_service.py`](backend/app/services/idea_service.py)
- **IdeaService**: Business logic for idea management
- Generates ideas via Watsonx
- Persists ideas to database
- Implements caching for performance
- CRUD operations for ideas

### 3. Data Layer

#### [`idea.py` (Model)](backend/app/models/idea.py)
Database model with fields:
- Core content: title, description, artistic_rationale
- Optional details: materials, scale, cultural_references
- Metadata: brief, project_id
- Timestamps: created_at, updated_at

#### [`idea_repo.py`](backend/app/repositories/idea_repo.py)
Repository pattern with methods:
- `get_by_project()`: Filter by project
- `get_by_brief()`: Filter by brief
- `get_recent()`: Get latest ideas
- `search_by_title()`: Search functionality
- `count_by_project()`: Count ideas

#### [`idea.py` (Schemas)](backend/app/schemas/idea.py)
Pydantic schemas:
- `IdeaGenerateRequest`: Input for generation
- `IdeaCardResponse`: Output format
- `IdeaGenerateResponse`: Batch generation response
- `IdeaUpdateRequest`: Update operations

### 4. API Endpoints ([`ideas.py`](backend/app/api/v1/ideas.py))

```
POST   /api/v1/ideas/generate          - Generate new ideas
GET    /api/v1/ideas                   - List all ideas (paginated)
GET    /api/v1/ideas/recent            - Get recent ideas
GET    /api/v1/ideas/project/{id}      - Get project ideas
GET    /api/v1/ideas/{id}              - Get specific idea
PUT    /api/v1/ideas/{id}              - Update idea
DELETE /api/v1/ideas/{id}              - Delete idea
```

### 5. Configuration

#### Environment Variables ([`.env`](backend/.env))
```bash
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-instruct-v2
```

#### Database Migration
- Created migration: [`add_ideas_table.py`](backend/migrations/versions/add_ideas_table.py)
- Includes indexes on title and project_id
- Foreign key to projects table

## How to Use

### 1. Setup Environment

```bash
# Navigate to backend
cd backend

# Copy environment template
cp .env.example .env

# Edit .env and add your Watsonx credentials
# Get API key from: https://cloud.ibm.com/iam/apikeys
# Get project ID from: https://dataplatform.cloud.ibm.com/wx/home
```

### 2. Run Database Migration

```bash
# Apply migration
alembic upgrade head
```

### 3. Start the Server

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload
```

### 4. Test the API

#### Generate Ideas
```bash
curl -X POST "http://localhost:8000/api/v1/ideas/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
    "num_ideas": 3
  }'
```

#### Get Recent Ideas
```bash
curl "http://localhost:8000/api/v1/ideas/recent?limit=5"
```

#### Get Specific Idea
```bash
curl "http://localhost:8000/api/v1/ideas/{idea_id}"
```

## API Response Example

```json
{
  "ideas": [
    {
      "id": "uuid-here",
      "title": "Bronze Resonance",
      "description": "A contemporary interpretation of Chola bronze casting...",
      "artistic_rationale": "This concept bridges ancient metallurgy with modern form...",
      "materials": "Bronze, patina finish",
      "scale": "Life-size, approximately 6 feet tall",
      "cultural_references": "Chola dynasty bronze casting, Nataraja iconography",
      "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
      "project_id": null,
      "created_at": "2026-06-15T18:00:00Z",
      "updated_at": "2026-06-15T18:00:00Z"
    }
  ],
  "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
  "generated_at": "2026-06-15T18:00:00Z",
  "model_used": "ibm/granite-13b-instruct-v2"
}
```

## Key Features

### 1. Prompt Engineering
- Structured prompts with clear instructions
- JSON output format for reliable parsing
- Context-aware generation

### 2. Error Handling
- Graceful degradation on API failures
- Detailed error logging
- User-friendly error messages

### 3. Performance Optimization
- Response caching (1 hour TTL)
- Singleton pattern for service instances
- Efficient database queries with indexes

### 4. Extensibility
- Template-based prompts (easy to modify)
- Modular architecture (easy to extend)
- Prepared for RAG integration (Stage 3C)

## What's NOT Included (Yet)

This is **Stage 3A only**. The following will come in later stages:

- ❌ Style DNA embeddings (Stage 3B)
- ❌ Vector database (pgvector) (Stage 3B)
- ❌ Ancient Art Knowledge Base (Stage 3C)
- ❌ RAG retrieval system (Stage 3C)
- ❌ Vision model integration (Later)

## Next Steps

### Stage 3B - Style DNA Embeddings
1. Install pgvector extension
2. Create style_profiles table
3. Implement embedding generation
4. Add similarity search

### Stage 3C - Ancient Art KB + RAG
1. Create ancient_art_chunks table
2. Implement document chunking
3. Build retrieval system
4. Integrate with idea generation

## Troubleshooting

### Issue: "Import errors" in IDE
**Solution**: These are type-checking warnings. The code will run correctly when executed.

### Issue: "Watsonx API key invalid"
**Solution**: 
1. Verify API key in `.env`
2. Check project ID is correct
3. Ensure API key has Watsonx permissions

### Issue: "Database connection failed"
**Solution**:
1. Ensure PostgreSQL is running
2. Check DATABASE_URL in `.env`
3. Run migrations: `alembic upgrade head`

### Issue: "Redis connection failed"
**Solution**:
1. Ensure Redis is running
2. Check REDIS_URL in `.env`
3. Caching will be disabled if Redis unavailable

## Architecture Decisions

### Why Singleton Pattern?
- Watsonx client initialization is expensive
- Reusing connections improves performance
- Thread-safe for FastAPI async operations

### Why Template-Based Prompts?
- Easy to modify without code changes
- Consistent prompt structure
- Version control for prompt engineering

### Why Repository Pattern?
- Separates data access from business logic
- Makes testing easier
- Allows database changes without affecting services

### Why Caching?
- Reduces API costs
- Improves response time
- Handles duplicate requests efficiently

## Testing Checklist

- [ ] Environment variables configured
- [ ] Database migration applied
- [ ] Server starts without errors
- [ ] Health check endpoint responds
- [ ] Idea generation works
- [ ] Ideas are saved to database
- [ ] Ideas can be retrieved
- [ ] Ideas can be updated
- [ ] Ideas can be deleted
- [ ] Error handling works correctly

## Resources

- [IBM Watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check logs in the terminal
4. Verify environment configuration

---

**Status**: ✅ Stage 3A Complete
# Stage 3A - Watsonx.ai Prompt Engine Implementation

## Overview

Stage 3A implements the **Watsonx.ai Prompt Engine** for AI-powered sculpture concept generation. This is the foundation for the RAG system that will be built in later stages.

## Architecture

```
React Frontend
      ↓
FastAPI Gateway
      ↓
Idea Service
      ↓
Watsonx Service
      ↓
IBM Watsonx.ai API
      ↓
Idea Cards (Database)
```

## What Was Implemented

### 1. Watsonx Integration Layer (`integrations/watsonx.ai/`)

#### [`clients.py`](integrations/watsonx.ai/clients.py)
- **WatsonxClient**: Handles all communication with IBM Watsonx.ai
- Authentication with IBM Cloud
- Model initialization and management
- Three specialized generation methods:
  - `generate_ideas()`: Creative idea generation (temperature=0.8)
  - `generate_critique()`: Balanced analysis (temperature=0.5)
  - `analyze_style()`: Style analysis (temperature=0.6)
- Health check functionality

#### [`prompts.py`](integrations/watsonx.ai/prompts.py)
- **IDEA_GENERATION_PROMPT**: Template for generating sculpture concepts
- **CRITIQUE_PROMPT**: Template for critiquing concepts
- **STYLE_DNA_PROMPT**: Template for style analysis
- `format_prompt()`: Helper function for template formatting

#### [`parser.py`](integrations/watsonx.ai/parser.py)
- `parse_idea_cards()`: Converts raw LLM output to structured idea cards
- `parse_critique()`: Parses critique responses
- `parse_style_dna()`: Parses style analysis
- JSON extraction and validation
- Error handling and recovery

### 2. Backend Services

#### [`watsonx_service.py`](backend/app/services/watsonx_service.py)
- **WatsonxService**: Business logic layer for Watsonx operations
- Orchestrates prompt formatting, API calls, and parsing
- Error handling and logging
- Singleton pattern for efficient resource usage

#### [`idea_service.py`](backend/app/services/idea_service.py)
- **IdeaService**: Business logic for idea management
- Generates ideas via Watsonx
- Persists ideas to database
- Implements caching for performance
- CRUD operations for ideas

### 3. Data Layer

#### [`idea.py` (Model)](backend/app/models/idea.py)
Database model with fields:
- Core content: title, description, artistic_rationale
- Optional details: materials, scale, cultural_references
- Metadata: brief, project_id
- Timestamps: created_at, updated_at

#### [`idea_repo.py`](backend/app/repositories/idea_repo.py)
Repository pattern with methods:
- `get_by_project()`: Filter by project
- `get_by_brief()`: Filter by brief
- `get_recent()`: Get latest ideas
- `search_by_title()`: Search functionality
- `count_by_project()`: Count ideas

#### [`idea.py` (Schemas)](backend/app/schemas/idea.py)
Pydantic schemas:
- `IdeaGenerateRequest`: Input for generation
- `IdeaCardResponse`: Output format
- `IdeaGenerateResponse`: Batch generation response
- `IdeaUpdateRequest`: Update operations

### 4. API Endpoints ([`ideas.py`](backend/app/api/v1/ideas.py))

```
POST   /api/v1/ideas/generate          - Generate new ideas
GET    /api/v1/ideas                   - List all ideas (paginated)
GET    /api/v1/ideas/recent            - Get recent ideas
GET    /api/v1/ideas/project/{id}      - Get project ideas
GET    /api/v1/ideas/{id}              - Get specific idea
PUT    /api/v1/ideas/{id}              - Update idea
DELETE /api/v1/ideas/{id}              - Delete idea
```

### 5. Configuration

#### Environment Variables ([`.env`](backend/.env))
```bash
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-13b-instruct-v2
```

#### Database Migration
- Created migration: [`add_ideas_table.py`](backend/migrations/versions/add_ideas_table.py)
- Includes indexes on title and project_id
- Foreign key to projects table

## How to Use

### 1. Setup Environment

```bash
# Navigate to backend
cd backend

# Copy environment template
cp .env.example .env

# Edit .env and add your Watsonx credentials
# Get API key from: https://cloud.ibm.com/iam/apikeys
# Get project ID from: https://dataplatform.cloud.ibm.com/wx/home
```

### 2. Run Database Migration

```bash
# Apply migration
alembic upgrade head
```

### 3. Start the Server

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload
```

### 4. Test the API

#### Generate Ideas
```bash
curl -X POST "http://localhost:8000/api/v1/ideas/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
    "num_ideas": 3
  }'
```

#### Get Recent Ideas
```bash
curl "http://localhost:8000/api/v1/ideas/recent?limit=5"
```

#### Get Specific Idea
```bash
curl "http://localhost:8000/api/v1/ideas/{idea_id}"
```

## API Response Example

```json
{
  "ideas": [
    {
      "id": "uuid-here",
      "title": "Bronze Resonance",
      "description": "A contemporary interpretation of Chola bronze casting...",
      "artistic_rationale": "This concept bridges ancient metallurgy with modern form...",
      "materials": "Bronze, patina finish",
      "scale": "Life-size, approximately 6 feet tall",
      "cultural_references": "Chola dynasty bronze casting, Nataraja iconography",
      "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
      "project_id": null,
      "created_at": "2026-06-15T18:00:00Z",
      "updated_at": "2026-06-15T18:00:00Z"
    }
  ],
  "brief": "Create a modern sculpture inspired by Chola bronze aesthetics",
  "generated_at": "2026-06-15T18:00:00Z",
  "model_used": "ibm/granite-13b-instruct-v2"
}
```

## Key Features

### 1. Prompt Engineering
- Structured prompts with clear instructions
- JSON output format for reliable parsing
- Context-aware generation

### 2. Error Handling
- Graceful degradation on API failures
- Detailed error logging
- User-friendly error messages

### 3. Performance Optimization
- Response caching (1 hour TTL)
- Singleton pattern for service instances
- Efficient database queries with indexes

### 4. Extensibility
- Template-based prompts (easy to modify)
- Modular architecture (easy to extend)
- Prepared for RAG integration (Stage 3C)

## What's NOT Included (Yet)

This is **Stage 3A only**. The following will come in later stages:

- ❌ Style DNA embeddings (Stage 3B)
- ❌ Vector database (pgvector) (Stage 3B)
- ❌ Ancient Art Knowledge Base (Stage 3C)
- ❌ RAG retrieval system (Stage 3C)
- ❌ Vision model integration (Later)

## Next Steps

### Stage 3B - Style DNA Embeddings
1. Install pgvector extension
2. Create style_profiles table
3. Implement embedding generation
4. Add similarity search

### Stage 3C - Ancient Art KB + RAG
1. Create ancient_art_chunks table
2. Implement document chunking
3. Build retrieval system
4. Integrate with idea generation

## Troubleshooting

### Issue: "Import errors" in IDE
**Solution**: These are type-checking warnings. The code will run correctly when executed.

### Issue: "Watsonx API key invalid"
**Solution**: 
1. Verify API key in `.env`
2. Check project ID is correct
3. Ensure API key has Watsonx permissions

### Issue: "Database connection failed"
**Solution**:
1. Ensure PostgreSQL is running
2. Check DATABASE_URL in `.env`
3. Run migrations: `alembic upgrade head`

### Issue: "Redis connection failed"
**Solution**:
1. Ensure Redis is running
2. Check REDIS_URL in `.env`
3. Caching will be disabled if Redis unavailable

## Architecture Decisions

### Why Singleton Pattern?
- Watsonx client initialization is expensive
- Reusing connections improves performance
- Thread-safe for FastAPI async operations

### Why Template-Based Prompts?
- Easy to modify without code changes
- Consistent prompt structure
- Version control for prompt engineering

### Why Repository Pattern?
- Separates data access from business logic
- Makes testing easier
- Allows database changes without affecting services

### Why Caching?
- Reduces API costs
- Improves response time
- Handles duplicate requests efficiently

## Testing Checklist

- [ ] Environment variables configured
- [ ] Database migration applied
- [ ] Server starts without errors
- [ ] Health check endpoint responds
- [ ] Idea generation works
- [ ] Ideas are saved to database
- [ ] Ideas can be retrieved
- [ ] Ideas can be updated
- [ ] Ideas can be deleted
- [ ] Error handling works correctly

## Resources

- [IBM Watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check logs in the terminal
4. Verify environment configuration

---

**Status**: ✅ Stage 3A Complete
**Next**: Stage 3B - Style DNA Embeddings
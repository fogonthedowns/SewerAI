# Sewer AI - Municipal Infrastructure Analysis

**AI-powered conversational interface**

Built for to gain actionable insights from 5GB+ of historical inspection records.

## Quick Start

```bash
# Backend (Flask API + AI)
make install && make run        # Starts on :5001

# Frontend (React UI)  
cd frontend && make install && make run  # Starts on :3000
```

**Demo:** Open http://localhost:3000 and ask "What cities have the most inspections?"

## Architecture Decisions

### Data Processing
- **S3 Streaming**: Process 5GB JSONL files without loading into memory
- **No Database**: Direct S3 access for simplicity, scales via streaming
- **Real-time Analysis**: 300-500 records processed in ~0.3s

### AI Integration
- **OpenAI GPT-3.5**: Natural language → data insights
- **Context-Aware**: AI receives relevant data subset based on query type
- **Structured Responses**: Returns both conversational answer + table data

### Tech Stack
- **Backend**: Python Flask + OpenAI + S3 streaming
- **Frontend**: React + Axios + sortable data tables
- **Communication**: RESTful JSON API with CORS

## API Endpoints

```bash
GET  /api/cities           # Cities with inspection counts
GET  /api/inspection-types # Project types analysis  
GET  /api/inspections      # Individual records (with filters)
POST /api/chat            # AI-powered natural language queries
```

## Sample Queries

- "What cities have the most sewer inspections?"
- "Show me emergency inspections by city"  
- "What kind of inspection projects are in this data?"
- "Which cities should we prioritize for infrastructure investment?"

## Key Features

- ✅ **5GB Data Processing**: Streams without memory issues
- ✅ **AI Analysis**: Conversational insights from real data  
- ✅ **Interactive Tables**: Sortable results for engineers
- ✅ **Real-time**: Sub-second response times
- ✅ **Professional UI**: Clean interface for infrastructure teams

## Production Considerations

**Database**: Migrate from S3 streaming → PostgreSQL with proper indexing
**Authentication**: Add JWT-based auth with role-based access
**Caching**: Redis for frequent queries and AI responses  
**Monitoring**: Structured logging + performance metrics
**Scaling**: Load balancers + CDN for static assets

## Environment Setup

```bash
# Backend requires
export OPENAI_API_KEY="your-key-here"

# Optional: Custom S3 bucket
export S3_BUCKET="your-bucket-name"
```

Built in 1h45m for rapid prototyping and demonstration of architectural decisions balancing performance, user experience, and technical constraints.
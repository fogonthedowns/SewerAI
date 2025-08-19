# Sewer AI - Municipal Infrastructure Analysis

**Thank you**

Thank you for considering me for this role.

- [Justin Zollars](https://www.linkedin.com/in/justinzollars/)

**AI-powered conversational interface**

Built for infrastructure engineers and city planners to gain actionable insights from 5GB+ of historical inspection records.

## Quick Start

```bash
export  OPENAI_API_KEY=""
source .env
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

## API Reference

### Data Sources
```bash
# Discover available files
curl http://localhost:5001/api/files

# API overview
curl http://localhost:5001/
```

### Inspection Records
```bash
# Basic pagination
curl "http://localhost:5001/api/inspections?limit=10&offset=0"
curl "http://localhost:5001/api/inspections?limit=10&offset=10"

# Filter by city
curl "http://localhost:5001/api/inspections?city=Chicago&limit=5"
curl "http://localhost:5001/api/inspections?city=Philadelphia&limit=5"

# Query specific data files
curl "http://localhost:5001/api/inspections?file=part1&limit=10"
curl "http://localhost:5001/api/inspections?file=part2&limit=10" 
curl "http://localhost:5001/api/inspections?file=part5&limit=10"

# Combined filters
curl "http://localhost:5001/api/inspections?file=part1&city=Denver&limit=5"
```

### Analysis Endpoints
```bash
# Cities with inspection counts
curl http://localhost:5001/api/cities
curl "http://localhost:5001/api/cities?limit=200"

# Inspection types breakdown  
curl http://localhost:5001/api/inspection-types
curl "http://localhost:5001/api/inspection-types?limit=300"

# Quick overview statistics
curl http://localhost:5001/api/stats
```

### AI-Powered Chat
```bash
# Cities analysis
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What cities have the most sewer inspections?"}'

# Project types
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What kind of inspection projects are in this data?"}'

# Emergency analysis
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me emergency inspections by city"}'

# Infrastructure planning
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Which cities should we prioritize for infrastructure investment?"}'

# Data overview
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Give me an overview of this sewer inspection data"}'

# Contractor analysis
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Which contractors perform the most inspections?"}'
```

### Pretty JSON Output (with jq)
```bash
# Formatted city analysis
curl -s http://localhost:5001/api/cities | jq

# Formatted AI response
curl -s -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What cities have the most inspections?"}' | jq

# Formatted inspection data
curl -s "http://localhost:5001/api/inspections?limit=5" | jq
```

## Sample Queries

- "What cities have the most sewer inspections?"
- "Show me emergency inspections by city"  
- "What kind of inspection projects are in this data?"
- "Which cities should we prioritize for infrastructure investment?"
- "Which contractors perform the most work?"
- "What's the condition of pipes over 30 years old?"

## Key Features

- ✅ **5GB Data Processing**: Streams without memory issues
- ✅ **AI Analysis**: Conversational insights from real data  
- ✅ **Interactive Tables**: Sortable results for engineers
- ✅ **Real-time**: Sub-second response times
- ✅ **Professional UI**: Clean interface for infrastructure teams
- ✅ **File-Specific Queries**: Target specific data sources
- ✅ **Pagination**: Handle large result sets efficiently

## Data Sources

**Available Files**: part1, part2, part5 (parts 3 & 4 not available)
**Total Size**: ~5GB of municipal sewer inspection records
**Format**: JSONL with structured inspection data including location, pipe details, defects, scores

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
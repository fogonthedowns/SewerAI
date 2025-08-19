from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
from processor import SewerDataProcessor
from ai_service import SewerAIService

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
processor = SewerDataProcessor()
ai_service = SewerAIService()

# API overview and available endpoints
@app.route('/')
def home():
    return jsonify({
        "api": "Sewer Inspection AI API",
        "data_sources": {
            "available_files": ["part1", "part2", "part5"],
            "total_size": "~5GB",
            "note": "Files part3 and part4 are not available"
        },
        "endpoints": [
            "GET /api/inspections?limit=100&offset=0&city=Chicago&file=part1",
            "GET /api/files - List available data files",
            "GET /api/cities", 
            "GET /api/inspection-types",
            "GET /api/stats",
            "POST /api/chat"
        ]
    })

# List available data files with info
@app.route('/api/files')
def get_files():
    """GET /api/files - List available data files"""
    files_info = []
    
    for i, filename in enumerate(processor.files):
        # Get a quick sample to show file info
        sample_count = 0
        for record in processor.stream_file(filename):
            sample_count += 1
            if sample_count >= 10:  # Just count first 10 for speed
                break
        
        part_name = filename.replace('sewer-inspections-', '').replace('.jsonl', '')
        files_info.append({
            "file": part_name,
            "filename": filename,
            "status": "available",
            "sample_records": sample_count
        })
    
    return jsonify({
        "available_files": files_info,
        "total_files": len(files_info),
        "missing_files": ["part3", "part4"]
    })

# AI chat interface for data analysis
@app.route('/api/chat', methods=['POST'])
def chat():
    """POST /api/chat - AI-powered conversational analysis"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        user_query = data['query']
        logger.info(f"Processing AI query: {user_query}")
        
        # Process query with AI
        result = ai_service.analyze_query(user_query)
        
        return jsonify({
            'status': 'success',
            'query': result['query'],
            'response': result['response'],
            'table_data': result.get('data'),
            'summary': result.get('data_summary'),
            'has_error': 'error' in result
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'response': 'I encountered an error processing your question. Please try again.'
        }), 500

# Get inspection records with pagination and filters
@app.route('/api/inspections')
def get_inspections():
    """GET /api/inspections - List inspection records with pagination and file filtering"""
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    city = request.args.get('city')
    file_filter = request.args.get('file')  # e.g., 'part1', 'part2', 'part5'
    
    inspections = []
    count = 0
    skipped = 0
    
    # Determine which files to process
    if file_filter:
        target_filename = f"sewer-inspections-{file_filter}.jsonl"
        if target_filename in processor.files:
            file_iterator = [processor.stream_file(target_filename)]
        else:
            return jsonify({'error': f'File {file_filter} not available. Available: part1, part2, part5'}), 400
    else:
        file_iterator = [processor.stream_file(f) for f in processor.files]
    
    # Process files
    for file_stream in file_iterator:
        for record in file_stream:
            # Apply filters
            if city and record.get('location', {}).get('city') != city:
                continue
            
            # Handle offset (skip records)
            if skipped < offset:
                skipped += 1
                continue
                
            inspections.append({
                'id': record.get('id'),
                'type': record.get('inspection_type'),
                'city': record.get('location', {}).get('city'),
                'state': record.get('location', {}).get('state'),
                'score': record.get('inspection_score'),
                'contractor': record.get('crew', {}).get('contractor'),
                'date': record.get('timestamp_utc', '').split('T')[0],  # Just date part
                'source_file': file_filter if file_filter else 'multiple'
            })
            
            count += 1
            if count >= limit:
                break
        
        if count >= limit:
            break
    
    # Calculate pagination info
    has_more = count == limit  # If we got full limit, there might be more
    next_offset = offset + limit if has_more else None
    
    return jsonify({
        'data': inspections, 
        'count': len(inspections),
        'filters': {
            'city': city,
            'file': file_filter
        },
        'pagination': {
            'offset': offset,
            'limit': limit,
            'has_more': has_more,
            'next_offset': next_offset
        }
    })

# List cities with inspection counts
@app.route('/api/cities')
def get_cities():
    """GET /api/cities - List cities with inspection counts"""
    limit = request.args.get('limit', 500, type=int)
    analysis = processor.analyze_cities(limit)
    
    cities = []
    for city, count in analysis['top_cities']:
        cities.append({
            'name': city,
            'inspection_count': count,
            'percentage': round((count/analysis['total_records_analyzed'])*100, 1)
        })
        
    return jsonify({
        'data': cities, 
        'total_analyzed': analysis['total_records_analyzed']
    })

# List inspection types with counts
@app.route('/api/inspection-types')
def get_inspection_types():
    """GET /api/inspection-types - List inspection types with counts"""
    limit = request.args.get('limit', 500, type=int)
    analysis = processor.analyze_projects(limit)
    
    types = []
    for insp_type, count in analysis['inspection_types']:
        types.append({
            'name': insp_type,
            'count': count,
            'percentage': round((count/analysis['total_records_analyzed'])*100, 1)
        })
        
    return jsonify({
        'data': types, 
        'total_analyzed': analysis['total_records_analyzed']
    })

# Quick overview statistics
@app.route('/api/stats')
def get_stats():
    """GET /api/stats - Quick overview statistics"""
    city_analysis = processor.analyze_cities(200)
    project_analysis = processor.analyze_projects(200)
    
    return jsonify({
        'cities': city_analysis['unique_cities'],
        'states': city_analysis['unique_states'],
        'inspection_types': len(project_analysis['inspection_types']),
        'sample_size': 200
    })

if __name__ == '__main__':
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment")
        print("   AI chat functionality will be limited")
    else:
        print("✅ OpenAI API key loaded")
    
    print("🚀 Starting Sewer AI API on port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001)
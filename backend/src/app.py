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

@app.route('/')
def home():
    return jsonify({
        "api": "Sewer Inspection AI API",
        "endpoints": [
            "GET /api/inspections",
            "GET /api/cities", 
            "GET /api/inspection-types",
            "GET /api/stats",
            "POST /api/chat"
        ]
    })

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

@app.route('/api/inspections')
def get_inspections():
    """GET /api/inspections - List inspection records"""
    limit = request.args.get('limit', 100, type=int)
    city = request.args.get('city')
    
    inspections = []
    count = 0
    
    for record in processor.stream_all_files():
        if city and record.get('location', {}).get('city') != city:
            continue
            
        inspections.append({
            'id': record.get('id'),
            'type': record.get('inspection_type'),
            'city': record.get('location', {}).get('city'),
            'state': record.get('location', {}).get('state'),
            'score': record.get('inspection_score'),
            'contractor': record.get('crew', {}).get('contractor')
        })
        
        count += 1
        if count >= limit:
            break
            
    return jsonify({
        'data': inspections, 
        'count': len(inspections)
    })

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
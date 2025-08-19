import os
import json
import openai
from processor import SewerDataProcessor

class SewerAIService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.processor = SewerDataProcessor()
        
    def analyze_query(self, user_query: str) -> dict:
        """Process natural language query and return structured response"""
        
        # Determine what data to fetch based on query
        data_context = self._get_relevant_data(user_query)
        
        # Create system prompt with data context
        system_prompt = self._build_system_prompt(data_context)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "query": user_query,
                "response": ai_response,
                "data": data_context.get("table_data"),
                "data_summary": data_context.get("summary")
            }
            
        except Exception as e:
            return {
                "query": user_query,
                "response": f"I encountered an error processing your question: {str(e)}",
                "data": None,
                "error": str(e)
            }
    
    def _get_relevant_data(self, query: str) -> dict:
        """Fetch relevant data based on query content"""
        query_lower = query.lower()
        
        # Determine query type and fetch appropriate data
        if any(word in query_lower for word in ['city', 'cities', 'location', 'where']):
            return self._get_city_data()
        elif any(word in query_lower for word in ['project', 'inspection', 'type', 'kind']):
            return self._get_project_data()
        elif any(word in query_lower for word in ['emergency', 'urgent', 'critical']):
            return self._get_emergency_data()
        else:
            # Default to general overview
            return self._get_overview_data()
    
    def _get_city_data(self) -> dict:
        """Get city analysis data"""
        analysis = self.processor.analyze_cities(limit=1000)  # Increased from 300
        
        table_data = {
            "columns": ["City", "Inspections", "Percentage"],
            "rows": [[city, count, f"{(count/analysis['total_records_analyzed']*100):.1f}%"] 
                    for city, count in analysis['top_cities'][:15]]  # Show top 15 instead of 10
        }
        
        return {
            "type": "cities",
            "table_data": table_data,
            "summary": f"Analysis of {analysis['total_records_analyzed']} inspections across {analysis['unique_cities']} cities in {analysis['unique_states']} states from 3 available data files"
        }
    
    def _get_project_data(self) -> dict:
        """Get project/inspection type analysis"""
        analysis = self.processor.analyze_projects(limit=1000)  # Increased from 300
        
        table_data = {
            "columns": ["Inspection Type", "Count", "Percentage"],
            "rows": [[insp_type, count, f"{(count/analysis['total_records_analyzed']*100):.1f}%"] 
                    for insp_type, count in analysis['inspection_types'][:15]]  # Show more results
        }
        
        return {
            "type": "projects",
            "table_data": table_data,
            "summary": f"Analysis of {analysis['total_records_analyzed']} inspections showing {len(analysis['inspection_types'])} different inspection types from 3 data files"
        }
    
    def _get_emergency_data(self) -> dict:
        """Get emergency inspection data"""
        inspections = []
        count = 0
        
        for record in self.processor.stream_all_files():
            if record.get('inspection_type', '').lower() == 'emergency':
                inspections.append([
                    record.get('location', {}).get('city', 'Unknown'),
                    record.get('location', {}).get('state', 'Unknown'),
                    record.get('inspection_score', 'N/A'),
                    record.get('crew', {}).get('contractor', 'Unknown')
                ])
                count += 1
                if count >= 20:  # Limit for performance
                    break
        
        table_data = {
            "columns": ["City", "State", "Score", "Contractor"],
            "rows": inspections
        }
        
        return {
            "type": "emergency",
            "table_data": table_data,
            "summary": f"Found {len(inspections)} emergency inspections"
        }
    
    def _get_overview_data(self) -> dict:
        """Get general overview data"""
        city_analysis = self.processor.analyze_cities(200)
        project_analysis = self.processor.analyze_projects(200)
        
        # Create a summary table
        table_data = {
            "columns": ["Metric", "Value"],
            "rows": [
                ["Total Cities", city_analysis['unique_cities']],
                ["Total States", city_analysis['unique_states']],
                ["Inspection Types", len(project_analysis['inspection_types'])],
                ["Sample Analyzed", city_analysis['total_records_analyzed']]
            ]
        }
        
        return {
            "type": "overview",
            "table_data": table_data,
            "summary": f"Overview of sewer inspection data from {city_analysis['unique_cities']} cities"
        }
    
    def _build_system_prompt(self, data_context: dict) -> str:
        """Build system prompt with data context"""
        
        base_prompt = """You are an expert infrastructure analyst specializing in municipal sewer inspection data. 
You help infrastructure engineers and city planners understand inspection data and make informed decisions.

Be conversational, professional, and provide actionable insights. Focus on trends, patterns, and recommendations.
Keep responses concise but informative. Always relate findings back to infrastructure management needs.

Current data context: """
        
        context_info = f"""
Data Type: {data_context.get('type', 'general')}
Summary: {data_context.get('summary', 'Municipal sewer inspection data')}

When responding:
1. Answer the user's question directly
2. Highlight key insights from the data
3. Provide practical recommendations for infrastructure teams
4. Mention that detailed data is available in the table below your response
"""
        
        return base_prompt + context_info
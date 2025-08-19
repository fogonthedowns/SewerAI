import requests
import json
from typing import Iterator, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SewerDataProcessor:
    def __init__(self):
        self.base_url = "https://sewerai-public.s3.us-west-2.amazonaws.com/"
        self.files = [f"sewer-inspections-part{i}.jsonl" for i in range(1, 6)]
        
    def stream_file(self, filename: str) -> Iterator[Dict]:
        """Stream JSONL records from a single S3 file"""
        url = f"{self.base_url}{filename}"
        logger.info(f"Streaming from: {url}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            buffer = ""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    # Decode bytes to string
                    chunk_str = chunk.decode('utf-8', errors='ignore')
                    buffer += chunk_str
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            try:
                                record = json.loads(line)
                                yield record
                            except json.JSONDecodeError as e:
                                logger.warning(f"Skipping invalid JSON line: {e}")
                                continue
                                
        except requests.RequestException as e:
            logger.error(f"Error streaming file {filename}: {e}")
            return
    
    def stream_all_files(self, limit_per_file: int = None) -> Iterator[Dict]:
        """Stream records from all 5 S3 files"""
        for filename in self.files:
            logger.info(f"Processing file: {filename}")
            count = 0
            
            for record in self.stream_file(filename):
                yield record
                count += 1
                
                if limit_per_file and count >= limit_per_file:
                    logger.info(f"Reached limit of {limit_per_file} records for {filename}")
                    break
                    
            logger.info(f"Finished processing {filename} - streamed {count} records")
    
    def get_sample_data(self, sample_size: int = 100) -> List[Dict]:
        """Get a sample of records for quick analysis"""
        records = []
        for record in self.stream_all_files():
            records.append(record)
            if len(records) >= sample_size:
                break
        return records
    
    def analyze_cities(self, limit: int = 1000) -> Dict:
        """Analyze what kind of cities are in the dataset"""
        cities = {}
        states = {}
        districts = {}
        
        count = 0
        for record in self.stream_all_files():
            if count >= limit:
                break
                
            location = record.get('location', {})
            city = location.get('city')
            state = location.get('state') 
            district = location.get('district')
            
            if city:
                cities[city] = cities.get(city, 0) + 1
            if state:
                states[state] = states.get(state, 0) + 1
            if district:
                districts[district] = districts.get(district, 0) + 1
                
            count += 1
        
        return {
            'total_records_analyzed': count,
            'unique_cities': len(cities),
            'unique_states': len(states), 
            'unique_districts': len(districts),
            'top_cities': sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10],
            'top_states': sorted(states.items(), key=lambda x: x[1], reverse=True)[:10],
            'top_districts': sorted(districts.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def analyze_projects(self, limit: int = 1000) -> Dict:
        """Analyze what kind of projects/inspections are in the dataset"""
        inspection_types = {}
        equipment_types = {}
        contractors = {}
        
        count = 0
        for record in self.stream_all_files():
            if count >= limit:
                break
                
            inspection_type = record.get('inspection_type')
            equipment = record.get('equipment', {})
            crew = record.get('crew', {})
            
            if inspection_type:
                inspection_types[inspection_type] = inspection_types.get(inspection_type, 0) + 1
                
            eq_type = equipment.get('type')
            if eq_type:
                equipment_types[eq_type] = equipment_types.get(eq_type, 0) + 1
                
            contractor = crew.get('contractor')
            if contractor:
                contractors[contractor] = contractors.get(contractor, 0) + 1
                
            count += 1
        
        return {
            'total_records_analyzed': count,
            'inspection_types': sorted(inspection_types.items(), key=lambda x: x[1], reverse=True),
            'equipment_types': sorted(equipment_types.items(), key=lambda x: x[1], reverse=True),
            'top_contractors': sorted(contractors.items(), key=lambda x: x[1], reverse=True)[:10]
        }

# Quick test function
def test_streaming():
    processor = SewerDataProcessor()
    
    print("Testing S3 streaming...")
    count = 0
    for record in processor.stream_all_files(limit_per_file=5):  # Just 5 per file for test
        print(f"Record {count + 1}: ID={record.get('id')}, City={record.get('location', {}).get('city')}")
        count += 1
        if count >= 15:  # Total of 15 records across all files
            break
    
    print(f"\nSuccessfully streamed {count} records from S3!")

if __name__ == "__main__":
    test_streaming()
#!/usr/bin/env python3
"""
Quick test to verify S3 streaming works
Run this first to make sure everything is working
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.append('src')

from processor import SewerDataProcessor
import time

def main():
    print("🧪 Testing Sewer AI S3 Streaming")
    print("=" * 40)
    
    processor = SewerDataProcessor()
    
    # Test 1: Basic connection and streaming
    print("\n📡 Test 1: Basic S3 Connection")
    print("Attempting to stream first few records...")
    
    try:
        start_time = time.time()
        count = 0
        
        for record in processor.stream_all_files(limit_per_file=3):
            count += 1
            city = record.get('location', {}).get('city', 'Unknown')
            inspection_type = record.get('inspection_type', 'Unknown')
            record_id = record.get('id', 'Unknown')
            
            print(f"  ✓ Record {count}: {record_id} | {city} | {inspection_type}")
            
            if count >= 15:  # 5 files × 3 records each
                break
        
        elapsed = time.time() - start_time
        print(f"✅ Streamed {count} records in {elapsed:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Streaming failed: {e}")
        return False
    
    # Test 2: City analysis
    print("\n🏙️ Test 2: City Analysis")
    try:
        start_time = time.time()
        cities = processor.analyze_cities(limit=200)
        elapsed = time.time() - start_time
        
        print(f"✅ Analyzed {cities['total_records_analyzed']} records in {elapsed:.2f}s")
        print(f"   Found {cities['unique_cities']} cities in {cities['unique_states']} states")
        print(f"   Top 3 cities: {cities['top_cities'][:3]}")
        
    except Exception as e:
        print(f"❌ City analysis failed: {e}")
        return False
    
    # Test 3: Project analysis
    print("\n🔧 Test 3: Project Analysis")
    try:
        start_time = time.time()
        projects = processor.analyze_projects(limit=200)
        elapsed = time.time() - start_time
        
        print(f"✅ Analyzed {projects['total_records_analyzed']} records in {elapsed:.2f}s")
        print(f"   Found {len(projects['inspection_types'])} inspection types")
        print(f"   Top inspection types: {projects['inspection_types'][:3]}")
        
    except Exception as e:
        print(f"❌ Project analysis failed: {e}")
        return False
    
    print("\n🎉 All tests passed!")
    print("👉 Ready to run: python src/app.py")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
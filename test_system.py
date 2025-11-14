#!/usr/bin/env python3
"""
System Test Script - NATO PMP Analyzer
"""

import sys
from pathlib import Path

print("=" * 60)
print("🔍 NATO PMP ANALYZER - SYSTEM TEST")
print("=" * 60)

# Test 1: Python version
print("\n✓ Python version:", sys.version.split()[0])

# Test 2: Import backend modules
print("\n📦 Testing Backend Imports...")
try:
    from backend.document_processor import DocumentProcessor
    print("  ✅ DocumentProcessor imported")
except Exception as e:
    print(f"  ❌ DocumentProcessor: {e}")
    sys.exit(1)

try:
    from backend.relationship_analyzer import RelationshipAnalyzer
    print("  ✅ RelationshipAnalyzer imported")
except Exception as e:
    print(f"  ❌ RelationshipAnalyzer: {e}")
    sys.exit(1)

try:
    from backend.rag_engine import RAGEngine
    print("  ✅ RAGEngine imported")
except Exception as e:
    print(f"  ❌ RAGEngine: {str(e)[:100]}...")

# Test 3: Test DocumentProcessor
print("\n🧪 Testing DocumentProcessor...")
try:
    processor = DocumentProcessor()
    print("  ✅ DocumentProcessor instantiated")
    print(f"  ✅ Supported formats: {processor.supported_formats}")
except Exception as e:
    print(f"  ❌ {e}")

# Test 4: Test RelationshipAnalyzer
print("\n🧪 Testing RelationshipAnalyzer...")
try:
    analyzer = RelationshipAnalyzer()
    print("  ✅ RelationshipAnalyzer instantiated")
    print(f"  ✅ Relationship types: {list(analyzer.relationship_types.keys())}")
    
    # Test with mock data
    mock_docs = [
        {
            'success': True,
            'file_name': 'project1.pdf',
            'metadata': {
                'project_name': 'Project Alpha',
                'status': 'GREEN',
                'stakeholders': ['alice@test.com', 'bob@test.com'],
                'budget': ['$100M'],
                'word_count': 1000
            },
            'text': 'This project uses AI and cloud technology'
        },
        {
            'success': True,
            'file_name': 'project2.pdf',
            'metadata': {
                'project_name': 'Project Beta',
                'status': 'GREEN',
                'stakeholders': ['bob@test.com', 'charlie@test.com'],
                'budget': ['$80M'],
                'word_count': 1200
            },
            'text': 'This project uses AI and security encryption'
        }
    ]
    
    network_data = analyzer.get_network_data(mock_docs)
    print(f"  ✅ Network data generated:")
    print(f"     - Nodes: {len(network_data['nodes'])}")
    print(f"     - Edges: {len(network_data['edges'])}")
    
except Exception as e:
    print(f"  ❌ {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ SYSTEM TEST COMPLETE")
print("=" * 60)

import os
import json
import traceback
from backend.rag_engine import RAGEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='.env')

print("Testing RAG initialization with saved documents...")
print(f"OpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")
api_key = os.getenv('OPENAI_API_KEY', '')
if api_key:
    print(f"API Key (first 20 chars): {api_key[:20]}...")

try:
    # Load documents
    print("\n🔄 Loading documents from processed_documents.json...")
    with open('processed_documents.json', 'r') as f:
        docs = json.load(f)
    print(f"✅ Loaded {len(docs)} documents")

    # Show document info
    print("\nDocument info:")
    for i, doc in enumerate(docs[:3]):
        print(f"  Doc {i+1}: {doc.get('file_name')}")
        print(f"    - success: {doc.get('success')}")
        print(f"    - text length: {len(doc.get('text', ''))}")
        print(f"    - has metadata: {'metadata' in doc}")

    # Create RAG engine
    print("\n🔄 Creating RAG engine...")
    rag = RAGEngine(persist_directory="./chroma_db")
    print("✅ RAG engine created")

    # Try to add documents
    print(f"\n🔄 Adding {len(docs)} documents to RAG...")
    success = rag.add_documents(docs)

    if success:
        print("✅ Documents added successfully!")

        # Test a query
        print("\n🔄 Testing query: 'What is the budget for AI projects?'")
        result = rag.query("What is the budget for AI projects?")
        answer = result.get('answer', 'No answer')
        print(f"\nAnswer: {answer[:500]}")
        print(f"\nSources: {len(result.get('sources', []))} found")
    else:
        print("❌ add_documents() returned False")
        print("\nThis could mean:")
        print("  - No documents with success=True")
        print("  - No text content in documents")
        print("  - Error during embedding generation")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"\nFull traceback:")
    print(traceback.format_exc())

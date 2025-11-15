import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv(dotenv_path='.env')

api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key from env: {api_key[:20]}...")
print(f"API Key length: {len(api_key)}")

# Test 1: Direct OpenAI client
print("\n" + "="*50)
print("TEST 1: Direct OpenAI Client")
print("="*50)
try:
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input="Test"
    )
    print("✅ Direct OpenAI Client: SUCCESS")
except Exception as e:
    print(f"❌ Direct OpenAI Client: FAILED")
    print(f"   Error: {str(e)[:200]}")

# Test 2: LangChain with api_key parameter
print("\n" + "="*50)
print("TEST 2: LangChain OpenAIEmbeddings with api_key parameter")
print("="*50)
try:
    embeddings = OpenAIEmbeddings(api_key=api_key)
    result = embeddings.embed_query("Test")
    print(f"✅ LangChain with api_key: SUCCESS (embedding dim: {len(result)})")
except Exception as e:
    print(f"❌ LangChain with api_key: FAILED")
    print(f"   Error: {str(e)[:200]}")

# Test 3: LangChain with environment variable
print("\n" + "="*50)
print("TEST 3: LangChain OpenAIEmbeddings with env var")
print("="*50)
try:
    os.environ["OPENAI_API_KEY"] = api_key
    embeddings2 = OpenAIEmbeddings()
    result2 = embeddings2.embed_query("Test")
    print(f"✅ LangChain with env var: SUCCESS (embedding dim: {len(result2)})")
except Exception as e:
    print(f"❌ LangChain with env var: FAILED")
    print(f"   Error: {str(e)[:200]}")

# Test 4: Check for special characters
print("\n" + "="*50)
print("TEST 4: API Key Analysis")
print("="*50)
print(f"First char: '{api_key[0]}' (ord: {ord(api_key[0])})")
print(f"Last char: '{api_key[-1]}' (ord: {ord(api_key[-1])})")
print(f"Contains whitespace: {any(c.isspace() for c in api_key)}")
print(f"Starts with 'sk-': {api_key.startswith('sk-')}")
print(f"Stripped length: {len(api_key.strip())}")
print(f"Original length: {len(api_key)}")

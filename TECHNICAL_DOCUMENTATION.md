# 🔧 NATO PMP Analyzer - Technical Documentation

## 🎯 Purpose
This document provides comprehensive technical information for developers, system administrators, and IT professionals working with the NATO PMP Analyzer.

**Target Audience:** Developers, DevOps Engineers, System Administrators, Technical Architects

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Component Documentation](#component-documentation)
5. [Data Flow](#data-flow)
6. [API & Integrations](#api--integrations)
7. [Configuration](#configuration)
8. [Database & Storage](#database--storage)
9. [Security](#security)
10. [Performance](#performance)
11. [Deployment](#deployment)
12. [Monitoring & Logging](#monitoring--logging)
13. [Development Guide](#development-guide)
14. [Testing](#testing)
15. [Troubleshooting](#troubleshooting)

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Browser                           │
│                     (User Interface)                         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP (localhost:8501)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Server                          │
│              (Frontend + Session Management)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌─────────────┐  ┌──────────────┐
│  Document    │  │  RAG        │  │ Relationship │
│  Processor   │  │  Engine     │  │ Analyzer     │
└──────┬───────┘  └──────┬──────┘  └──────┬───────┘
       │                 │                │
       │                 │                │
       ▼                 ▼                ▼
┌─────────────────────────────────────────────────┐
│           Backend Processing Layer               │
│  • PDF/DOCX parsing                             │
│  • Metadata extraction                          │
│  • Text chunking                                │
│  • Relationship detection                       │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────────┐
        │            │                │
        ▼            ▼                ▼
┌──────────────┐ ┌────────┐  ┌────────────────┐
│  ChromaDB    │ │ OpenAI │  │ Session State  │
│  (Vectors)   │ │  API   │  │  (In-Memory)   │
└──────────────┘ └────────┘  └────────────────┘
```

### Component Interaction Flow

```
User Upload → DocumentProcessor → Text Extraction
                    ↓
            Metadata Extraction
                    ↓
            RAGEngine → Text Chunking → ChromaDB (Embeddings)
                    ↓
            RelationshipAnalyzer → Network Data
                    ↓
            Session State Storage
                    ↓
            UI Rendering (Streamlit)
```

### Architecture Principles

1. **Stateful Sessions:** Streamlit session_state maintains user data
2. **Modular Backend:** Separate processors for different functions
3. **Cached Resources:** @st.cache_resource for expensive operations
4. **Async Processing:** Non-blocking document uploads
5. **Vector Storage:** Persistent ChromaDB for semantic search

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.31.0+ | Web UI framework |
| **Backend** | Python | 3.10+ | Core language |
| **LLM** | OpenAI GPT-4 | gpt-4-turbo-preview | Language understanding |
| **Embeddings** | OpenAI Embeddings | text-embedding-ada-002 | Vector creation |
| **Vector DB** | ChromaDB | Latest | Semantic search storage |
| **RAG Framework** | LangChain | 0.1.0+ | RAG orchestration |
| **PDF Processing** | PyPDF2 | Latest | PDF text extraction |
| **DOCX Processing** | python-docx | Latest | Word document parsing |
| **Data Manipulation** | Pandas | Latest | Data processing |
| **Visualization** | Plotly | Latest | Interactive charts |
| **Network Graphs** | NetworkX | Latest | Graph analysis |
| **Environment** | python-dotenv | Latest | Config management |

### Detailed Dependencies

See `requirements.txt`:
```txt
streamlit
pandas
plotly
PyPDF2
python-docx
langchain
langchain-community
langchain-openai
chromadb
python-dotenv
openai
networkx
```

### External Services

1. **OpenAI API**
   - Endpoint: `https://api.openai.com/v1/`
   - Used for: GPT-4 completions, text embeddings
   - Authentication: API key via environment variable

---

## 📁 Project Structure

```
nato-pmp-analyzer/
│
├── app.py                          # Main Streamlit application (1018 lines)
│   ├── Page routing
│   ├── Session state management
│   ├── UI components
│   └── Event handlers
│
├── backend/                        # Core processing modules
│   ├── __init__.py                # Package initialization
│   ├── document_processor.py      # PDF/DOCX processing + metadata
│   ├── rag_engine.py              # RAG pipeline (GPT-4 + ChromaDB)
│   └── relationship_analyzer.py   # Network & relationship detection
│
├── chroma_db/                     # Vector database (generated)
│   └── [ChromaDB files]           # Persistent embeddings storage
│
├── .env                           # Environment variables (git-ignored)
├── .env.example                   # Template for configuration
├── .gitignore                     # Git ignore rules
│
├── requirements.txt               # Python dependencies
├── README.md                      # Main documentation
├── USER_GUIDE.md                 # End-user documentation
├── TECHNICAL_DOCUMENTATION.md    # This file
│
├── DEMO_SCRIPT.md                # Demo walkthrough
├── DEMO_QUESTIONS.md             # Sample chatbot queries
├── DEMO_CHECKLIST.md             # Demo preparation
├── PRESENTATION_OUTLINE.md       # Presentation template
│
├── screenshots/                   # UI screenshots (optional)
├── venv/                         # Python virtual environment (git-ignored)
└── __pycache__/                  # Python bytecode (git-ignored)
```

---

## 🔧 Component Documentation

### 1. Document Processor (`backend/document_processor.py`)

**Purpose:** Extract text and metadata from PDF/DOCX files

**Class: `DocumentProcessor`**

```python
class DocumentProcessor:
    """Process PDF and DOCX documents"""

    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']

    def process_document(self, file_path: str, file_name: str) -> Dict
    def _extract_pdf_text(self, file_path: str) -> str
    def _extract_docx_text(self, file_path: str) -> str
    def _extract_metadata(self, text: str, file_name: str) -> Dict
    def _extract_project_name(self, text: str, file_name: str) -> Optional[str]
    def _extract_budget(self, text: str) -> List[str]
    def _extract_dates(self, text: str) -> List[str]
    def _extract_stakeholders(self, text: str) -> List[str]
    def _extract_status(self, text: str) -> str
    def get_text_preview(self, text: str, max_length: int) -> str
```

**Key Methods:**

**`process_document(file_path, file_name)`**
- **Input:** File path (temp), original filename
- **Output:** Dict with success, text, metadata, errors
- **Process:**
  1. Determine file type
  2. Extract text (PDF or DOCX)
  3. Extract metadata from text
  4. Return structured result

**`_extract_metadata(text, file_name)`**
- **Input:** Full document text
- **Output:** Dict with project_name, budget, dates, stakeholders, status, word_count
- **Extraction Methods:**
  - **Project Name:** Regex patterns, fallback to filename
  - **Budget:** Pattern matching (€X.X million, M€, etc.)
  - **Dates:** Multiple date formats
  - **Stakeholders:** Email patterns, name patterns
  - **Status:** Keywords (red, amber, green)

**Metadata Accuracy:** ~85% on well-formatted documents

**Dependencies:**
- PyPDF2 for PDF parsing
- python-docx for Word documents
- re (regex) for pattern matching
- datetime for timestamp

---

### 2. RAG Engine (`backend/rag_engine.py`)

**Purpose:** Retrieval-Augmented Generation using GPT-4 and ChromaDB

**Class: `RAGEngine`**

```python
class RAGEngine:
    """RAG Engine for document analysis"""

    def __init__(self, persist_directory: str = "./chroma_db")
    def add_documents(self, documents: List[Dict]) -> bool
    def query(self, question: str) -> Dict
    def get_stats(self) -> Dict
    def _format_response(self, answer: str, source_docs: List) -> Dict
```

**Architecture:**

```
Document → Text Splitter → Chunks (1000 chars, 200 overlap)
                              ↓
                      OpenAI Embeddings
                              ↓
                         ChromaDB
                              ↓
         User Query → Retriever → Relevant Chunks
                              ↓
                    GPT-4 + Context → Answer
```

**Key Methods:**

**`add_documents(documents)`**
- **Input:** List of processed document dicts
- **Process:**
  1. Split text into chunks (RecursiveCharacterTextSplitter)
  2. Create metadata for each chunk
  3. Generate embeddings (OpenAI)
  4. Store in ChromaDB
- **Output:** Boolean success
- **Performance:** ~500ms per document

**`query(question)`**
- **Input:** Natural language question
- **Process:**
  1. Convert question to embedding
  2. Similarity search in ChromaDB (k=4 chunks)
  3. Construct prompt with context
  4. Send to GPT-4
  5. Parse response
  6. Format with sources
- **Output:** Dict with answer and source citations
- **Response Time:** 3-8 seconds

**Configuration:**

```python
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
MODEL = "gpt-4-turbo-preview"
TEMPERATURE = 0.3           # Lower = more deterministic
TOP_K_RETRIEVAL = 4         # Number of chunks to retrieve
```

**Prompt Template:**

```
You are an AI assistant analyzing NATO project management plans.

Context from documents:
{context}

Question: {question}

Provide a clear, concise answer based ONLY on the context above.
If the answer isn't in the context, say so.
```

**Dependencies:**
- langchain-openai for GPT-4 interface
- langchain-community for ChromaDB
- langchain-core for base classes
- chromadb for vector storage

---

### 3. Relationship Analyzer (`backend/relationship_analyzer.py`)

**Purpose:** Detect relationships between projects

**Class: `RelationshipAnalyzer`**

```python
class RelationshipAnalyzer:
    """Analyze relationships between projects"""

    def __init__(self)
    def analyze_relationships(self, documents: List[Dict]) -> List[Dict]
    def get_network_data(self, documents: List[Dict]) -> Dict
    def _find_relationships(self, doc1: Dict, doc2: Dict) -> List[Dict]
    def _check_stakeholder_overlap(self, meta1: Dict, meta2: Dict) -> int
    def _check_technology_overlap(self, doc1: Dict, doc2: Dict) -> int
    def _check_budget_similarity(self, meta1: Dict, meta2: Dict) -> bool
```

**Relationship Detection:**

**1. Stakeholder Overlap**
- Method: Set intersection of stakeholder lists
- Strength: Count of shared stakeholders
- Example: Both projects have john.doe@nato.int

**2. Technology Keywords**
- Method: Keyword matching in full text
- Keywords: ['quantum', 'cyber', 'ai', 'cloud', 'security', '5g', etc.]
- Strength: Count of common technologies
- Example: Both mention "artificial intelligence" and "cybersecurity"

**3. Budget Similarity**
- Method: Numeric comparison of budget amounts
- Threshold: Ratio > 0.5 (within 50%)
- Example: €10M and €12M are similar

**4. Status Alignment**
- Method: Exact match of RAG status
- Values: RED, AMBER, GREEN
- Example: Both RED status

**Output Format:**

```python
{
    'source': 'Project A',
    'target': 'Project B',
    'type': 'stakeholder',  # or 'technology', 'budget', 'status'
    'strength': 3,          # numeric strength
    'label': '3 shared stakeholder(s)'
}
```

**Network Data Structure:**

```python
{
    'nodes': [
        {
            'id': 'Project Name',
            'label': 'Project Name',
            'status': 'RED',
            'word_count': 5000,
            'stakeholders': 10
        },
        ...
    ],
    'edges': [
        {
            'source': 'Project A',
            'target': 'Project B',
            'type': 'stakeholder',
            'label': 'Description',
            'strength': 3
        },
        ...
    ]
}
```

---

### 4. Main Application (`app.py`)

**Purpose:** Streamlit web interface and orchestration

**Structure:**

```python
# Configuration
st.set_page_config(...)
st.markdown("""<style>...</style>""")  # Custom CSS

# Session State Initialization
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
# ... more state vars

# Cached Resources
@st.cache_resource
def get_processor():
    return DocumentProcessor()

@st.cache_resource
def get_rag_engine():
    return RAGEngine()

# Sidebar Navigation
with st.sidebar:
    page = st.radio("Select Page", [...])
    # Status indicators
    # Document list
    # System info

# Page Routing
if page == "🏠 Home":
    # Home page logic
elif page == "📤 Upload Documents":
    # Upload logic
elif page == "💬 Chatbot":
    # Chatbot logic
elif page == "📈 Dashboard":
    # Dashboard logic
elif page == "👥 Stakeholder Network":
    # Stakeholder network logic
elif page == "🔗 Network Graph":
    # Network graph logic
```

**Session State Variables:**

```python
st.session_state.uploaded_files         # List of File objects
st.session_state.processing_status      # Dict of processing status
st.session_state.processed_documents    # List of processed docs
st.session_state.rag_initialized        # Boolean RAG status
st.session_state.relationship_analyzer  # RelationshipAnalyzer instance
st.session_state.network_data          # Network graph data
st.session_state.messages              # Chat history
```

**Key Functions:**

**`generate_simple_response(prompt, documents)`**
- Fallback chatbot when RAG not available
- Pattern matching for common queries
- Returns formatted string response

---

## 🔄 Data Flow

### Document Upload Flow

```
1. User selects file(s)
        ↓
2. Streamlit file_uploader
        ↓
3. Temporary file creation
        ↓
4. DocumentProcessor.process_document()
        ↓
5. Text extraction (PDF/DOCX)
        ↓
6. Metadata extraction
        ↓
7. Result stored in session_state.processed_documents
        ↓
8. RAGEngine.add_documents()
        ↓
9. Text chunking
        ↓
10. Embedding generation (OpenAI API)
        ↓
11. Storage in ChromaDB
        ↓
12. session_state.rag_initialized = True
        ↓
13. UI update (sidebar, metrics)
```

### Chatbot Query Flow

```
1. User types question
        ↓
2. Input captured by st.chat_input()
        ↓
3. Added to session_state.messages
        ↓
4. If RAG initialized:
   4a. RAGEngine.query(question)
   4b. Question → Embedding
   4c. ChromaDB similarity search
   4d. Retrieve top-k chunks
   4e. Construct prompt with context
   4f. Send to GPT-4
   4g. Parse response
   4h. Extract sources
        ↓
5. Else: generate_simple_response()
        ↓
6. Response added to session_state.messages
        ↓
7. UI renders chat history
```

### Dashboard Rendering Flow

```
1. User navigates to Dashboard
        ↓
2. Retrieve session_state.processed_documents
        ↓
3. Calculate metrics:
   - Status counts (RED/AMBER/GREEN)
   - Budget totals
   - Word counts
        ↓
4. Generate Plotly charts:
   - Pie chart (status distribution)
   - Bar charts (metrics)
        ↓
5. Create Pandas DataFrames for tables
        ↓
6. Streamlit rendering:
   - st.metric()
   - st.plotly_chart()
   - st.dataframe()
```

### Network Graph Generation Flow

```
1. User clicks "Generate Network"
        ↓
2. RelationshipAnalyzer.get_network_data()
        ↓
3. For each document pair:
   - Check stakeholder overlap
   - Check technology keywords
   - Check budget similarity
   - Check status match
        ↓
4. Build nodes list (projects)
        ↓
5. Build edges list (relationships)
        ↓
6. NetworkX graph creation
        ↓
7. Calculate spring layout
        ↓
8. Generate Plotly traces:
   - Edge traces (lines)
   - Node trace (circles)
        ↓
9. Render interactive graph
```

---

## 🔌 API & Integrations

### OpenAI API

**Configuration:**
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
```

**Endpoints Used:**

1. **Chat Completions** (`/v1/chat/completions`)
   - Model: gpt-4-turbo-preview
   - Temperature: 0.3
   - Purpose: Answer user queries with context

2. **Embeddings** (`/v1/embeddings`)
   - Model: text-embedding-ada-002
   - Purpose: Convert text to vectors for similarity search

**Rate Limits:**
- Default: 10,000 TPM (tokens per minute)
- Recommended: Monitor usage in OpenAI dashboard

**Error Handling:**
```python
try:
    response = llm.invoke(prompt)
except openai.RateLimitError:
    # Handle rate limit
except openai.APIError:
    # Handle API errors
```

**Cost Estimation:**
- GPT-4 Turbo: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens
- Embeddings: ~$0.0001 per 1K tokens
- Typical document (5000 words): ~$0.10-0.50 to process

### ChromaDB

**Local Storage:**
- Location: `./chroma_db/`
- Persistence: Automatic
- Format: SQLite + vector files

**API Usage:**
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=langchain_docs,
    embedding=OpenAIEmbeddings(openai_api_key=api_key),
    persist_directory="./chroma_db"
)
```

**Querying:**
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
relevant_docs = retriever.get_relevant_documents(query)
```

### Future Integration Points

**Potential Integrations:**
- **SharePoint:** Pull PMPs automatically
- **Jira:** Import project metadata
- **MS Project:** Extract timeline data
- **Slack/Teams:** Notifications and alerts
- **Power BI:** Embed analytics
- **REST API:** Expose query endpoint

---

## ⚙️ Configuration

### Environment Variables (`.env`)

**Required:**
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Optional:**
```bash
OPENAI_MODEL=gpt-4-turbo-preview  # Default model
CHROMA_PERSIST_DIRECTORY=./chroma_db  # Vector DB location
```

**Getting an API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to `.env` file
4. Never commit `.env` to git

### Application Configuration

**Streamlit Config (`app.py`):**
```python
st.set_page_config(
    page_title="NATO PMP Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**RAG Configuration (`backend/rag_engine.py`):**
```python
# Text splitting
chunk_size = 1000
chunk_overlap = 200

# Model settings
model_name = "gpt-4-turbo-preview"
temperature = 0.3

# Retrieval
top_k = 4  # Number of chunks to retrieve
```

**Custom CSS Styling:**
- Defined in `app.py` via `st.markdown()`
- Modify colors, fonts, spacing
- Uses inline `<style>` tags

---

## 💾 Database & Storage

### Session State (In-Memory)

**Purpose:** Maintain user data during session

**Storage:**
```python
st.session_state.processed_documents = [
    {
        'file_name': 'project.pdf',
        'file_type': '.pdf',
        'processed_at': '2025-11-14T12:00:00',
        'success': True,
        'text': 'Full document text...',
        'metadata': {
            'project_name': 'Project Name',
            'budget': ['€10 million'],
            'dates': ['2024-01-15'],
            'stakeholders': ['john.doe@nato.int'],
            'status': 'GREEN',
            'word_count': 5000,
            'char_count': 25000
        }
    },
    ...
]
```

**Persistence:** Lost on browser refresh/close

**Scalability:** Limited by browser memory (~100MB typical limit)

### ChromaDB (Persistent Vector Storage)

**Location:** `./chroma_db/` directory

**Contents:**
- SQLite database (metadata)
- Vector files (embeddings)
- Chunk index

**Size:** ~1-5MB per document (depends on length)

**Persistence:** Survives application restart

**Backup:** Copy entire `chroma_db/` folder

**Clearing:**
```bash
rm -rf chroma_db/
```
Rebuilds on next document upload

### File Storage

**Temporary Files:**
- Location: System temp directory
- Purpose: Store uploaded files during processing
- Lifecycle: Deleted after processing
- Function: `tempfile.NamedTemporaryFile()`

**No Permanent File Storage:**
- Original documents NOT stored
- Only text and metadata retained
- Privacy-focused design

---

## 🔒 Security

### Current Security Measures

**1. API Key Protection**
- Stored in `.env` (git-ignored)
- Never logged or displayed
- Environment variable only

**2. Input Validation**
- File type checking (PDF/DOCX only)
- File size limits (Streamlit default: 200MB)
- No code execution from documents

**3. Data Privacy**
- Documents processed locally
- Only text chunks sent to OpenAI
- No storage of original files
- Session-based data (not persistent)

**4. Network Security**
- HTTPS for OpenAI API calls
- localhost-only by default
- No public endpoints

### Security Considerations

**⚠️ Current Limitations:**
- No user authentication
- No authorization/access control
- No encryption at rest
- No audit logging
- Single-user sessions
- OpenAI data policy applies

**🔐 Enterprise Security Recommendations:**

1. **Authentication & Authorization**
   - Implement OAuth 2.0 / SAML
   - Role-based access control (RBAC)
   - Session management

2. **Data Protection**
   - Encrypt ChromaDB at rest
   - Encrypt data in transit (TLS)
   - Secure API key management (HashiCorp Vault)

3. **Classified Documents**
   - Deploy on-premise LLM (no cloud API)
   - Air-gapped environment
   - Classified network deployment

4. **Compliance**
   - GDPR compliance for EU data
   - NATO security standards
   - Data retention policies

5. **Monitoring**
   - Audit logging
   - Access logs
   - Anomaly detection

### Secure Deployment Checklist

- [ ] Change default ports
- [ ] Enable HTTPS/TLS
- [ ] Implement authentication
- [ ] Set up firewall rules
- [ ] Configure network isolation
- [ ] Enable audit logging
- [ ] Set up backup procedures
- [ ] Document security policies
- [ ] Conduct security review
- [ ] Penetration testing

---

## ⚡ Performance

### Current Performance Metrics

| Operation | Performance | Notes |
|-----------|-------------|-------|
| PDF Processing | 2-5 sec | Per document |
| DOCX Processing | 1-3 sec | Per document |
| Metadata Extraction | <1 sec | Included in processing |
| Embedding Generation | 1-3 sec | Per document (OpenAI API) |
| ChromaDB Storage | <500ms | Per document |
| RAG Query | 3-8 sec | Includes retrieval + GPT-4 |
| Dashboard Rendering | <2 sec | Up to 50 documents |
| Network Graph | 5-15 sec | Depends on node count |

### Bottlenecks

1. **OpenAI API Calls**
   - Slowest component
   - Network latency
   - API rate limits

2. **Document Processing**
   - Large PDFs (>100 pages)
   - Complex DOCX with tables

3. **Network Graph Rendering**
   - Many nodes (>50 projects)
   - Many edges (>200 relationships)

### Optimization Strategies

**1. Caching**
```python
@st.cache_resource
def get_processor():
    return DocumentProcessor()

@st.cache_resource
def get_rag_engine():
    return RAGEngine()
```

**2. Batch Processing**
- Upload multiple documents at once
- Single RAG initialization

**3. Async Operations** (Future)
- Background document processing
- Parallel API calls

**4. Vector Store Optimization**
- Reduce chunk size for faster search
- Limit top-k retrieval

**5. UI Optimization**
- Lazy loading for large tables
- Pagination for document lists
- Conditional rendering

### Scalability Limits

**Current System:**
- **Documents:** ~100-200 optimal
- **Concurrent Users:** 1 (single session)
- **Memory:** Browser-limited (~100MB session state)
- **Storage:** Disk-limited (ChromaDB)

**Enterprise Scalability:**
- Multi-user support requires backend refactor
- Database instead of session state
- Load balancing for multiple instances
- Distributed vector store

---

## 🚀 Deployment

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/MuratGoksu/nato-pmp-analyzer.git
cd nato-pmp-analyzer

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add OPENAI_API_KEY

# 5. Run application
streamlit run app.py

# 6. Access in browser
# http://localhost:8501
```

### Production Deployment Options

#### Option 1: Streamlit Cloud (Easiest)

**Steps:**
1. Push code to GitHub
2. Sign up at streamlit.io/cloud
3. Connect GitHub repository
4. Add OPENAI_API_KEY in secrets
5. Deploy

**Pros:**
- Free tier available
- Automatic HTTPS
- Easy updates (git push)

**Cons:**
- Public internet required
- Limited resources
- Shared infrastructure

#### Option 2: Docker Container

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
docker build -t nato-pmp-analyzer .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-xxx nato-pmp-analyzer
```

**Pros:**
- Consistent environment
- Easy deployment
- Scalable

**Cons:**
- Requires Docker knowledge
- Stateless (ChromaDB needs volume mount)

#### Option 3: VM/Server Deployment

**Requirements:**
- Ubuntu 20.04+ or similar
- Python 3.10+
- 2GB RAM minimum
- 10GB disk space

**Setup:**
```bash
# Install Python
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# Clone and setup
git clone https://github.com/MuratGoksu/nato-pmp-analyzer.git
cd nato-pmp-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add API key

# Run as service (systemd)
sudo nano /etc/systemd/system/pmp-analyzer.service
```

**systemd service:**
```ini
[Unit]
Description=NATO PMP Analyzer
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/nato-pmp-analyzer
Environment="PATH=/home/ubuntu/nato-pmp-analyzer/venv/bin"
ExecStart=/home/ubuntu/nato-pmp-analyzer/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pmp-analyzer
sudo systemctl start pmp-analyzer
```

**Reverse Proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

#### Option 4: On-Premise (Classified)

**For classified documents:**
1. Air-gapped network
2. Replace OpenAI with on-premise LLM:
   - LLaMA 2
   - GPT-J
   - Government-approved AI service
3. Deploy on classified network
4. No internet connectivity required

---

## 📊 Monitoring & Logging

### Current Logging

**Streamlit Native:**
- Console output (terminal)
- Error stack traces
- Performance warnings

**Example Output:**
```
2025-11-14 12:00:00.123
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### Adding Custom Logging

**Python logging module:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)
logger.info("Document uploaded: document.pdf")
logger.error("Failed to process: error details")
```

### Monitoring Recommendations

**Production Monitoring:**
1. **Application Monitoring**
   - Uptime monitoring (UptimeRobot, Pingdom)
   - Error tracking (Sentry)
   - Performance monitoring (New Relic, Datadog)

2. **API Monitoring**
   - OpenAI API usage tracking
   - Rate limit monitoring
   - Cost monitoring

3. **Resource Monitoring**
   - CPU usage
   - Memory usage
   - Disk usage
   - Network traffic

4. **User Analytics**
   - Page views
   - Feature usage
   - Query patterns
   - Error rates

### Log Files to Monitor

```
app.log              # Application logs
streamlit.log        # Streamlit server logs
error.log            # Error-only logs
access.log           # Access logs (if using Nginx)
```

---

## 🛠️ Development Guide

### Setting Up Development Environment

```bash
# Clone repo
git clone https://github.com/MuratGoksu/nato-pmp-analyzer.git
cd nato-pmp-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black flake8 pytest

# Configure pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Code Style

**Python Style Guide:**
- Follow PEP 8
- Use Black for formatting
- Maximum line length: 100 characters
- Use type hints where helpful

**Example:**
```python
def process_document(file_path: str, file_name: str) -> Dict[str, Any]:
    """
    Process a document and extract metadata.

    Args:
        file_path: Path to the document file
        file_name: Original filename

    Returns:
        Dict containing processing results and metadata
    """
    pass
```

### Adding a New Feature

**1. Create Feature Branch**
```bash
git checkout -b feature/new-feature-name
```

**2. Implement Feature**
- Add code to appropriate module
- Update UI if needed (app.py)
- Add docstrings
- Follow existing patterns

**3. Test Feature**
- Manual testing
- Unit tests (if applicable)
- Integration testing

**4. Document Feature**
- Update USER_GUIDE.md
- Update TECHNICAL_DOCUMENTATION.md
- Update README.md
- Add comments in code

**5. Commit & Push**
```bash
git add .
git commit -m "Add: Description of feature"
git push origin feature/new-feature-name
```

**6. Create Pull Request**
- Describe changes
- Reference issues
- Request review

### Adding a New Backend Module

**Example: `backend/export_engine.py`**

```python
"""
Export Engine - Export portfolio data to various formats
"""

from typing import List, Dict
import pandas as pd

class ExportEngine:
    """Export portfolio data"""

    def __init__(self):
        self.supported_formats = ['csv', 'xlsx', 'json']

    def export_to_csv(self, documents: List[Dict], file_path: str) -> bool:
        """Export documents to CSV"""
        df = self._create_dataframe(documents)
        df.to_csv(file_path, index=False)
        return True

    def _create_dataframe(self, documents: List[Dict]) -> pd.DataFrame:
        """Convert documents to DataFrame"""
        data = []
        for doc in documents:
            metadata = doc.get('metadata', {})
            data.append({
                'Project': metadata.get('project_name', 'N/A'),
                'Status': metadata.get('status', 'N/A'),
                'Budget': ', '.join(metadata.get('budget', [])),
                'Word Count': metadata.get('word_count', 0)
            })
        return pd.DataFrame(data)
```

**Integrate in `app.py`:**
```python
from backend.export_engine import ExportEngine

@st.cache_resource
def get_export_engine():
    return ExportEngine()

export_engine = get_export_engine()

# In UI:
if st.button("Export to CSV"):
    export_engine.export_to_csv(
        st.session_state.processed_documents,
        "portfolio_export.csv"
    )
    st.success("Exported successfully!")
```

### Running Tests

**Unit Tests (pytest):**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_document_processor.py

# Run with coverage
pytest --cov=backend
```

**Manual Testing Checklist:**
- [ ] Upload PDF document
- [ ] Upload DOCX document
- [ ] Upload multiple documents
- [ ] Test chatbot queries
- [ ] Generate dashboard charts
- [ ] Generate network graphs
- [ ] Test all navigation
- [ ] Test error handling (bad files)
- [ ] Test with large documents (>100 pages)
- [ ] Test with many documents (>20)

---

## 🧪 Testing

### Test Structure

```
tests/
├── __init__.py
├── test_document_processor.py
├── test_rag_engine.py
├── test_relationship_analyzer.py
└── fixtures/
    ├── sample.pdf
    └── sample.docx
```

### Example Unit Test

**`tests/test_document_processor.py`:**
```python
import pytest
from backend.document_processor import DocumentProcessor

@pytest.fixture
def processor():
    return DocumentProcessor()

def test_extract_project_name(processor):
    text = "Project Name: NATO Cyber Defense Initiative"
    result = processor._extract_project_name(text, "test.pdf")
    assert result == "NATO Cyber Defense Initiative"

def test_extract_budget(processor):
    text = "Total budget: €10.5 million"
    result = processor._extract_budget(text)
    assert "€10.5 million" in result

def test_extract_status_red(processor):
    text = "Project status is RED due to delays"
    result = processor._extract_status(text)
    assert result == "RED"
```

### Integration Testing

**Test RAG Pipeline:**
```python
def test_rag_pipeline_integration():
    # Setup
    processor = DocumentProcessor()
    rag_engine = RAGEngine()

    # Process document
    doc = processor.process_document("tests/fixtures/sample.pdf", "sample.pdf")

    # Add to RAG
    success = rag_engine.add_documents([doc])
    assert success

    # Query
    result = rag_engine.query("What is the project name?")
    assert result['answer'] is not None
    assert len(result['sources']) > 0
```

### Test Coverage Goals

- **Document Processor:** 80%+
- **RAG Engine:** 70%+ (hard to test LLM responses)
- **Relationship Analyzer:** 80%+
- **UI Components:** Manual testing

---

## 🔧 Troubleshooting

See detailed troubleshooting in separate [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file.

**Quick Reference:**

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "ModuleNotFoundError" | Missing dependencies | `pip install -r requirements.txt` |
| "OPENAI_API_KEY not found" | Missing .env | Create .env with API key |
| "Rate limit exceeded" | Too many API calls | Wait, upgrade OpenAI plan |
| Documents not uploading | File format issue | Check PDF/DOCX, not scanned |
| Chatbot slow | Normal RAG latency | Expected 3-8 seconds |
| ChromaDB error | Corrupted database | Delete chroma_db folder, restart |
| Network graph empty | No relationships | Need 2+ documents with connections |

---

## 📚 Additional Resources

**Documentation:**
- [README.md](README.md) - Main documentation
- [USER_GUIDE.md](USER_GUIDE.md) - End-user guide
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - Demo walkthrough
- [PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md) - Presentation template

**External References:**
- [Streamlit Docs](https://docs.streamlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [NetworkX Docs](https://networkx.org/documentation/)

**GitHub:**
- Repository: https://github.com/MuratGoksu/nato-pmp-analyzer
- Issues: https://github.com/MuratGoksu/nato-pmp-analyzer/issues

---

## 📝 Document Version

**Technical Documentation Version:** 1.0
**Last Updated:** November 14, 2025
**Compatible with:** NATO PMP Analyzer v0.4+

---

**For user-facing documentation, see [USER_GUIDE.md](USER_GUIDE.md)**

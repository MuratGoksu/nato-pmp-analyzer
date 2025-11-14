import streamlit as st
import os
from pathlib import Path
import tempfile
from datetime import datetime
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.relationship_analyzer import RelationshipAnalyzer
import networkx as nx

sys.path.append(str(Path(__file__).parent))

from backend.document_processor import DocumentProcessor
from backend.rag_engine import RAGEngine

st.set_page_config(
    page_title="NATO PMP Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processing_status' not in st.session_state:
    st.session_state.processing_status = {}
if 'processed_documents' not in st.session_state:
    st.session_state.processed_documents = []
if 'rag_initialized' not in st.session_state:
    st.session_state.rag_initialized = False
if 'relationship_analyzer' not in st.session_state:
    st.session_state.relationship_analyzer = RelationshipAnalyzer()
if 'network_data' not in st.session_state:
    st.session_state.network_data = None
@st.cache_resource
def get_processor():
    return DocumentProcessor()

@st.cache_resource
def get_rag_engine():
    try:
        return RAGEngine()
    except ValueError as e:
        st.error(f"⚠️ OpenAI API Key not configured! {str(e)}")
        return None

processor = get_processor()
rag_engine = get_rag_engine()

def generate_simple_response(prompt: str, documents: list) -> str:
    prompt_lower = prompt.lower()
    status_counts = {"RED": 0, "AMBER": 0, "GREEN": 0}
    for doc in documents:
        status = doc.get('metadata', {}).get('status', 'GREEN')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    if any(word in prompt_lower for word in ['how many', 'count', 'number of', 'total']):
        if 'red' in prompt_lower or 'risk' in prompt_lower:
            return f"📊 Based on the processed documents:\n\n🔴 **{status_counts['RED']} project(s)** are marked as RED status (at risk)."
        elif 'project' in prompt_lower:
            return f"📊 Based on the processed documents:\n\n**Total Projects:** {len(documents)}\n- 🟢 GREEN: {status_counts['GREEN']}\n- 🟡 AMBER: {status_counts['AMBER']}\n- 🔴 RED: {status_counts['RED']}"
    
    if 'list' in prompt_lower:
        project_names = [doc.get('metadata', {}).get('project_name', 'Unknown') for doc in documents]
        return f"📋 **Processed Projects:**\n\n" + "\n".join([f"- {name}" for name in project_names])
    
    return f"I've processed {len(documents)} document(s). Please ask specific questions about the projects."

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/NATO_OTAN_landscape_logo.svg/320px-NATO_OTAN_landscape_logo.svg.png", width=200)
    st.markdown("---")
    
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Select Page",
        ["🏠 Home", "📤 Upload Documents", "💬 Chatbot", "📈 Dashboard", "👥 Stakeholder Network", "🔗 Network Graph"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📁 Processed Documents")
    if st.session_state.processed_documents:
        for doc in st.session_state.processed_documents:
            status_icon = "✅" if doc['success'] else "❌"
            st.markdown(f"{status_icon} {doc['file_name']}")
    else:
        st.info("No documents processed yet")
    
    st.markdown("---")
    st.markdown("### 🤖 RAG Status")
    if rag_engine and st.session_state.rag_initialized:
        st.success("🟢 RAG Active")
        try:
            stats = rag_engine.get_stats()
            st.info(f"📚 {stats.get('total_chunks', 0)} chunks indexed")
        except:
            pass
    elif rag_engine:
        st.warning("🟡 RAG Ready (no docs)")
    else:
        st.error("🔴 RAG Not Configured")
    
    st.markdown("---")
    st.markdown("### ℹ️ System Status")
    st.success("🟢 System Online")
    st.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    total_docs = len(st.session_state.processed_documents)
    successful = sum(1 for doc in st.session_state.processed_documents if doc['success'])
    st.metric("Processed", f"{successful}/{total_docs}")

if page == "🏠 Home":
    st.markdown('<div class="main-header">🛡️ NATO PMP Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Project Management Plan Analysis with RAG</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_docs = len(st.session_state.processed_documents)
    successful_docs = sum(1 for doc in st.session_state.processed_documents if doc['success'])
    
    with col1:
        st.metric(
            label="📁 Documents Processed",
            value=successful_docs,
            delta=f"+{successful_docs} today"
        )
    
    with col2:
        rag_status = "Active with RAG" if st.session_state.rag_initialized else "Pattern Matching"
        st.metric(
            label="🤖 AI Engine",
            value=rag_status,
            delta="GPT-4" if st.session_state.rag_initialized else "Basic"
        )
    
    with col3:
        total_words = sum(doc.get('metadata', {}).get('word_count', 0) 
                         for doc in st.session_state.processed_documents if doc['success'])
        st.metric(
            label="📝 Words Processed",
            value=f"{total_words:,}",
            delta="Vectorized" if st.session_state.rag_initialized else "Extracted"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📋 Document Processing ✅
        - ✅ PDF/DOCX text extraction
        - ✅ Metadata extraction
        - ✅ Stakeholder detection
        - ✅ RAG status identification
        """)
        
        st.markdown("""
        #### 💬 Intelligent Chatbot ✅
        - ✅ Natural language queries
        - ✅ Context-aware responses (RAG)
        - ✅ Semantic search
        - ✅ Source citations
        """)
    
    with col2:
        st.markdown("""
        #### 📊 Analytics Dashboard ✅
        - ✅ Portfolio overview
        - ✅ Plotly interactive charts
        - ✅ Budget visualization
        - ✅ Status tracking
        """)
        
        st.markdown("""
        #### 🔗 Coming Soon
        - 🔄 Network graph visualization
        - 🔄 Advanced filtering
        - 🔄 Export functionality
        - 🔄 Timeline charts
        """)
    
    st.markdown("---")
    
    if total_docs == 0:
        st.info("👈 **Get Started:** Upload documents to begin analysis!")
    else:
        if st.session_state.rag_initialized:
            st.success(f"✅ {successful_docs} document(s) processed with RAG! Try asking complex questions in the Chatbot!")
        else:
            st.warning(f"⚠️ {successful_docs} document(s) processed but RAG not initialized. Re-upload documents to enable RAG.")

elif page == "📤 Upload Documents":
    st.markdown("### 📤 Upload Project Management Plans")
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PMP files (PDF or DOCX)",
        type=['pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        help="Upload one or more Project Management Plan documents"
    )
    
    if uploaded_files:
        st.markdown("#### 📋 Uploaded Files:")
        
        for uploaded_file in uploaded_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📄 **{uploaded_file.name}**")
            with col2:
                st.write(f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                file_type = uploaded_file.name.split('.')[-1].upper()
                st.write(f"📎 {file_type}")
        
        st.markdown("---")
        
        if st.button("🚀 Process Documents", type="primary", width="stretch"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            new_documents = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    result = processor.process_document(tmp_file_path, uploaded_file.name)
                    st.session_state.processed_documents.append(result)
                    new_documents.append(result)
                    os.unlink(tmp_file_path)
                except Exception as e:
                    st.error(f"Error: {uploaded_file.name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.empty()
            progress_bar.empty()
            
            if rag_engine and new_documents:
                with st.spinner("🤖 Initializing RAG engine..."):
                    success = rag_engine.add_documents(st.session_state.processed_documents)
                    if success:
                        st.session_state.rag_initialized = True
                        st.success(f"✅ Processed {len(uploaded_files)} document(s) with RAG!")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Documents processed but RAG initialization failed.")
            else:
                st.success(f"✅ Processed {len(uploaded_files)} document(s)!")
            
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.processed_documents:
        st.markdown("---")
        st.markdown("### 📚 Document Library")
        
        for doc in st.session_state.processed_documents:
            if doc['success']:
                with st.expander(f"📄 {doc['file_name']} ✅", expanded=False):
                    st.markdown("#### 📊 Extracted Metadata")
                    col1, col2 = st.columns(2)
                    
                    metadata = doc.get('metadata', {})
                    
                    with col1:
                        st.markdown(f"**Project Name:** {metadata.get('project_name', 'N/A')}")
                        st.markdown(f"**Status:** {metadata.get('status', 'N/A')}")
                        st.markdown(f"**Word Count:** {metadata.get('word_count', 0):,}")
                    
                    with col2:
                        budgets = metadata.get('budget', [])
                        st.markdown(f"**Budget:** {', '.join(budgets) if budgets else 'Not found'}")
                        dates = metadata.get('dates', [])
                        st.markdown(f"**Dates Found:** {len(dates)}")
                        stakeholders = metadata.get('stakeholders', [])
                        st.markdown(f"**Stakeholders:** {len(stakeholders)}")
                    
                    st.markdown("#### 📝 Text Preview")
                    preview = processor.get_text_preview(doc.get('text', ''), max_length=500)
                    st.text_area("First 500 characters:", preview, height=150, disabled=True, 
                                key=f"txt_prev_{doc['file_name']}_{doc['processed_at']}")
                    
                    if st.checkbox(f"Show detailed metadata", key=f"meta_{doc['file_name']}"):
                        st.json(metadata)

elif page == "💬 Chatbot":
    st.markdown("### 💬 Ask Questions About Your PMPs")
    
    if not st.session_state.processed_documents:
        st.warning("⚠️ Please upload and process documents first!")
        if st.button("Go to Upload Page"):
            st.rerun()
    else:
        successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
        
        if st.session_state.rag_initialized and rag_engine:
            st.success(f"🤖 RAG-powered chatbot active! Ask complex questions about {len(successful_docs)} document(s)")
        else:
            st.info(f"💡 Basic chatbot mode (pattern matching) - {len(successful_docs)} document(s)")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.markdown(f"""
                            <div class="source-box">
                            📄 <strong>{source['file_name']}</strong><br/>
                            📋 Project: {source['project_name']}<br/>
                            🚦 Status: {source['status']}<br/>
                            📝 Snippet: {source['snippet']}
                            </div>
                            """, unsafe_allow_html=True)
        
        if prompt := st.chat_input("Ask a question about your PMPs..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    if st.session_state.rag_initialized and rag_engine:
                        result = rag_engine.query(prompt)
                        response = result['answer']
                        sources = result.get('sources', [])
                        
                        st.markdown(response)
                        if sources:
                            with st.expander("📚 Sources"):
                                for source in sources:
                                    st.markdown(f"""
                                    <div class="source-box">
                                    📄 <strong>{source['file_name']}</strong><br/>
                                    📋 Project: {source['project_name']}<br/>
                                    🚦 Status: {source['status']}<br/>
                                    📝 Snippet: {source['snippet']}
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "sources": sources
                        })
                    else:
                        response = generate_simple_response(prompt, successful_docs)
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

elif page == "📈 Dashboard":
    st.markdown("### 📈 Portfolio Dashboard")
    
    successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
    
    if not successful_docs:
        st.warning("⚠️ Please upload and process documents first!")
        if st.button("Go to Upload Page"):
            st.rerun()
    else:
        red_projects = [doc for doc in successful_docs if doc.get('metadata', {}).get('status') == 'RED']
        amber_projects = [doc for doc in successful_docs if doc.get('metadata', {}).get('status') == 'AMBER']
        green_projects = [doc for doc in successful_docs if doc.get('metadata', {}).get('status') == 'GREEN']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Critical (RED)", len(red_projects))
        with col2:
            st.metric("🟡 Warning (AMBER)", len(amber_projects))
        with col3:
            st.metric("🟢 Healthy (GREEN)", len(green_projects))
        
        st.markdown("---")
        
        if red_projects:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🔴 Risk Distribution")
                risk_df = pd.DataFrame({"Status": ["RED", "AMBER", "GREEN"], "Count": [len(red_projects), len(amber_projects), len(green_projects)]})
                fig_risk = px.pie(risk_df, values="Count", names="Status", color_discrete_map={"RED": "#dc3545", "AMBER": "#ffc107", "GREEN": "#28a745"})
                st.plotly_chart(fig_risk, width="stretch")
            with col2:
                st.markdown("#### 📊 Risk Summary")
                portfolio_health = (len(green_projects) / len(successful_docs) * 100) if successful_docs else 0
                st.metric("Portfolio Health", f"{portfolio_health:.0f}%")
                st.metric("At Risk", len(red_projects) + len(amber_projects))
            st.markdown("---")
            st.markdown("#### 🔴 RED Projects")
            red_data = []
            for doc in red_projects:
                metadata = doc.get("metadata", {})
                red_data.append({"Project": metadata.get("project_name", "N/A")[:25], "Status": "RED", "Words": metadata.get("word_count", 0), "Budget": len(metadata.get("budget", []))})
            if red_data:
                red_df = pd.DataFrame(red_data)
                st.dataframe(red_df, width="stretch", hide_index=True)
        else:
            st.success("✅ No RED projects!")

elif page == "👥 Stakeholder Network":
    st.markdown("### 👥 Stakeholder Network Analysis")
    
    successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
    
    if not successful_docs:
        st.warning("⚠️ Please upload and process documents first!")
        if st.button("Go to Upload Page"):
            st.rerun()
    else:
        # Extract all stakeholders from all documents
        all_stakeholders = {}  # {stakeholder_name: [project_names]}
        
        for doc in successful_docs:
            metadata = doc.get('metadata', {})
            project_name = metadata.get('project_name', doc.get('file_name', 'Unknown'))
            stakeholders = metadata.get('stakeholders', [])
            
            # Clean stakeholders (remove __ markers)
            for stakeholder in stakeholders:
                cleaned_stakeholder = stakeholder.strip('_')
                if cleaned_stakeholder not in all_stakeholders:
                    all_stakeholders[cleaned_stakeholder] = []
                all_stakeholders[cleaned_stakeholder].append(project_name)
        
        # Statistics
        st.markdown("#### 📊 Stakeholder Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        total_unique_stakeholders = len(all_stakeholders)
        total_stakeholder_mentions = sum(len(projects) for projects in all_stakeholders.values())
        avg_stakeholders_per_project = total_stakeholder_mentions / len(successful_docs) if successful_docs else 0
        
        # Find most connected stakeholder
        most_connected = max(all_stakeholders.items(), key=lambda x: len(x[1])) if all_stakeholders else ("N/A", [])
        
        with col1:
            st.metric("👥 Unique Stakeholders", total_unique_stakeholders)
        
        with col2:
            st.metric("📊 Total Mentions", total_stakeholder_mentions)
        
        with col3:
            st.metric("📈 Avg per Project", f"{avg_stakeholders_per_project:.1f}")
        
        with col4:
            if most_connected[0] != "N/A":
                name_display = most_connected[0].split('@')[0] if '@' in most_connected[0] else most_connected[0][:20]
                st.metric("🌟 Most Connected", name_display, f"{len(most_connected[1])} projects")
            else:
                st.metric("🌟 Most Connected", "N/A")
        
        st.markdown("---")
        
        # Stakeholder table with filtering
        st.markdown("#### 📋 Stakeholder Directory")
        
        # Filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search Stakeholder", "")
        with col2:
            min_projects = st.number_input("Min Projects", min_value=1, max_value=len(successful_docs), value=1)
        
        # Filter stakeholders
        filtered_stakeholders = {
            name: projects for name, projects in all_stakeholders.items()
            if len(projects) >= min_projects and (not search_term or search_term.lower() in name.lower())
        }
        
        if filtered_stakeholders:
            # Create stakeholder table
            stakeholder_data = []
            for stakeholder, projects in sorted(filtered_stakeholders.items(), key=lambda x: len(x[1]), reverse=True):
                stakeholder_data.append({
                    'Stakeholder': stakeholder,
                    'Project Count': len(projects),
                    'Projects': ', '.join(projects[:3]) + ('...' if len(projects) > 3 else '')
                })
            
            stakeholder_df = pd.DataFrame(stakeholder_data)
            st.dataframe(stakeholder_df, width="stretch", hide_index=True)
            
            st.info(f"📊 Showing {len(filtered_stakeholders)} stakeholder(s)")
        else:
            st.warning("No stakeholders match your filters")
        
        st.markdown("---")
        
        # Stakeholder overlap analysis
        st.markdown("#### 🔗 Stakeholder Overlap Analysis")
        
        # Find shared stakeholders between projects
        project_pairs = []
        for i, doc1 in enumerate(successful_docs):
            for j, doc2 in enumerate(successful_docs):
                if i >= j:
                    continue
                
                meta1 = doc1.get('metadata', {})
                meta2 = doc2.get('metadata', {})
                
                # Clean stakeholders before comparison
                stakeholders1 = set(s.strip('_') for s in meta1.get('stakeholders', []))
                stakeholders2 = set(s.strip('_') for s in meta2.get('stakeholders', []))
                
                shared = stakeholders1.intersection(stakeholders2)
                
                if shared:
                    proj1_name = meta1.get('project_name', doc1.get('file_name', 'Unknown'))
                    proj2_name = meta2.get('project_name', doc2.get('file_name', 'Unknown'))
                    
                    project_pairs.append({
                        'Project 1': proj1_name[:40],
                        'Project 2': proj2_name[:40],
                        'Shared': len(shared),
                        'Stakeholders': ', '.join([s.split('@')[0] for s in list(shared)[:3]]) + ('...' if len(shared) > 3 else '')
                    })
        
        if project_pairs:
            st.markdown(f"##### 🤝 Found {len(project_pairs)} project pair(s) with shared stakeholders")
            
            # Sort by number of shared stakeholders
            overlap_df = pd.DataFrame(project_pairs).sort_values('Shared', ascending=False)
            st.dataframe(overlap_df, width="stretch", hide_index=True)
            
            # Visualization: Stakeholder distribution
            st.markdown("---")
            st.markdown("#### 📊 Stakeholder Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Stakeholders per project
                project_stakeholder_counts = []
                for doc in successful_docs:
                    metadata = doc.get('metadata', {})
                    project_stakeholder_counts.append({
                        'Project': metadata.get('project_name', 'Unknown')[:30],
                        'Stakeholders': len(metadata.get('stakeholders', []))
                    })
                
                if project_stakeholder_counts:
                    proj_stake_df = pd.DataFrame(project_stakeholder_counts)
                    fig_stakeholders = px.bar(
                        proj_stake_df,
                        x='Project',
                        y='Stakeholders',
                        title='Stakeholders per Project',
                        color='Stakeholders',
                        color_continuous_scale='Viridis'
                    )
                    fig_stakeholders.update_layout(height=400, showlegend=False)
                    fig_stakeholders.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig_stakeholders, width="stretch")
            
            with col2:
                # Top stakeholders by project count
                top_stakeholders = sorted(all_stakeholders.items(), key=lambda x: len(x[1]), reverse=True)[:10]
                
                if top_stakeholders:
                    top_stake_df = pd.DataFrame({
                        'Stakeholder': [s[0].split('@')[0] for s in top_stakeholders],
                        'Projects': [len(s[1]) for s in top_stakeholders]
                    })
                    
                    fig_top = px.bar(
                        top_stake_df,
                        x='Projects',
                        y='Stakeholder',
                        orientation='h',
                        title='Top 10 Most Connected Stakeholders',
                        color='Projects',
                        color_continuous_scale='Blues'
                    )
                    fig_top.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig_top, width="stretch")
            
            # Network visualization
            st.markdown("---")
            st.markdown("#### 🕸️ Stakeholder Network Graph")
            
            if st.button("🔄 Generate Network Visualization", type="primary"):
                with st.spinner("Creating network graph..."):
                    try:
                        # Create network graph using networkx
                        G = nx.Graph()
                        
                        # Add nodes for projects
                        for doc in successful_docs:
                            meta = doc.get('metadata', {})
                            project_name = meta.get('project_name', doc.get('file_name', 'Unknown'))
                            G.add_node(project_name, node_type='project')
                        
                        # Add edges for shared stakeholders
                        for pair in project_pairs:
                            G.add_edge(
                                pair['Project 1'],
                                pair['Project 2'],
                                weight=pair['Shared']
                            )
                        
                        # Create plotly figure
                        pos = nx.spring_layout(G, k=1, iterations=50)
                        
                        # Create edges
                        edge_trace = []
                        for edge in G.edges():
                            x0, y0 = pos[edge[0]]
                            x1, y1 = pos[edge[1]]
                            edge_trace.append(
                                go.Scatter(
                                    x=[x0, x1, None],
                                    y=[y0, y1, None],
                                    mode='lines',
                                    line=dict(width=2, color='#888'),
                                    hoverinfo='none',
                                    showlegend=False
                                )
                            )
                        
                        # Create nodes
                        node_x = []
                        node_y = []
                        node_text = []
                        node_size = []
                        
                        for node in G.nodes():
                            x, y = pos[node]
                            node_x.append(x)
                            node_y.append(y)
                            
                            # Get stakeholder count for this project
                            doc = next((d for d in successful_docs 
                                      if d.get('metadata', {}).get('project_name', d.get('file_name')) == node), None)
                            stake_count = len(doc.get('metadata', {}).get('stakeholders', [])) if doc else 0
                            
                            node_text.append(f"{node}<br>Stakeholders: {stake_count}")
                            node_size.append(20 + stake_count * 5)
                        
                        node_trace = go.Scatter(
                            x=node_x,
                            y=node_y,
                            mode='markers+text',
                            text=[n.split()[0] if ' ' in n else n[:15] for n in G.nodes()],
                            textposition='top center',
                            hovertext=node_text,
                            hoverinfo='text',
                            marker=dict(
                                size=node_size,
                                color='#1f77b4',
                                line=dict(width=2, color='white')
                            ),
                            showlegend=False
                        )
                        
                        # Create figure
                        fig = go.Figure(data=edge_trace + [node_trace])
                        fig.update_layout(
                            title=dict(
                                text='Project Network by Shared Stakeholders',
                                font=dict(size=16)
                            ),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            height=600
                        )
                        
                        st.plotly_chart(fig, width="stretch")
                        st.success("✅ Network visualization generated!")
                        
                    except Exception as e:
                        st.error(f"Error creating network: {str(e)}")
        else:
            st.info("ℹ️ No shared stakeholders found between projects")
        
        # Detailed stakeholder breakdown
        st.markdown("---")
        st.markdown("#### 🔍 Detailed Stakeholder Breakdown")
        
        selected_stakeholder = st.selectbox(
            "Select a stakeholder to see details:",
            options=[''] + sorted(all_stakeholders.keys()),
            index=0
        )
        
        if selected_stakeholder:
            projects_with_stakeholder = all_stakeholders[selected_stakeholder]
            
            st.markdown(f"##### 👤 {selected_stakeholder}")
            st.info(f"📊 Appears in **{len(projects_with_stakeholder)}** project(s)")
            
            # Show projects
            st.markdown("**Projects:**")
            for proj in projects_with_stakeholder:
                st.markdown(f"- {proj}")

elif page == "🔗 Network Graph":
    st.markdown("### 🔗 Project Relationship Network")
    
    successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
    
    if not successful_docs:
        st.warning("⚠️ Please upload and process documents first!")
    else:
        # Generate network data
        network_data = st.session_state.relationship_analyzer.get_network_data(successful_docs)
        nodes = network_data['nodes']
        edges = network_data['edges']
        
        # Sidebar controls
        with st.sidebar:
            st.markdown("### 🎛️ Network Controls")
            
            relationship_filter = st.multiselect(
                "Filter by Relationship Type:",
                ['stakeholder', 'technology', 'budget', 'status'],
                default=['stakeholder', 'technology', 'budget', 'status']
            )
        
        # Filter edges
        filtered_edges = [e for e in edges if e['type'] in relationship_filter]
        
        # Statistics
        st.markdown("#### 📊 Network Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🟢 Projects", len(nodes))
        
        with col2:
            st.metric("🔗 Relationships", len(filtered_edges))
        
        with col3:
            if nodes:
                avg_connections = len(filtered_edges) * 2 / len(nodes)
                st.metric("🤝 Avg Connections", f"{avg_connections:.1f}")
        
        # Relationship breakdown
        st.markdown("#### 📋 Relationship Breakdown")
        rel_counts = {}
        for edge in filtered_edges:
            rel_type = edge['type']
            rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
        
        if rel_counts:
            rel_df = pd.DataFrame({
                'Type': list(rel_counts.keys()),
                'Count': list(rel_counts.values())
            })
            st.bar_chart(rel_df.set_index('Type'))
            st.dataframe(rel_df, width="stretch", hide_index=True)
        else:
            st.info("No relationships found with current filters")
        
        # Projects table
        st.markdown("#### 📋 Projects in Network")
        projects_df = pd.DataFrame([
            {
                'Project': node['label'],
                'Status': node['status'],
                'Words': node['word_count'],
                'Stakeholders': node['stakeholders']
            }
            for node in nodes
        ])
        st.dataframe(projects_df, width="stretch", hide_index=True)
        
        # Relationship details
        st.markdown("#### 🔗 Relationship Details")
        if filtered_edges:
            for edge in filtered_edges[:10]:
                st.write(f"**{edge['source']}** ↔️ **{edge['target']}**")
                st.caption(f"🏷️ {edge['type'].title()} - {edge['label']}")
        else:
            st.info("No relationships to display")
        
        # Network Visualization
        st.markdown("---")
        st.markdown("#### 🕸️ Interactive Network Graph")
        
        if st.button("🔄 Generate Network Visualization", type="primary", key="network_graph_viz"):
            with st.spinner("Creating interactive network graph..."):
                try:
                    import networkx as nx
                    
                    # Create network graph
                    G = nx.Graph()
                    
                    # Add nodes
                    for node in nodes:
                        G.add_node(
                            node['id'],
                            label=node['label'],
                            status=node['status'],
                            word_count=node['word_count'],
                            stakeholders=node['stakeholders']
                        )
                    
                    # Add edges
                    for edge in filtered_edges:
                        G.add_edge(
                            edge['source'],
                            edge['target'],
                            type=edge['type'],
                            label=edge['label'],
                            strength=edge['strength']
                        )
                    
                    # Calculate layout
                    pos = nx.spring_layout(G, k=2, iterations=50)
                    
                    # Define colors for relationship types
                    edge_colors = {
                        'stakeholder': '#FF6B6B',  # Red
                        'technology': '#4ECDC4',   # Teal
                        'budget': '#FFD93D',       # Yellow
                        'status': '#95E1D3'        # Mint
                    }
                    
                    # Create edge traces by type
                    edge_traces = []
                    for edge_type in ['stakeholder', 'technology', 'budget', 'status']:
                        if edge_type not in relationship_filter:
                            continue
                        
                        edge_x = []
                        edge_y = []
                        
                        for edge in G.edges(data=True):
                            if edge[2].get('type') == edge_type:
                                x0, y0 = pos[edge[0]]
                                x1, y1 = pos[edge[1]]
                                edge_x.extend([x0, x1, None])
                                edge_y.extend([y0, y1, None])
                        
                        if edge_x:
                            edge_trace = go.Scatter(
                                x=edge_x,
                                y=edge_y,
                                mode='lines',
                                line=dict(width=2, color=edge_colors[edge_type]),
                                hoverinfo='none',
                                name=edge_type.title(),
                                showlegend=True
                            )
                            edge_traces.append(edge_trace)
                    
                    # Create node trace
                    node_x = []
                    node_y = []
                    node_text = []
                    node_size = []
                    node_color = []
                    
                    # Status colors
                    status_colors = {
                        'GREEN': '#28a745',
                        'AMBER': '#ffc107',
                        'RED': '#dc3545',
                        'UNKNOWN': '#6c757d'
                    }
                    
                    for node_id in G.nodes():
                        x, y = pos[node_id]
                        node_x.append(x)
                        node_y.append(y)
                        
                        # Get node data
                        node_data = G.nodes[node_id]
                        
                        # Calculate node size based on connections
                        connections = len(list(G.neighbors(node_id)))
                        node_size.append(20 + connections * 10)
                        
                        # Node color based on status
                        node_color.append(status_colors.get(node_data['status'], '#6c757d'))
                        
                        # Hover text
                        hover_text = f"<b>{node_data['label']}</b><br>"
                        hover_text += f"Status: {node_data['status']}<br>"
                        hover_text += f"Words: {node_data['word_count']}<br>"
                        hover_text += f"Stakeholders: {node_data['stakeholders']}<br>"
                        hover_text += f"Connections: {connections}"
                        node_text.append(hover_text)
                    
                    node_trace = go.Scatter(
                        x=node_x,
                        y=node_y,
                        mode='markers+text',
                        text=[G.nodes[n]['label'].split()[0] if ' ' in G.nodes[n]['label'] else G.nodes[n]['label'][:15] for n in G.nodes()],
                        textposition='top center',
                        hovertext=node_text,
                        hoverinfo='text',
                        marker=dict(
                            size=node_size,
                            color=node_color,
                            line=dict(width=2, color='white')
                        ),
                        showlegend=False
                    )
                    
                    # Create figure
                    fig = go.Figure(data=edge_traces + [node_trace])
                    fig.update_layout(
                        title=dict(
                            text='Project Relationship Network',
                            font=dict(size=18)
                        ),
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=60),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=700,
                        legend=dict(
                            x=0.01,
                            y=0.99,
                            bgcolor='rgba(255,255,255,0.8)',
                            bordercolor='#333',
                            borderwidth=1
                        )
                    )
                    
                    st.plotly_chart(fig, width="stretch")
                    st.success("✅ Network visualization generated!")
                    
                    # Show legend explanation
                    st.markdown("---")
                    st.markdown("##### 📖 Legend")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**Relationship Types:**")
                        st.markdown("🔴 Stakeholder Overlap")
                        st.markdown("🔵 Technology Keywords")
                    
                    with col2:
                        st.markdown("**&nbsp;**")
                        st.markdown("🟡 Budget Similarity")
                        st.markdown("🟢 Same Status")
                    
                    with col3:
                        st.markdown("**Node Colors (Status):**")
                        st.markdown("🟢 GREEN - On Track")
                        st.markdown("🟡 AMBER - Warning")
                    
                    with col4:
                        st.markdown("**&nbsp;**")
                        st.markdown("🔴 RED - At Risk")
                        st.markdown("⚫ UNKNOWN")
                    
                    st.info("💡 **Tip:** Node size = number of connections. Hover over nodes and edges for details!")
                    
                except Exception as e:
                    st.error(f"❌ Error creating network: {str(e)}")
                    st.exception(e)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🛡️ NATO PMP Analyzer PoC v0.4 | Built with Streamlit, OpenAI & LangChain</p>
    <p>📅 Week 1 Complete - Day 5: Clean & Stable ✅</p>
</div>
""", unsafe_allow_html=True)

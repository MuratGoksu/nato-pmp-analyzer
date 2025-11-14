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
    st.title("👥 Stakeholder Network Analysis")
    st.success("✅ PAGE IS LOADING!")
    
    st.write(f"Debug: Total docs = {len(st.session_state.processed_documents)}")
    st.write(f"Debug: Session state keys = {list(st.session_state.keys())}")
    
    successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
    st.write(f"Debug: Successful docs = {len(successful_docs)}")
    
    if successful_docs:
        st.write("**Document list:**")
        for doc in successful_docs:
            st.write(f"- {doc.get('file_name', 'Unknown')}")
            st.write(f"  Metadata: {list(doc.get('metadata', {}).keys())}")
            st.write(f"  Stakeholders: {doc.get('metadata', {}).get('stakeholders', [])}")
    else:
        st.warning("No successful docs found")
    
    st.markdown("---")
    st.info("If you see this message, the page is working!")

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
    successful_docs = [doc for doc in st.session_state.processed_documents if doc['success']]
    
    if not successful_docs:
        st.warning("⚠️ Please upload and process documents first!")
        if st.button("Go to Upload Page"):
            st.rerun()
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        total_words = sum(doc.get('metadata', {}).get('word_count', 0) for doc in successful_docs)
        status_counts = {"RED": 0, "AMBER": 0, "GREEN": 0}
        for doc in successful_docs:
            status = doc.get('metadata', {}).get('status', 'GREEN')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        with col1:
            st.metric("📁 Total Projects", len(successful_docs), f"+{len(successful_docs)}")
        
        with col2:
            total_budgets = sum(len(doc.get('metadata', {}).get('budget', [])) for doc in successful_docs)
            st.metric("💰 Budget Mentions", total_budgets, "Found")
        
        with col3:
            total_stakeholders = sum(len(doc.get('metadata', {}).get('stakeholders', [])) for doc in successful_docs)
            st.metric("👥 Stakeholders", total_stakeholders, "Identified")
        
        with col4:
            st.metric("🎯 At Risk (RED)", status_counts.get("RED", 0), f"{status_counts.get('RED', 0)} projects")
        
        st.markdown("---")
        st.markdown("#### 📋 Project List")
        
        table_data = []
        for doc in successful_docs:
            metadata = doc.get('metadata', {})
            table_data.append({
                'Project Name': metadata.get('project_name', 'N/A'),
                'Status': metadata.get('status', 'N/A'),
                'Words': f"{metadata.get('word_count', 0):,}",
                'Budget Items': len(metadata.get('budget', [])),
                'Stakeholders': len(metadata.get('stakeholders', [])),
                'Dates': len(metadata.get('dates', []))
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, width="stretch", hide_index=True)
        
        st.markdown("---")
        st.markdown("### 📊 Interactive Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Budget Distribution")
            budget_data = []
            for doc in successful_docs:
                metadata = doc.get('metadata', {})
                budgets = metadata.get('budget', [])
                if budgets:
                    import re
                    budget_str = budgets[0]
                    numbers = re.findall(r'[\d,\.]+', budget_str)
                    if numbers:
                        try:
                            amount = float(numbers[0].replace(',', ''))
                            budget_data.append({
                                'Project': metadata.get('project_name', 'Unknown')[:30],
                                'Budget': amount
                            })
                        except:
                            pass
            
            if budget_data:
                budget_df = pd.DataFrame(budget_data)
                fig_budget = px.pie(
                    budget_df, 
                    values='Budget', 
                    names='Project',
                    title='Budget Allocation',
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig_budget.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_budget, width="stretch")
            else:
                st.info("No budget data available")
        
        with col2:
            st.markdown("#### 🚦 RAG Status")
            status_df = pd.DataFrame({
                'Status': ['GREEN', 'AMBER', 'RED'],
                'Count': [status_counts.get('GREEN', 0), status_counts.get('AMBER', 0), status_counts.get('RED', 0)],
                'Color': ['#28a745', '#ffc107', '#dc3545']
            })
            
            fig_status = go.Figure(data=[
                go.Bar(
                    x=status_df['Status'],
                    y=status_df['Count'],
                    marker_color=status_df['Color'],
                    text=status_df['Count'],
                    textposition='auto',
                )
            ])
            fig_status.update_layout(
                title='Project Status (RAG)',
                xaxis_title='Status',
                yaxis_title='Projects',
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_status, width="stretch")
        
        st.markdown("#### 📝 Word Count Comparison")
        word_data = []
        for doc in successful_docs:
            metadata = doc.get('metadata', {})
            word_data.append({
                'Project': metadata.get('project_name', 'Unknown')[:30],
                'Words': metadata.get('word_count', 0)
            })
        
        word_df = pd.DataFrame(word_data)
        fig_words = px.bar(
            word_df,
            x='Project',
            y='Words',
            title='Document Size by Word Count',
            color='Words',
            color_continuous_scale='Blues'
        )
        fig_words.update_layout(height=400)
        st.plotly_chart(fig_words, width="stretch")
        
        st.markdown("---")
        st.markdown("#### 📈 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Total Words", f"{total_words:,}")
        
        with col2:
            avg_words = total_words // len(successful_docs) if successful_docs else 0
            st.metric("📊 Average Words/Doc", f"{avg_words:,}")
        
        with col3:
            max_words = max([d.get('metadata', {}).get('word_count', 0) for d in successful_docs]) if successful_docs else 0
            st.metric("📈 Largest Document", f"{max_words:,} words")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🛡️ NATO PMP Analyzer PoC v0.4 | Built with Streamlit, OpenAI & LangChain</p>
    <p>📅 Week 1 Complete - Day 5: Clean & Stable ✅</p>
</div>
""", unsafe_allow_html=True)

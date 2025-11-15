"""
RAG Engine - Compatible with LangChain 0.1.0+
"""

import os
from typing import List, Dict
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

from dotenv import dotenv_values

# Load env using dotenv_values (more reliable than load_dotenv)
_env_path = Path(__file__).parent.parent / '.env'
_env_config = dotenv_values(_env_path) if _env_path.exists() else {}


class RAGEngine:
    """RAG Engine for document analysis"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        # Use dotenv_values for reliable key loading (load_dotenv truncates long keys)
        self.openai_api_key = _env_config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model_name = _env_config.get("OPENAI_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found!")

        # Ensure environment variable is set for LangChain
        os.environ["OPENAI_API_KEY"] = self.openai_api_key

        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.7,  # Increased for more varied responses
            api_key=self.openai_api_key
        )
        
        self.vectorstore = None
        self.qa_chain = None
        self.retriever = None
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def add_documents(self, documents: List[Dict]) -> bool:
        """Add processed documents to vector store"""
        try:
            langchain_docs = []
            
            for doc in documents:
                if not doc.get('success', False):
                    continue
                
                text = doc.get('text', '')
                if not text:
                    continue
                
                chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    metadata = {
                        'source': doc.get('file_name', 'Unknown'),
                        'project_name': doc.get('metadata', {}).get('project_name', 'Unknown'),
                        'status': doc.get('metadata', {}).get('status', 'Unknown'),
                        'chunk_id': i,
                        'total_chunks': len(chunks)
                    }
                    
                    langchain_docs.append(Document(page_content=chunk, metadata=metadata))
            
            if not langchain_docs:
                return False
            
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=langchain_docs,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory
                )
            else:
                self.vectorstore.add_documents(langchain_docs)

            # Note: Chroma 0.4.x+ auto-persists, no manual persist() needed
            self._setup_qa_chain()
            
            return True
            
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False
    
    def _setup_qa_chain(self):
        """Setup QA chain using LCEL"""
        template = """You are an expert AI analyst specializing in NATO Project Management Plans (PMPs).

INSTRUCTIONS:
- Analyze the provided context carefully and extract SPECIFIC information
- Give DETAILED answers with concrete facts, numbers, dates, and names when available
- ALWAYS cite which project(s) you're referencing
- If information is not in the context, clearly state "I cannot find this information in the uploaded documents"
- Provide different insights for different questions - avoid generic responses
- When asked about multiple projects, compare and contrast them
- Include relevant details like: budget amounts, dates, stakeholders, status, risks

Context from PMPs:
{context}

User Question: {question}

Detailed Answer (be specific and cite sources):"""
        
        QA_PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 6}  # Retrieve more chunks for better context
        )
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.qa_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | QA_PROMPT
            | self.llm
        )
    
    def query(self, question: str) -> Dict:
        """Query the RAG system"""
        if self.qa_chain is None:
            return {
                'answer': "No documents processed yet.",
                'sources': []
            }
        
        try:
            answer = self.qa_chain.invoke(question)
            source_docs = self.retriever.invoke(question)
            
            sources = []
            seen_sources = set()
            
            for doc in source_docs:
                source_name = doc.metadata.get('source', 'Unknown')
                project_name = doc.metadata.get('project_name', 'Unknown')
                source_key = f"{source_name}_{project_name}"
                
                if source_key not in seen_sources:
                    sources.append({
                        'file_name': source_name,
                        'project_name': project_name,
                        'status': doc.metadata.get('status', 'Unknown'),
                        'snippet': doc.page_content[:200] + "..."
                    })
                    seen_sources.add(source_key)
            
            answer_text = answer.content if hasattr(answer, 'content') else str(answer)
            
            return {
                'answer': answer_text,
                'sources': sources[:3]
            }
            
        except Exception as e:
            return {
                'answer': f"Error: {str(e)}",
                'sources': []
            }
    
    def get_stats(self) -> Dict:
        """Get stats"""
        if self.vectorstore is None:
            return {'total_chunks': 0}
        
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {'total_chunks': count}
        except:
            return {'total_chunks': 0}

"""
Document Storage Manager
Handles persistent storage of processed documents
"""

import json
import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class DocumentStorage:
    """Manages persistent storage of processed documents"""

    def __init__(self, storage_file: str = "processed_documents.json"):
        self.storage_file = storage_file
        self.storage_path = Path(storage_file)

    def save_documents(self, documents: List[Dict]) -> bool:
        """
        Save processed documents to disk

        Args:
            documents: List of processed document dictionaries

        Returns:
            bool: True if successful
        """
        try:
            # Prepare documents for JSON serialization
            serializable_docs = []
            for doc in documents:
                # Create a copy to avoid modifying original
                doc_copy = {
                    'file_name': doc.get('file_name', ''),
                    'success': doc.get('success', False),
                    'processed_at': doc.get('processed_at', datetime.now().isoformat()),
                    'text': doc.get('text', ''),
                    'metadata': doc.get('metadata', {}),
                    'error': doc.get('error', None)
                }
                serializable_docs.append(doc_copy)

            # Write to file
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_docs, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved {len(serializable_docs)} documents to {self.storage_file}")
            return True

        except Exception as e:
            print(f"❌ Error saving documents: {str(e)}")
            return False

    def load_documents(self) -> List[Dict]:
        """
        Load processed documents from disk

        Returns:
            List of document dictionaries (empty list if file doesn't exist)
        """
        try:
            if not self.storage_path.exists():
                print(f"ℹ️  No saved documents found at {self.storage_file}")
                return []

            with open(self.storage_path, 'r', encoding='utf-8') as f:
                documents = json.load(f)

            print(f"✅ Loaded {len(documents)} documents from {self.storage_file}")
            return documents

        except Exception as e:
            print(f"❌ Error loading documents: {str(e)}")
            return []

    def clear_documents(self) -> bool:
        """
        Clear all saved documents

        Returns:
            bool: True if successful
        """
        try:
            if self.storage_path.exists():
                os.remove(self.storage_path)
                print(f"✅ Cleared saved documents")
            return True
        except Exception as e:
            print(f"❌ Error clearing documents: {str(e)}")
            return False

    def get_document_count(self) -> int:
        """
        Get count of saved documents

        Returns:
            int: Number of saved documents
        """
        docs = self.load_documents()
        return len(docs)

    def document_exists(self, file_name: str) -> bool:
        """
        Check if a document with given filename already exists

        Args:
            file_name: Name of the file to check

        Returns:
            bool: True if document exists
        """
        docs = self.load_documents()
        return any(doc.get('file_name') == file_name for doc in docs)

    def add_document(self, document: Dict) -> bool:
        """
        Add a single document to storage

        Args:
            document: Document dictionary to add

        Returns:
            bool: True if successful
        """
        try:
            # Load existing documents
            documents = self.load_documents()

            # Check for duplicates
            file_name = document.get('file_name', '')
            if any(doc.get('file_name') == file_name for doc in documents):
                print(f"ℹ️  Document '{file_name}' already exists, replacing...")
                documents = [doc for doc in documents if doc.get('file_name') != file_name]

            # Add new document
            documents.append(document)

            # Save all documents
            return self.save_documents(documents)

        except Exception as e:
            print(f"❌ Error adding document: {str(e)}")
            return False

    def remove_document(self, file_name: str) -> bool:
        """
        Remove a document from storage

        Args:
            file_name: Name of file to remove

        Returns:
            bool: True if successful
        """
        try:
            documents = self.load_documents()
            filtered_docs = [doc for doc in documents if doc.get('file_name') != file_name]

            if len(filtered_docs) < len(documents):
                print(f"✅ Removed document '{file_name}'")
                return self.save_documents(filtered_docs)
            else:
                print(f"ℹ️  Document '{file_name}' not found")
                return False

        except Exception as e:
            print(f"❌ Error removing document: {str(e)}")
            return False

    def get_storage_info(self) -> Dict:
        """
        Get information about storage

        Returns:
            Dict with storage statistics
        """
        docs = self.load_documents()

        if not self.storage_path.exists():
            return {
                'exists': False,
                'document_count': 0,
                'file_size': 0,
                'last_modified': None
            }

        stat = self.storage_path.stat()

        return {
            'exists': True,
            'document_count': len(docs),
            'file_size': stat.st_size,
            'file_size_mb': round(stat.st_size / (1024 * 1024), 2),
            'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

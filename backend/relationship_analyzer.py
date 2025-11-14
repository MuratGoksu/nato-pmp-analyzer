"""
Relationship Analyzer - Detects relationships between projects
"""

from typing import List, Dict


class RelationshipAnalyzer:
    """Analyze relationships between projects"""
    
    def __init__(self):
        self.relationship_types = {
            'stakeholder': 'Shared Stakeholders',
            'technology': 'Common Technologies',
            'budget': 'Similar Budget Range',
            'status': 'Same Status'
        }
    
    def analyze_relationships(self, documents: List[Dict]) -> List[Dict]:
        """Analyze relationships between all documents"""
        relationships = []
        
        for i, doc1 in enumerate(documents):
            for j, doc2 in enumerate(documents):
                if i >= j:
                    continue
                
                rels = self._find_relationships(doc1, doc2)
                if rels:
                    relationships.extend(rels)
        
        return relationships
    
    def _find_relationships(self, doc1: Dict, doc2: Dict) -> List[Dict]:
        """Find all relationships between two documents"""
        relationships = []
        
        meta1 = doc1.get('metadata', {})
        meta2 = doc2.get('metadata', {})
        
        proj1 = meta1.get('project_name', doc1.get('file_name', 'Unknown'))
        proj2 = meta2.get('project_name', doc2.get('file_name', 'Unknown'))
        
        stakeholder_rel = self._check_stakeholder_overlap(meta1, meta2)
        if stakeholder_rel:
            relationships.append({
                'source': proj1,
                'target': proj2,
                'type': 'stakeholder',
                'strength': stakeholder_rel,
                'label': f"{stakeholder_rel} shared stakeholder(s)"
            })
        
        tech_rel = self._check_technology_overlap(doc1, doc2)
        if tech_rel > 0:
            relationships.append({
                'source': proj1,
                'target': proj2,
                'type': 'technology',
                'strength': tech_rel,
                'label': f"{tech_rel} common keyword(s)"
            })
        
        budget_rel = self._check_budget_similarity(meta1, meta2)
        if budget_rel:
            relationships.append({
                'source': proj1,
                'target': proj2,
                'type': 'budget',
                'strength': 1,
                'label': 'Similar budget range'
            })
        
        if meta1.get('status') == meta2.get('status') and meta1.get('status'):
            relationships.append({
                'source': proj1,
                'target': proj2,
                'type': 'status',
                'strength': 1,
                'label': f"Both {meta1.get('status')}"
            })
        
        return relationships
    
    def _check_stakeholder_overlap(self, meta1: Dict, meta2: Dict) -> int:
        stakeholders1 = set(meta1.get('stakeholders', []))
        stakeholders2 = set(meta2.get('stakeholders', []))
        overlap = stakeholders1.intersection(stakeholders2)
        return len(overlap)
    
    def _check_technology_overlap(self, doc1: Dict, doc2: Dict) -> int:
        tech_keywords = ['quantum', 'cyber', 'ai', 'artificial intelligence', 'cloud',
                        'security', 'encryption', 'machine learning', 'blockchain',
                        'iot', '5g', 'satellite', 'drone', 'autonomous']
        
        text1 = doc1.get('text', '').lower()
        text2 = doc2.get('text', '').lower()
        
        common_techs = 0
        for keyword in tech_keywords:
            if keyword in text1 and keyword in text2:
                common_techs += 1
        
        return common_techs
    
    def _check_budget_similarity(self, meta1: Dict, meta2: Dict) -> bool:
        import re
        
        budgets1 = meta1.get('budget', [])
        budgets2 = meta2.get('budget', [])
        
        if not budgets1 or not budgets2:
            return False
        
        def extract_amount(budget_str):
            numbers = re.findall(r'[\d,\.]+', budget_str)
            if numbers:
                try:
                    return float(numbers[0].replace(',', ''))
                except:
                    return None
            return None
        
        amount1 = extract_amount(budgets1[0])
        amount2 = extract_amount(budgets2[0])
        
        if amount1 and amount2:
            ratio = min(amount1, amount2) / max(amount1, amount2)
            return ratio > 0.5
        
        return False
    
    def get_network_data(self, documents: List[Dict]) -> Dict:
        """Get network data for visualization"""
        relationships = self.analyze_relationships(documents)
        
        nodes = []
        for doc in documents:
            if not doc.get('success'):
                continue
            
            meta = doc.get('metadata', {})
            nodes.append({
                'id': meta.get('project_name', doc.get('file_name', 'Unknown')),
                'label': meta.get('project_name', doc.get('file_name', 'Unknown'))[:40],
                'status': meta.get('status', 'UNKNOWN'),
                'word_count': meta.get('word_count', 0),
                'stakeholders': len(meta.get('stakeholders', []))
            })
        
        edges = []
        for rel in relationships:
            edges.append({
                'source': rel['source'],
                'target': rel['target'],
                'type': rel['type'],
                'label': rel['label'],
                'strength': rel['strength']
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }

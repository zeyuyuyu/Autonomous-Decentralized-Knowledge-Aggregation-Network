import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class KnowledgeNode:
    content: str
    timestamp: datetime
    source: str
    trust_score: float
    verification_count: int
    hash: str

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_graph: Dict[str, KnowledgeNode] = {}
        self.trust_scores: Dict[str, float] = {}
        self.consensus_threshold = 0.75
    
    def add_knowledge(self, content: str, source: str) -> str:
        """Add new knowledge to the network with initial trust scoring"""
        timestamp = datetime.now()
        node_hash = self._generate_hash(content, source, timestamp)
        
        trust_score = self.trust_scores.get(source, 0.5)
        
        node = KnowledgeNode(
            content=content,
            timestamp=timestamp,
            source=source,
            trust_score=trust_score,
            verification_count=1,
            hash=node_hash
        )
        
        self.knowledge_graph[node_hash] = node
        return node_hash
    
    def verify_knowledge(self, node_hash: str, verifier: str) -> bool:
        """Verify existing knowledge and update trust scores"""
        if node_hash not in self.knowledge_graph:
            return False
            
        node = self.knowledge_graph[node_hash]
        verifier_trust = self.trust_scores.get(verifier, 0.5)
        
        # Update node verification metrics
        node.verification_count += 1
        node.trust_score = self._calculate_weighted_trust(node, verifier_trust)
        
        # Update source trust scores
        if node.trust_score > self.consensus_threshold:
            self._update_trust_score(node.source, 0.1)
            self._update_trust_score(verifier, 0.05)
        
        return True
    
    def get_verified_knowledge(self, min_trust: float = 0.7) -> List[KnowledgeNode]:
        """Retrieve knowledge that meets minimum trust threshold"""
        return [
            node for node in self.knowledge_graph.values()
            if node.trust_score >= min_trust
        ]
    
    def _generate_hash(self, content: str, source: str, timestamp: datetime) -> str:
        """Generate unique hash for knowledge node"""
        hash_input = f"{content}{source}{timestamp.isoformat()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def _calculate_weighted_trust(self, node: KnowledgeNode, verifier_trust: float) -> float:
        """Calculate weighted trust score based on verifications"""
        base_trust = node.trust_score * node.verification_count
        new_trust = base_trust + verifier_trust
        return new_trust / (node.verification_count + 1)
    
    def _update_trust_score(self, source: str, delta: float):
        """Update trust score for a source"""
        current_trust = self.trust_scores.get(source, 0.5)
        new_trust = min(1.0, max(0.0, current_trust + delta))
        self.trust_scores[source] = new_trust
    
    def get_source_trust(self, source: str) -> float:
        """Get trust score for a specific source"""
        return self.trust_scores.get(source, 0.5)

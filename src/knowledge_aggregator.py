import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class KnowledgeNode:
    id: str
    data: Any
    timestamp: float
    signatures: List[str] = None
    references: List[str] = None

class KnowledgeAggregator:
    def __init__(self, node_id: str, min_consensus: float = 0.67):
        self.node_id = node_id
        self.knowledge_pool = {}
        self.pending_validations = {}
        self.validated_knowledge = {}
        self.min_consensus = min_consensus
        self.peers = set()
    
    def add_peer(self, peer_id: str) -> None:
        self.peers.add(peer_id)
    
    def submit_knowledge(self, data: Any, references: List[str] = None) -> str:
        """Submit new knowledge to the network for validation"""
        node = KnowledgeNode(
            id=self._generate_id(data),
            data=data,
            timestamp=datetime.now().timestamp(),
            signatures=[self.node_id],
            references=references or []
        )
        self.pending_validations[node.id] = node
        return node.id
    
    def validate_knowledge(self, node_id: str, peer_signature: str) -> bool:
        """Validate knowledge and track consensus"""
        if node_id not in self.pending_validations:
            return False
            
        node = self.pending_validations[node_id]
        if peer_signature not in node.signatures:
            node.signatures.append(peer_signature)
        
        # Check if consensus reached
        if len(node.signatures) >= len(self.peers) * self.min_consensus:
            self.validated_knowledge[node_id] = node
            del self.pending_validations[node_id]
            return True
        return False
    
    def get_knowledge(self, node_id: str) -> KnowledgeNode:
        """Retrieve validated knowledge by ID"""
        return self.validated_knowledge.get(node_id)
    
    def get_all_validated_knowledge(self) -> Dict[str, KnowledgeNode]:
        """Get all knowledge that reached consensus"""
        return self.validated_knowledge
    
    def _generate_id(self, data: Any) -> str:
        """Generate deterministic ID for knowledge node"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def verify_references(self, references: List[str]) -> bool:
        """Verify that all referenced knowledge exists and is validated"""
        return all(ref in self.validated_knowledge for ref in references)

    def get_knowledge_chain(self, node_id: str) -> List[KnowledgeNode]:
        """Get the chain of referenced knowledge nodes"""
        chain = []
        current = self.get_knowledge(node_id)
        
        while current and current.references:
            chain.append(current)
            # Follow first reference (can be extended to handle multiple paths)
            current = self.get_knowledge(current.references[0]) if current.references else None
            
        return chain
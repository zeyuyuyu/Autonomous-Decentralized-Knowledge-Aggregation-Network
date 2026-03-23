import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class KnowledgeNode:
    content: str
    timestamp: datetime
    source: str
    hash: str
    validators: List[str]
    confidence: float

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_graph: Dict[str, KnowledgeNode] = {}
        self.peer_network: List[str] = []
        self.validation_threshold = 0.75
    
    def add_peer(self, peer_id: str) -> None:
        if peer_id not in self.peer_network:
            self.peer_network.append(peer_id)
    
    def remove_peer(self, peer_id: str) -> None:
        if peer_id in self.peer_network:
            self.peer_network.remove(peer_id)
    
    def submit_knowledge(self, content: str, source: str) -> str:
        timestamp = datetime.now()
        node_hash = self._generate_hash(content, timestamp, source)
        
        node = KnowledgeNode(
            content=content,
            timestamp=timestamp,
            source=source,
            hash=node_hash,
            validators=[],
            confidence=0.0
        )
        
        self.knowledge_graph[node_hash] = node
        return node_hash
    
    def validate_node(self, node_hash: str, validator_id: str) -> bool:
        if node_hash not in self.knowledge_graph:
            return False
            
        node = self.knowledge_graph[node_hash]
        if validator_id not in node.validators:
            node.validators.append(validator_id)
            node.confidence = len(node.validators) / len(self.peer_network)
            
        return True
    
    def get_consensus_knowledge(self) -> List[KnowledgeNode]:
        return [
            node for node in self.knowledge_graph.values()
            if node.confidence >= self.validation_threshold
        ]
    
    def _generate_hash(self, content: str, timestamp: datetime, source: str) -> str:
        hash_input = f"{content}{timestamp.isoformat()}{source}"
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def export_knowledge(self, filepath: str) -> None:
        consensus_nodes = self.get_consensus_knowledge()
        export_data = [
            {
                "content": node.content,
                "timestamp": node.timestamp.isoformat(),
                "source": node.source,
                "hash": node.hash,
                "validators": node.validators,
                "confidence": node.confidence
            }
            for node in consensus_nodes
        ]
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_knowledge(self, filepath: str) -> None:
        with open(filepath, 'r') as f:
            import_data = json.load(f)
            
        for node_data in import_data:
            node = KnowledgeNode(
                content=node_data["content"],
                timestamp=datetime.fromisoformat(node_data["timestamp"]),
                source=node_data["source"],
                hash=node_data["hash"],
                validators=node_data["validators"],
                confidence=node_data["confidence"]
            )
            self.knowledge_graph[node.hash] = node
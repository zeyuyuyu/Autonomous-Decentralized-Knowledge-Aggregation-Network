import hashlib
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class KnowledgeNode:
    content: Any
    timestamp: datetime
    source: str
    confidence: float
    hash: str = ''

    def __post_init__(self):
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        content_str = str(self.content) + str(self.timestamp) + self.source + str(self.confidence)
        return hashlib.sha256(content_str.encode()).hexdigest()

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_pool: Dict[str, List[KnowledgeNode]] = {}
        self.consensus_threshold = 0.75

    def add_knowledge(self, content: Any, source: str, confidence: float) -> str:
        """Add a new piece of knowledge to the network"""
        node = KnowledgeNode(
            content=content,
            timestamp=datetime.now(),
            source=source,
            confidence=confidence
        )
        
        if node.hash not in self.knowledge_pool:
            self.knowledge_pool[node.hash] = []
        self.knowledge_pool[node.hash].append(node)
        return node.hash

    def get_consensus_knowledge(self, hash_id: str) -> Dict[str, Any]:
        """Retrieve knowledge with consensus validation"""
        if hash_id not in self.knowledge_pool:
            return {'error': 'Knowledge not found'}

        nodes = self.knowledge_pool[hash_id]
        total_confidence = sum(node.confidence for node in nodes)
        avg_confidence = total_confidence / len(nodes)

        if avg_confidence >= self.consensus_threshold:
            return {
                'content': nodes[0].content,
                'sources': [node.source for node in nodes],
                'confidence': avg_confidence,
                'consensus': True,
                'timestamp': max(node.timestamp for node in nodes)
            }
        return {
            'error': 'Consensus threshold not met',
            'current_confidence': avg_confidence
        }

    def validate_knowledge(self, hash_id: str, source: str, confidence: float) -> bool:
        """Validate existing knowledge by adding confirmation"""
        if hash_id not in self.knowledge_pool:
            return False
            
        existing_node = self.knowledge_pool[hash_id][0]
        new_node = KnowledgeNode(
            content=existing_node.content,
            timestamp=datetime.now(),
            source=source,
            confidence=confidence
        )
        
        if new_node.hash == hash_id:
            self.knowledge_pool[hash_id].append(new_node)
            return True
        return False

    def get_network_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge network"""
        total_nodes = sum(len(nodes) for nodes in self.knowledge_pool.values())
        consensus_count = sum(
            1 for hash_id in self.knowledge_pool
            if self.get_consensus_knowledge(hash_id).get('consensus', False)
        )
        
        return {
            'total_knowledge_pieces': len(self.knowledge_pool),
            'total_nodes': total_nodes,
            'consensus_reached': consensus_count,
            'average_sources_per_knowledge': total_nodes / len(self.knowledge_pool) if self.knowledge_pool else 0
        }

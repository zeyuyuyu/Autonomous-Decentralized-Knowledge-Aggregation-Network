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
    confidence: float
    hash: str
    validators: List[str]

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_store: Dict[str, KnowledgeNode] = {}
        self.validation_threshold = 0.75
        self.min_validators = 3
    
    def add_knowledge(self, content: str, source: str) -> str:
        """Add new knowledge to the network with initial validation."""
        timestamp = datetime.utcnow()
        node_hash = self._generate_hash(content, timestamp, source)
        
        node = KnowledgeNode(
            content=content,
            timestamp=timestamp,
            source=source,
            confidence=0.0,
            hash=node_hash,
            validators=[]
        )
        
        self.knowledge_store[node_hash] = node
        return node_hash

    def validate_knowledge(self, node_hash: str, validator: str, validation_score: float) -> bool:
        """Validate knowledge node by network participants."""
        if node_hash not in self.knowledge_store:
            return False
            
        node = self.knowledge_store[node_hash]
        
        if validator in node.validators:
            return False
            
        node.validators.append(validator)
        
        # Update confidence score with new validation
        total_validations = len(node.validators)
        node.confidence = ((node.confidence * (total_validations - 1)) + validation_score) / total_validations
        
        return True

    def get_verified_knowledge(self) -> List[KnowledgeNode]:
        """Retrieve knowledge that meets validation criteria."""
        return [
            node for node in self.knowledge_store.values()
            if len(node.validators) >= self.min_validators 
            and node.confidence >= self.validation_threshold
        ]

    def query_knowledge(self, query: str) -> Optional[KnowledgeNode]:
        """Query verified knowledge by content match."""
        verified = self.get_verified_knowledge()
        matches = [
            node for node in verified
            if query.lower() in node.content.lower()
        ]
        return max(matches, key=lambda x: x.confidence) if matches else None

    def _generate_hash(self, content: str, timestamp: datetime, source: str) -> str:
        """Generate unique hash for knowledge node."""
        hash_input = f"{content}{timestamp.isoformat()}{source}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def export_knowledge(self, filepath: str) -> None:
        """Export verified knowledge to JSON file."""
        verified = self.get_verified_knowledge()
        export_data = [
            {
                'content': node.content,
                'timestamp': node.timestamp.isoformat(),
                'source': node.source,
                'confidence': node.confidence,
                'hash': node.hash,
                'validators': node.validators
            }
            for node in verified
        ]
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

    def import_knowledge(self, filepath: str) -> None:
        """Import knowledge from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        for item in data:
            node = KnowledgeNode(
                content=item['content'],
                timestamp=datetime.fromisoformat(item['timestamp']),
                source=item['source'],
                confidence=item['confidence'],
                hash=item['hash'],
                validators=item['validators']
            )
            self.knowledge_store[node.hash] = node
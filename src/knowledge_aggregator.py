import hashlib
from typing import Dict, List, Set
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Knowledge:
    content: str
    source: str
    timestamp: datetime
    confidence: float
    verification_count: int

@dataclass 
class PeerNode:
    id: str
    reputation: float
    contribution_count: int
    last_active: datetime

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_base: Dict[str, Knowledge] = {}
        self.peers: Dict[str, PeerNode] = {}
        self.consensus_threshold = 0.75
        
    def add_knowledge(self, content: str, source: str) -> str:
        """Add new knowledge entry with initial confidence score"""
        knowledge_id = hashlib.sha256(content.encode()).hexdigest()
        
        if knowledge_id not in self.knowledge_base:
            self.knowledge_base[knowledge_id] = Knowledge(
                content=content,
                source=source,
                timestamp=datetime.now(),
                confidence=0.1,
                verification_count=1
            )
            
            if source not in self.peers:
                self.peers[source] = PeerNode(
                    id=source,
                    reputation=0.5,
                    contribution_count=1,
                    last_active=datetime.now()
                )
            else:
                self.peers[source].contribution_count += 1
                self.peers[source].last_active = datetime.now()
                
        return knowledge_id

    def verify_knowledge(self, knowledge_id: str, verifier: str) -> float:
        """Verify knowledge and update confidence based on verifier reputation"""
        if knowledge_id not in self.knowledge_base:
            raise ValueError("Knowledge ID not found")
            
        knowledge = self.knowledge_base[knowledge_id]
        verifier_rep = self.peers.get(verifier, PeerNode(verifier, 0.5, 0, datetime.now())).reputation
        
        # Update confidence score using weighted average
        old_confidence = knowledge.confidence
        knowledge.verification_count += 1
        knowledge.confidence = (old_confidence + verifier_rep) / knowledge.verification_count
        
        # Update peer reputations
        if knowledge.confidence >= self.consensus_threshold:
            self._update_reputations(knowledge_id)
            
        return knowledge.confidence

    def _update_reputations(self, knowledge_id: str) -> None:
        """Update peer reputations based on consensus achievement"""
        knowledge = self.knowledge_base[knowledge_id]
        
        # Reward original contributor
        contributor = self.peers[knowledge.source]
        contributor.reputation = min(1.0, contributor.reputation + 0.1)
        
        # Update all peer reputations based on their verification alignment
        for peer in self.peers.values():
            if peer.last_active > knowledge.timestamp:
                alignment_factor = 0.05 * (1 if knowledge.confidence >= self.consensus_threshold else -1)
                peer.reputation = max(0.1, min(1.0, peer.reputation + alignment_factor))

    def get_verified_knowledge(self, min_confidence: float = 0.75) -> List[Knowledge]:
        """Get all knowledge entries above confidence threshold"""
        return [k for k in self.knowledge_base.values() if k.confidence >= min_confidence]

    def get_peer_rankings(self) -> List[PeerNode]:
        """Get peers sorted by reputation"""
        return sorted(
            self.peers.values(),
            key=lambda x: (x.reputation, x.contribution_count),
            reverse=True
        )

    def prune_inactive_peers(self, max_inactive_days: int = 30) -> None:
        """Remove peers inactive beyond threshold"""
        cutoff = datetime.now()
        inactive = [
            pid for pid, peer in self.peers.items()
            if (cutoff - peer.last_active).days > max_inactive_days
        ]
        for pid in inactive:
            del self.peers[pid]
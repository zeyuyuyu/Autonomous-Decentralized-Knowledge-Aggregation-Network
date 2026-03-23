import hashlib
from typing import List, Dict, Any
from datetime import datetime
import json

class KnowledgeNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.knowledge_store = {}
        self.peers = set()
        self.consensus_votes = {}
        self.confirmed_knowledge = {}

    def add_peer(self, peer_id: str) -> None:
        self.peers.add(peer_id)

    def remove_peer(self, peer_id: str) -> None:
        self.peers.discard(peer_id)

class ConsensusProtocol:
    def __init__(self, tolerance: float = 0.66):
        self.tolerance = tolerance
        self.proposals = {}
        self.votes = {}

    def propose_knowledge(self, knowledge_id: str, data: Dict[str, Any]) -> str:
        proposal = {
            'knowledge_id': knowledge_id,
            'data': data,
            'timestamp': datetime.utcnow().isoformat(),
            'hash': self._compute_hash(data)
        }
        self.proposals[knowledge_id] = proposal
        return proposal['hash']

    def vote(self, knowledge_id: str, node_id: str, accept: bool) -> None:
        if knowledge_id not in self.votes:
            self.votes[knowledge_id] = {}
        self.votes[knowledge_id][node_id] = accept

    def check_consensus(self, knowledge_id: str) -> bool:
        if knowledge_id not in self.votes:
            return False
        
        total_votes = len(self.votes[knowledge_id])
        accept_votes = sum(1 for v in self.votes[knowledge_id].values() if v)
        
        return accept_votes / total_votes >= self.tolerance

    @staticmethod
    def _compute_hash(data: Dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class KnowledgeAggregator:
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.consensus = ConsensusProtocol()

    def create_node(self, node_id: str) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = KnowledgeNode(node_id)

    def submit_knowledge(self, node_id: str, knowledge_id: str, data: Dict[str, Any]) -> str:
        if node_id not in self.nodes:
            raise ValueError(f'Node {node_id} does not exist')

        proposal_hash = self.consensus.propose_knowledge(knowledge_id, data)
        
        # Initiate voting process
        for peer_id in self.nodes[node_id].peers:
            self._request_vote(peer_id, knowledge_id, data)

        return proposal_hash

    def _request_vote(self, node_id: str, knowledge_id: str, data: Dict[str, Any]) -> None:
        # Simulate network communication and voting
        # In a real implementation, this would involve network calls
        is_valid = self._validate_knowledge(data)
        self.consensus.vote(knowledge_id, node_id, is_valid)

    def _validate_knowledge(self, data: Dict[str, Any]) -> bool:
        # Implement validation logic
        # This is a placeholder that always returns True
        return True

    def get_consensus_status(self, knowledge_id: str) -> bool:
        return self.consensus.check_consensus(knowledge_id)

    def get_confirmed_knowledge(self, knowledge_id: str) -> Dict[str, Any]:
        if not self.get_consensus_status(knowledge_id):
            raise ValueError(f'No consensus reached for knowledge {knowledge_id}')
        return self.consensus.proposals[knowledge_id]['data']

    def get_network_status(self) -> Dict[str, Any]:
        return {
            'node_count': len(self.nodes),
            'active_proposals': len(self.consensus.proposals),
            'consensus_reached': sum(1 for k in self.consensus.proposals 
                                   if self.get_consensus_status(k))
        }
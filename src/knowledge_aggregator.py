import hashlib
import json
from typing import Dict, List

class KnowledgeNode:
    def __init__(self, data: Dict[str, any]):
        self.data = data
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.data, sort_keys=True).encode()).hexdigest()

class KnowledgeAggregator:
    def __init__(self):
        self.nodes: List[KnowledgeNode] = []
        self.consensus_threshold = 0.6

    def add_node(self, node: KnowledgeNode):
        for existing_node in self.nodes:
            if existing_node.hash == node.hash:
                return
        self.nodes.append(node)

    def get_consensus_knowledge(self) -> Dict[str, any]:
        node_counts: Dict[str, int] = {}
        for node in self.nodes:
            node_hash = node.hash
            if node_hash not in node_counts:
                node_counts[node_hash] = 1
            else:
                node_counts[node_hash] += 1

        consensus_data = None
        consensus_hash = None
        for node_hash, count in node_counts.items():
            if count / len(self.nodes) >= self.consensus_threshold:
                for node in self.nodes:
                    if node.hash == node_hash:
                        consensus_data = node.data
                        consensus_hash = node_hash
                        break
                break

        return consensus_data

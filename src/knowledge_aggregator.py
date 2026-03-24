import asyncio
import json
import hashlib
from typing import List

class KnowledgeNode:
    def __init__(self, node_id: str, knowledge: dict):
        self.node_id = node_id
        self.knowledge = knowledge
        self.peers: List[KnowledgeNode] = []
        self.consensus_weight = 1.0

    async def sync_knowledge(self):
        await asyncio.gather(*[peer.sync_with(self) for peer in self.peers])
        self.knowledge = self.aggregate_knowledge()

    async def sync_with(self, other_node: 'KnowledgeNode'):
        if self.node_id < other_node.node_id:
            self.knowledge.update(other_node.knowledge)
            other_node.consensus_weight *= 0.9
        else:
            other_node.knowledge.update(self.knowledge)
            self.consensus_weight *= 0.9

    def aggregate_knowledge(self) -> dict:
        aggregated = {}
        for node in self.peers + [self]:
            for topic, info in node.knowledge.items():
                if topic not in aggregated or node.consensus_weight > aggregated[topic]['consensus_weight']:
                    aggregated[topic] = {
                        'content': info['content'],
                        'consensus_weight': node.consensus_weight
                    }
        return aggregated

class KnowledgeAggregator:
    def __init__(self, node_id: str):
        self.node = KnowledgeNode(node_id, {})
        self.node_registry = {node_id: self.node}

    def register_node(self, node: KnowledgeNode):
        self.node_registry[node.node_id] = node
        self.node.peers.append(node)
        node.peers.append(self.node)

    async def update_knowledge(self, topic: str, content: str):
        self.node.knowledge[topic] = {'content': content, 'consensus_weight': 1.0}
        await self.node.sync_knowledge()

    async def query_knowledge(self, topic: str) -> dict:
        await self.node.sync_knowledge()
        return self.node.knowledge.get(topic, {})

import hashlib
import json
import time
from typing import Dict, List

class KnowledgeBlock:
    def __init__(self, data: Dict, timestamp: float, prev_hash: str):
        self.data = data
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class KnowledgeChain:
    def __init__(self):
        self.chain: List[KnowledgeBlock] = []
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis_block = KnowledgeBlock({
            'index': 0,
            'data': 'Genesis Block'
        }, time.time(), '0')
        self.chain.append(genesis_block)

    def add_block(self, data: Dict) -> KnowledgeBlock:
        prev_block = self.chain[-1]
        new_block = KnowledgeBlock(data, time.time(), prev_block.hash)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

        return True

class KnowledgeConsensus:
    def __init__(self, peers: List[str]):
        self.chain = KnowledgeChain()
        self.peers = peers

    def broadcast_block(self, block: KnowledgeBlock):
        for peer in self.peers:
            # Simulate broadcasting the block to peers
            print(f'Broadcasting block to {peer}')

    def reach_consensus(self) -> bool:
        majority_chain = self.chain
        for peer in self.peers:
            # Simulate retrieving the chain from a peer
            peer_chain = self.retrieve_chain_from_peer(peer)
            if len(peer_chain.chain) > len(majority_chain.chain) and peer_chain.is_chain_valid():
                majority_chain = peer_chain

        if majority_chain != self.chain:
            self.chain = majority_chain
            return True
        return False

    def retrieve_chain_from_peer(self, peer: str) -> KnowledgeChain:
        # Simulate retrieving the chain from a peer
        return KnowledgeChain()

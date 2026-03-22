import os
import ipfs
import blockchain
import json

class KnowledgeNode:
    def __init__(self, node_id, knowledge_base):
        self.node_id = node_id
        self.knowledge_base = knowledge_base
        self.connections = []

    def connect(self, other_node):
        self.connections.append(other_node)
        other_node.connections.append(self)

    def add_knowledge(self, knowledge):
        self.knowledge_base.append(knowledge)
        self.publish_knowledge()

    def publish_knowledge(self):
        for connection in self.connections:
            connection.sync_knowledge(self.knowledge_base)

    def sync_knowledge(self, new_knowledge):
        self.knowledge_base.extend(new_knowledge)
        self.knowledge_base = list(set(self.knowledge_base))

    def query_knowledge(self, query):
        results = []
        for item in self.knowledge_base:
            if query in item:
                results.append(item)
        return results

class KnowledgeNetwork:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def connect_nodes(self, node1, node2):
        node1.connect(node2)

    def publish_knowledge(self, node, knowledge):
        node.add_knowledge(knowledge)

    def query_network(self, query):
        results = []
        for node in self.nodes:
            results.extend(node.query_knowledge(query))
        return results

# Example usage
node1 = KnowledgeNode('node1', ['Python is a programming language', 'Machine learning is a field of AI'])
node2 = KnowledgeNode('node2', ['Data science is the study of data', 'Blockchain is a distributed ledger technology'])
node3 = KnowledgeNode('node3', ['Autonomous systems are self-governing', 'Decentralization means no single point of control'])

network = KnowledgeNetwork()
network.add_node(node1)
network.add_node(node2)
network.add_node(node3)

network.connect_nodes(node1, node2)
network.connect_nodes(node2, node3)
network.connect_nodes(node3, node1)

network.publish_knowledge(node1, 'Artificial intelligence is the study of creating intelligent agents')
network.publish_knowledge(node2, 'Cryptography is the practice and study of secure communication')
network.publish_knowledge(node3, 'Distributed systems are collections of independent computers')

print(network.query_network('programming language'))
print(network.query_network('distributed'))

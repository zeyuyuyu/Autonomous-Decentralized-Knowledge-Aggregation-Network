import os
import asyncio
import multiprocessing as mp
from swarm.agents import KnowledgeAggregationAgent
from swarm.cluster import AgentCluster
from governance.decentralized_protocol import DecentralizedGovernanceProtocol

def main():
    # Initialize the decentralized governance protocol
    governance_protocol = DecentralizedGovernanceProtocol()

    # Create the agent cluster
    agent_cluster = AgentCluster(governance_protocol=governance_protocol)

    # Spawn the knowledge aggregation agents
    for _ in range(100):
        agent = KnowledgeAggregationAgent(agent_cluster)
        agent_cluster.add_agent(agent)

    # Start the agent cluster
    agent_cluster.start()

    # Run the event loop
    asyncio.run(agent_cluster.run())

if __name__ == '__main__':
    main()
import os
import json
from typing import List, Dict

class KnowledgeAggregator:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.knowledge_base: Dict[str, Dict] = {}
        self.load_knowledge_base()

    def load_knowledge_base(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.data_dir, filename), 'r') as f:
                    data = json.load(f)
                    self.knowledge_base.update(data)

    def query_knowledge_base(self, query: str) -> List[Dict]:
        results = []
        for _, item in self.knowledge_base.items():
            if query.lower() in item['content'].lower():
                results.append(item)
        return results

    def synthesize_knowledge(self, queries: List[str]) -> Dict[str, float]:
        synthesis = {}
        for query in queries:
            results = self.query_knowledge_base(query)
            if results:
                synthesis[query] = self._compute_relevance(results)
        return synthesis

    def _compute_relevance(self, results: List[Dict]) -> float:
        relevance = 0
        for result in results:
            relevance += len(result['content'].split()) / len(result['title'].split())
        return relevance / len(results)

    def reason_about_knowledge(self, synthesis: Dict[str, float]) -> Dict[str, float]:
        reasoning = {}
        for query, relevance in synthesis.items():
            reasoning[query] = self._infer_reasoning(query, relevance)
        return reasoning

    def _infer_reasoning(self, query: str, relevance: float) -> float:
        # Implement logic to infer reasoning based on query and relevance
        if relevance > 0.8:
            return 0.9
        elif relevance > 0.5:
            return 0.7
        else:
            return 0.4

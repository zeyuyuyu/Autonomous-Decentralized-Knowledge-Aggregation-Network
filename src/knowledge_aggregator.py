import numpy as np
from typing import List, Dict, Tuple

class KnowledgeAggregator:
    def __init__(self):
        self.knowledge_sources = {}
        self.source_weights = {}
        self.confidence_threshold = 0.75

    def add_knowledge_source(self, source_id: str, reliability_score: float = 1.0):
        """Add a new knowledge source with an optional reliability score"""
        self.knowledge_sources[source_id] = []
        self.source_weights[source_id] = reliability_score

    def submit_knowledge(self, source_id: str, knowledge: Dict, confidence: float):
        """Submit a piece of knowledge with associated confidence score"""
        if source_id not in self.knowledge_sources:
            raise ValueError(f'Unknown knowledge source: {source_id}')
        
        self.knowledge_sources[source_id].append({
            'content': knowledge,
            'confidence': confidence,
            'timestamp': np.datetime64('now')
        })

    def aggregate_knowledge(self) -> List[Tuple[Dict, float]]:
        """Aggregate knowledge across sources using weighted consensus"""
        all_knowledge = []
        
        # Collect all knowledge pieces with their weighted confidence scores
        for source_id, submissions in self.knowledge_sources.items():
            source_weight = self.source_weights[source_id]
            
            for submission in submissions:
                weighted_confidence = submission['confidence'] * source_weight
                all_knowledge.append({
                    'content': submission['content'],
                    'weighted_confidence': weighted_confidence,
                    'timestamp': submission['timestamp']
                })

        # Group similar knowledge and combine confidence scores
        aggregated = {}
        for item in all_knowledge:
            key = str(item['content'])  # Use content as key for grouping
            if key not in aggregated:
                aggregated[key] = {
                    'content': item['content'],
                    'confidence_sum': item['weighted_confidence'],
                    'count': 1,
                    'latest_timestamp': item['timestamp']
                }
            else:
                aggregated[key]['confidence_sum'] += item['weighted_confidence']
                aggregated[key]['count'] += 1
                aggregated[key]['latest_timestamp'] = max(
                    aggregated[key]['latest_timestamp'],
                    item['timestamp']
                )

        # Calculate final confidence scores and filter results
        results = []
        for item in aggregated.values():
            final_confidence = item['confidence_sum'] / item['count']
            if final_confidence >= self.confidence_threshold:
                results.append((item['content'], final_confidence))

        # Sort by confidence score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_top_knowledge(self, n: int = 10) -> List[Tuple[Dict, float]]:
        """Get top N knowledge items by confidence score"""
        aggregated = self.aggregate_knowledge()
        return aggregated[:n]

    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold for including knowledge in results"""
        if not 0 <= threshold <= 1:
            raise ValueError('Confidence threshold must be between 0 and 1')
        self.confidence_threshold = threshold
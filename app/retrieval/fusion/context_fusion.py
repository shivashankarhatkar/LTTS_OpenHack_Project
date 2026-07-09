"""
Context fusion.

Combines graph, vector and keyword retrieval.
"""

from __future__ import annotations


class ContextFusion:
    """
    Merge retrieval results.
    """

    def fuse(
        self,
        graph_results: list,
        vector_results: list,
        keyword_results: list,
    ) -> dict:
        """
        Merge retrieval outputs.
        """

        return {
            "graph": graph_results,
            "vector": vector_results,
            "keyword": keyword_results,
        }


context_fusion = ContextFusion()
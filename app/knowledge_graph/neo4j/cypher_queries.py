"""
Centralized Cypher queries for the Knowledge Graph.
"""

CREATE_ENTITY_NODE = """
MERGE (n:{label} {id:$id})
SET n += $properties
"""

CREATE_RELATIONSHIP = """
MATCH (a {id:$source_id})
MATCH (b {id:$target_id})
MERGE (a)-[r:{relationship}]->(b)
SET r += $properties
"""

GET_NODE = """
MATCH (n {id:$id})
RETURN n
"""

DELETE_NODE = """
MATCH (n {id:$id})
DETACH DELETE n
"""

CLEAR_DATABASE = """
MATCH (n)
DETACH DELETE n
"""

GET_ALL_NODES = """
MATCH (n)
RETURN n
"""

GET_ALL_RELATIONSHIPS = """
MATCH (a)-[r]->(b)
RETURN a,r,b
"""